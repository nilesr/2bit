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
max_i = len(files) * (8+8)
for f in files:
    if (os.path.isdir(f)): continue
    for bits in range(8+8):
        bits += 1
        percolor = []
        pc = ""
        if bits > 8:
            percolor = ["--per-color"]
            pc = "-per-color"
        print(str(int(float(1000*i)/max_i)/10) + "% done")
        bits_formatted = str((bits-1)%8+1)
        outfilename = "out/" + ".".join(f.split(".")[:-1]) + "-output" + pc + "-" + bits_formatted + "bits.png"
        print("On " + outfilename)
        subprocess.call(["python3", "../2bit.py", f, outfilename, bits_formatted, *percolor])
        i += 1
