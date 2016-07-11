import glob, subprocess, os
try:
    import shutil
    shutil.rmtree("out")
except:
    pass
files = glob.glob("*")
del files[files.index("run.py")]
if not os.path.isdir("out"): os.mkdir("out")
i = 0
max_i = len(files) * (16*3)

def getparams(i):
    percolor = dither = False
    if i % 16 >= 8:
        percolor = True
    if i >= 16:
        dither = '15'
    if i >= 32:
        dither = '50'
    return percolor, dither

for f in files:
    if (os.path.isdir(f)): continue
    if (f[-3:]) == '.py': continue
    for bits in range(16*3):
        bits += 1
        percolor, dither = getparams(i)
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
        print(str(int(float(1000*i)/max_i)/10) + "% done")
        bits_formatted = str((bits-1)%8+1)
        outfilename = "out/" + ".".join(f.split(".")[:-1]) + "-output-" + pc + dc + bits_formatted + "bits.png"
        print("On " + outfilename)
        subprocess.call(["python3", "../2bit.py", f, outfilename, bits_formatted, *percolor, *dither])
        i += 1
