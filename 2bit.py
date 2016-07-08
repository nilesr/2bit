bits = 2
outfile = "out.png"
print_debug = False

# End of the configuration section

import PIL.Image, sys
def debug(*args):
    if print_debug: print(*args)
def binprecision(start, bits, length):
    end = bin(int(start))[2:]
    while len(end) < bits:
        end = '0' + end
    return end[:length]
image = PIL.Image.open(sys.argv[1])
mode = "L"
if bits == 1:
    mode = "1"
out = PIL.Image.new(mode,image.size)
colors = [int(i*255.0/(2**bits-1)) for i in range(2**bits)]
debug(image.width, image.height)
for x in range(image.width):
    for y in range(image.height):
        pos = (x,y)
        color = image.getpixel(pos)
        debug(color)
        if len(color) == 4:
            color = color[:3] # Exclude alpha layer
        color = float(sum(color))/len(color)
        debug(color)
        debug(bin(int(color)))
        index = int(binprecision(color, 8, bits), 2)
        debug(index)
        out.putpixel(pos, colors[index])
        debug()
    debug("------------")
    debug()
out.save(outfile)
