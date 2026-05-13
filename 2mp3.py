import glob
import os
import subprocess

# 検索フォルダ(と拡張子).
file = "C:/Users/okaji/Desktop/pro/delete/master3.wav"
# 出力フォルダ.
OUTPUT_DIR = "C:/Users/okaji/Desktop/pro/delete/"
# ビットレート.
BIT_RATE = "1411k"

cmd = [
    "ffmpeg",
    "-i",
    file,
    "-b:a",
    BIT_RATE,  # ビットレート.
    os.path.join(OUTPUT_DIR, os.path.basename(file)),  # outputフォルダに出力
]
print(cmd)
subprocess.run(cmd)

