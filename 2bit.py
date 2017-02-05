#!/usr/bin/env python3
bits = 2
outfile = "out.png"
per_color = False
dither = False
use_non_random_dither = False
no_status_bar = False

# End of the configuration section

import PIL.Image, sys, random
import pip._vendor.progress.bar as libbar
# Returns a human readable percentage, so for a d of 0.1234567 it would return 12.3%
def format_dither(d):
    d = float(int(float(dither) * 1000)) / 10
    return str(d) + "%"
# Attempts to guess the dither percentage based off the number of bits, based on the assumption that a lower bit depth requires more dither
def auto_dither(bits):
    #return 1.0 / (bits + 1)
    return 1.0 / (2**bits)
# A little complicated. This takes the height of the image and tries to generate a number of pixels for non-random dither.
# The basis is that if the height is a multiple of the number it returns, there will be ugly banding because the percentage of dither applied will be the same for an entire scanline.
# The unfortunate part is that due to other reasons, the number it returns isn't actually the number of pixels, it's one less than the number of pixels used, which is the oly reason it seems so complicated.
#Also, it tries to generate a sane minimum so that on extremely large images it doesn't use tiny nonrandom dither counter values, but usually values lower than 4 look grainy.
def auto_counter_max(h):
    k = max(int(float(h)/200),4)
    while h % (k + 1) == 0: k += 1
    return k
# Take a number, convert it to binary and truncate it based on how many bits the user wants.
def binprecision(start, bits, length):
    end = bin(int(start))[2:]
    while len(end) < bits:
        end = '0' + end
    return end[:length]
# Set variables based on command line arguments
if len(sys.argv) >= 3:
    outfile = sys.argv[2]
if len(sys.argv) >= 4:
    bits = int(sys.argv[3])
# Lowercase the rest of the arguments in case the user typed them wrong
args = [f.lower() for f in sys.argv]
# Get the argument that comes after --dither in args and if it's "auto" then guess what value to use
if "--dither" in args:
    dither = args[args.index("--dither") + 1].replace("%","")
    if dither == "auto":
        dither = auto_dither(bits)
        print("Using dither of " + format_dither(dither))
    else:
        dither = float(dither)
# If the user specified 0.55 then dither would be set to 0.55, however if they specified 55% then it would be set to 55, so if the dither is greater than one we should divide it by 100 to get the float value
if dither > 1:
    dither /= 100
# set percolor to true if "--per-color" appears anywhere in the arguments, same for displaying the status bar
per_color = "--per-color" in args
no_status_bar = "--no-status-bar" in args
# This is very similar to the logic for automatically setting dither, however it checks if dither was not set at all, and if dither was not set but nonrandom dither *was* set, then we automatically select a dither value
use_non_random_dither = "--non-random-dither" in args
if use_non_random_dither:
    counter_max = args[args.index("--non-random-dither") + 1]
    if counter_max == "auto":
        counter_max = auto_counter_max(image.height)
        print("Using non-random dither counter value of " + str(counter_max) + " pixels")
    else:
        counter_max = int(counter_max)
    if not dither:
        dither = auto_dither(bits)
        print("Non-random dither has no effect if dither is disabled. Guessing you want "+format_dither(dither)+" dither")
# Mode for the output file.
mode = "L" # 1x8 bit unsigned integer
if per_color:
    mode = "RGB" # one eight byte unsigned integer per channel
elif bits == 1:
    # We do this because it allows us to compress the data a lot easier
    mode = "1" # 1x1 bit unsigned integer
# Begin creating some objects
image = PIL.Image.open(sys.argv[1])
out = PIL.Image.new(mode,image.size)
# This actually generates a number of colors equal to two to the power of the bit depth. So if your bit depth was one, it would return a list of (black, white), while if your bit depth was 8, it would return a list of 255 different shades of grey, in order
colors = [int(i*255.0/(2**bits-1)) for i in range(2**bits)]
# Create a status bar
if not no_status_bar:
    bar = libbar.IncrementalBar(max = image.height * image.width)
    bar.start()
# i is used to update the bar
i = 0
if use_non_random_dither:
    counter = 1
# Main loop
for x in range(image.width):
    for y in range(image.height):
        i += 1
        # This is the logic where the maximum value of counter will actually be set to counter_max, I mentioned this in the auto_counter_max function
        if use_non_random_dither:
            counter += 1
            counter %= counter_max + 1
        if not no_status_bar:
            bar.index = i
            if i % 193 == 0: bar.update() # I used to use 200 but then the last two digits of the current status were always "00" which made it look like the progress bar was fake
        pos = (x,y)
        color = image.getpixel(pos)
        # Cast all the colors to a list so I can average them the same way. color will only be an integer if the input file specified was greyscale
        if type(color) == int:
            color = (color,)
        if len(color) == 4:
            color = color[:3] # Exclude alpha layer
        color = list(color)
        # If we're just taking the average of all the colors (i.e. not using bits per color, actually using bits per pixel), set color to the average of the three (or one for greyscale images) channels.
        if not per_color:
            color = [float(sum(color))/len(color)]
        # For each color in the list (which is only one float long if we did not select percolor, otherwise three)
        for z in range(len(color)):
            # If we're applying dither
            if dither:
                # Add a random amount of dither within the dither percentage
                val = 255 * random.uniform(-dither, dither)
                # if we're using non-random dither, determine the value to be added based of both the dither percentage and the current counter value.
                if use_non_random_dither:
                    val = 255*float(counter)/counter_max # goes from 0 to 255
                    val *= dither # for dither = .1 and counter max = 4 it goes from 0 to 25.5
                    val *= 2 # 0 to +51
                    val -= 255 * dither # -25.5 to +25.5
                    val = int(val)
                    # Actually add the value, then make sure we're within allowable range
                color[z] += val
                color[z] = min(color[z], 255)
                color[z] = max(color[z], 0)
            # Now we have our dithered color which is either an average of all the channels of the pixel (in which case range(len(colors)) is [0] and this loop will end now) or the one channel for the pixel we're on, in which case this loop will repeat for all the colors
            # We then cut that dithered value down to our desired bit depth, and use that number as an index to the big list of colors we generated right before we entered the main loop.
            index = int(binprecision(color[z], 8, bits), 2)
            color[z] = colors[index]
        # color has now been set to the processed values and we can pass it as an argument to putpixel for the outfile.
        out.putpixel(pos, tuple(color))
out.save(outfile)
if not no_status_bar:
    bar.update() # Otherwise it will display the last multiple of 193 out of the total value
    bar.finish()
