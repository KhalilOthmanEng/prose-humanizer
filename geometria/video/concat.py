# concat.py: run after rendering all acts.
# Usage:  python concat.py            (1080p60 renders, output lezione_geometria.mp4)
#         python concat.py 480p15     (low quality test renders)
import os
import subprocess
import sys

SCRIPT_NAME = "lezione_geometria"
QUALITY = sys.argv[1] if len(sys.argv) > 1 else "1080p60"
OUTPUT = "lezione_geometria.mp4" if QUALITY == "1080p60" else f"lezione_geometria_{QUALITY}.mp4"

ACTS = [
    "P01_Porta",
    "P02_Circonferenza",
    "P03_Perche360",
    "P04_Tipi",
    "P05_Coppie",
    "P06_Parallele",
    "P07_Somma180",
    "P08_Altezze",
    "P09_Congruenza",
    "P10_Criteri",
    "P11_Dimostrazioni",
    "P12_Quaderno",
    "P13_Riepilogo",
]

media_dir = os.path.join("media", "videos", SCRIPT_NAME, QUALITY)
filelist = "filelist.txt"

missing, paths = [], []
for act in ACTS:
    p = os.path.abspath(os.path.join(media_dir, f"{act}.mp4"))
    if not os.path.isfile(p):
        missing.append(p)
    paths.append(p)

if missing:
    print("The following rendered files are missing:")
    for m in missing:
        print("   ", m)
    print("\nRender them first with:  manim -qh lezione_geometria.py <ActName>")
    sys.exit(1)

with open(filelist, "w", encoding="utf-8") as f:    # utf-8 without BOM
    for p in paths:
        f.write(f"file '{p}'\n")

cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", filelist,
       "-c", "copy", "-movflags", "+faststart", OUTPUT]
print("Running:", " ".join(cmd))
r = subprocess.run(cmd)
if r.returncode == 0:
    print(f"Done. Output: {OUTPUT}")
else:
    print(f"ffmpeg failed with exit code {r.returncode}")
    sys.exit(r.returncode)
