import os
import sys

folder = sys.argv[1]

files = sorted([
    f for f in os.listdir(folder)
    if f.endswith(".jpg")
])

with open(
    os.path.join(folder, "rgb.txt"),
    "w"
) as f:

    for i, name in enumerate(files):
        f.write(
            f"{i*0.05:.6f} {name}\n"
        )

print("Created", len(files), "entries")
print("Saved:", os.path.join(folder, "rgb.txt"))