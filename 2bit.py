bits = 2
outfile = "out.png"
per_color = False
dither = False

# End of the configuration section

import PIL.Image, sys, random
sys.path.append(".")
import libbar
if len(sys.argv) >= 3:
    outfile = sys.argv[2]
if len(sys.argv) >= 4:
    bits = int(sys.argv[3])
args = [f.lower() for f in sys.argv]
if "--dither" in args:
    dither = float(args[args.index("--dither") + 1].replace("%",""))
if dither > 1:
    dither /= 100
per_color = "--per-color" in args
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
bar = libbar.IncrementalBar(max = image.height * image.width)
bar.start()
i = 0
for x in range(image.width):
    for y in range(image.height):
        i += 1
        bar.index = i
        if i % 200 == 0: bar.update()
        pos = (x,y)
        color = image.getpixel(pos)
        if len(color) == 4:
            color = color[:3] # Exclude alpha layer
        color = list(color)
        if not per_color:
            color = [float(sum(color))/len(color)]
        for z in range(len(color)):
            if dither:
                color[z] += 255 * random.uniform(-dither,dither)
                color[z] = min(color[z], 255)
                color[z] = max(color[z], 0)
            index = int(binprecision(color[z], 8, bits), 2)
            color[z] = colors[index]
        out.putpixel(pos, tuple(color))
out.save(outfile)
bar.finish()
