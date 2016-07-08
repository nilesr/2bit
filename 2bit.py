bits = 2
outfile = "out.png"
print_debug = False
per_color = False

# End of the configuration section

import PIL.Image, sys
if len(sys.argv) >= 3:
    outfile = sys.argv[2]
if len(sys.argv) >= 4:
    bits = int(sys.argv[3])
per_color = "--per-color" in [f.lower() for f in sys.argv]
def debug(*args):
    if print_debug: print(*args)
def binprecision(start, bits, length):
    end = bin(int(start))[2:]
    while len(end) < bits:
        end = '0' + end
    return end[:length]
image = PIL.Image.open(sys.argv[1])
mode = "L" # 1x8 bit unsigned integer
if per_color:
    mode = "RGB"
elif bits == 1:
    mode = "1" # 1x1 bit unsigned integer
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
        color = list(color)
        if not per_color:
            color = [float(sum(color))/len(color)]
        debug(color)
        for z in color: debug(bin(int(z)))
        for z in range(len(color)):
            index = int(binprecision(color[z], 8, bits), 2)
            debug(index)
            color[z] = colors[index]
        out.putpixel(pos, tuple(color))
        debug()
    debug("------------")
    debug()
out.save(outfile)
