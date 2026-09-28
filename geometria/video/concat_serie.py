# concat_serie.py: join the rendered parts of one video of the series.
# Usage:  python concat_serie.py v1_numeri            (1080p60 renders)
#         python concat_serie.py v1_numeri 480p15     (low quality test renders)
# Output: consegna/<script>.mp4, and if it is larger than LIMIT_MB also
#         consegna/<script>_parte1.mp4 and _parte2.mp4, split at a scene boundary.
import os
import re
import subprocess
import sys

LIMIT_MB = 29.0
SCRIPT = sys.argv[1].removesuffix(".py")
QUALITY = sys.argv[2] if len(sys.argv) > 2 else "1080p60"
OUT_DIR = "consegna"
media_dir = os.path.join("media", "videos", SCRIPT, QUALITY)

with open(f"{SCRIPT}.py", encoding="utf-8") as f:
    scenes = re.findall(r"^class (\w+)\(LessonScene\)", f.read(), flags=re.M)

paths = [os.path.abspath(os.path.join(media_dir, f"{s}.mp4")) for s in scenes]
missing = [p for p in paths if not os.path.isfile(p)]
if missing:
    print("Missing renders:", *missing, sep="\n   ")
    sys.exit(1)


def join(parts, out):
    """concat without re-encoding the video, then rebuild the audio so every
    scene's sound stays aligned (each scene's audio ends a little before its video)"""
    lst = out + ".txt"
    with open(lst, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    raw = out + ".raw.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", raw], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-c:v", "copy",
                    "-af", "aresample=async=1:first_pts=0,apad", "-shortest",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
    os.remove(raw)
    os.remove(lst)
    mb = os.path.getsize(out) / 2**20
    print(f"{out}: {mb:.1f} MB")
    return mb


os.makedirs(OUT_DIR, exist_ok=True)
suffix = "" if QUALITY == "1080p60" else f"_{QUALITY}"
full = os.path.join(OUT_DIR, f"{SCRIPT}{suffix}.mp4")
if join(paths, full) > LIMIT_MB:
    sizes = [os.path.getsize(p) for p in paths]
    total = sum(sizes)
    best = min(range(1, len(paths)), key=lambda k: abs(sum(sizes[:k]) - total / 2))
    join(paths[:best], os.path.join(OUT_DIR, f"{SCRIPT}{suffix}_parte1.mp4"))
    join(paths[best:], os.path.join(OUT_DIR, f"{SCRIPT}{suffix}_parte2.mp4"))
