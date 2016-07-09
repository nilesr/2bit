import PIL.Image
import itertools
bar_height = 10
permutations = list(itertools.permutations([0, 255, "S", "S", "S"], 3))
image = PIL.Image.new("RGB", (255, bar_height * len(permutations))) # Size subject to change
offset = 0
for combination in permutations:
    for x in range(255):
        for y in range(offset * bar_height, (offset + 1) * bar_height):
            color = []
            for c in combination:
                if type(c) == str:
                    color.append(x)
                else:
                    color.append(c)
            image.putpixel((x,y),tuple(color))
    offset += 1
image.save("out.png")
