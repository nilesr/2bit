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
max_i = len(files) * 8
for f in files:
    if (os.path.isdir(f)): continue
    for bits in range(8):
        bits += 1
        print(str(int(float(1000*i)/max_i)/10) + "% done")
        outfilename = "out/" + f.split(".")[:-1] + "-output-" + str(bits) + "bits.png"
        print("On " + outfilename)
        subprocess.call(["python3", "../2bit.py", f, outfilename, str(bits)])
        i += 1
