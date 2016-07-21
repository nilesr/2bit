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
torun = []
for f in files:
    if (os.path.isdir(f)): continue
    if (f[-3:]) == '.py': continue
    for bits in range(8):
        for dither in [False, "15", "50", "auto"]:
            for nonrandom in [False, "7", "10", "auto"]:
                for percolor in [False, True]:
                    if nonrandom and not dither: continue
                    torun.append([bits, percolor, dither, nonrandom])
print(str(len(torun)) + " images to generate")
i = 0
for args in torun:
    i += 1
    print(str(int(i * 1000 / len(torun))/10.0) + "% done")
    run(*args)

print("Done")
