bits = 2
outfile = "out.png"
per_color = False
dither = False
use_non_random_dither = False

# End of the configuration section

import PIL.Image, sys, random
import pip._vendor.progress.bar as libbar
def format_dither(d):
    d = float(int(float(dither) * 1000)) / 10
    return str(d) + "%"
def auto_dither(bits):
    #return 1.0 / (bits + 1)
    return 1.0 / (2**bits)
def auto_counter_max(w):
    k = max(int(float(w)/200),2)
    while w % (k + 1) == 0: k += 1
    return k
if len(sys.argv) >= 3:
    outfile = sys.argv[2]
if len(sys.argv) >= 4:
    bits = int(sys.argv[3])
args = [f.lower() for f in sys.argv]
if "--dither" in args:
    dither = args[args.index("--dither") + 1].replace("%","")
    if dither == "auto":
        dither = auto_dither(bits)
        print("Using dither of " + format_dither(dither))
    else:
        dither = float(dither)
if dither > 1:
    dither /= 100
per_color = "--per-color" in args
use_non_random_dither = "--non-random-dither" in args
image = PIL.Image.open(sys.argv[1])
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
def binprecision(start, bits, length):
    end = bin(int(start))[2:]
    while len(end) < bits:
        end = '0' + end
    return end[:length]
mode = "L" # 1x8 bit unsigned integer
if per_color:
    mode = "RGB"
elif bits == 1:
    mode = "1" # 1x1 bit unsigned integer
out = PIL.Image.new(mode,image.size)
colors = [int(i*255.0/(2**bits-1)) for i in range(2**bits)]
bar = libbar.IncrementalBar(max = image.height * image.width)
bar.start()
i = 0
if use_non_random_dither:
    counter = 1
for x in range(image.width):
    for y in range(image.height):
        i += 1
        if use_non_random_dither:
            counter += 1
            counter %= counter_max + 1
        bar.index = i
        if i % 193 == 0: bar.update() # I used to use 200 but then the last two digits of the current status were always "00" which made it look like the progress bar was fake
        pos = (x,y)
        color = image.getpixel(pos)
        if type(color) == int:
            color = (color,)
        if len(color) == 4:
            color = color[:3] # Exclude alpha layer
        color = list(color)
        if not per_color:
            color = [float(sum(color))/len(color)]
        for z in range(len(color)):
            if dither:
                val = 255 * random.uniform(-dither, dither)
                if use_non_random_dither:
                    val = 255*float(counter)/counter_max # goes from 0 to 255
                    val *= dither # for dither = .1 and counter max = 4 it goes from 0 to 25.5
                    val *= 2 # 0 to +51
                    val -= 255 * dither # -25.5 to +25.5
                    val = int(val)
                color[z] += val
                color[z] = min(color[z], 255)
                color[z] = max(color[z], 0)
            index = int(binprecision(color[z], 8, bits), 2)
            color[z] = colors[index]
        out.putpixel(pos, tuple(color))
out.save(outfile)
bar.update() # Otherwise it will display the last multiple of 193 out of the total value
bar.finish()
