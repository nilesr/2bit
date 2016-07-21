import glob, subprocess, os
try:
    import shutil
    shutil.rmtree("out")
except:
    pass
files = glob.glob("*")
del files[files.index("gentest.py")]
del files[files.index("run.py")]
if not os.path.isdir("out"): os.mkdir("out")
i = 0
max_i = len(files) * (112)
def run(bits, percolor, dither, nonrandom):
    if not percolor:
        percolor = []
        pc = ""
    else:
        percolor = ["--per-color"]
        pc = "per-color-"
    if not dither:
        dither = []
        dc = ""
    else:
        dc = "dither-" + dither + "%-"
        dither = ["--dither", dither]
    if not nonrandom:
        nonrandom = []
        nc = ""
    else:
        nc = "nonrandom-dither-" + nonrandom + "pixels-"
        nonrandom = ["--non-random-dither", nonrandom]
    bits_formatted = str(bits + 1)
    outfilename = "out/" + ".".join(f.split(".")[:-1]) + "-output-" + pc + dc + nc + bits_formatted + "bits.png"
    print("On " + outfilename)
    subprocess.call(["python3", "../2bit.py", f, outfilename, bits_formatted, *percolor, *dither, *nonrandom])
print(str(max_i) + " images to generate")
for f in files:
    if (os.path.isdir(f)): continue
    if (f[-3:]) == '.py': continue
    for bits in range(8):
        for dither in [False, "15", "50", "auto"]:
            for nonrandom in [False, "7", "10"]:
                for percolor in [False, True]:
                    if nonrandom and not dither: continue
                    i += 1
                    run(bits, percolor, dither, nonrandom)
                    print(str(int(float(1000*i)/max_i)/10) + "% done")

print("Done")
