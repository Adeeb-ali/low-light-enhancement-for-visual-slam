import cv2
import os
import glob
import sys

dataset = sys.argv[1]

INPUT_DIR = f"enhanced/{dataset}"
OUTPUT_DIR = f"slam_ready/{dataset}"

os.makedirs(OUTPUT_DIR, exist_ok=True)

images = sorted(
    glob.glob(
        os.path.join(INPUT_DIR, "*.jpg")
    )
)

print("Found", len(images), "images")

for i, img_path in enumerate(images):

    img = cv2.imread(img_path)

    if img is None:
        continue

    resized = cv2.resize(
        img,
        (752, 480),
        interpolation=cv2.INTER_CUBIC
    )

    save_path = os.path.join(
        OUTPUT_DIR,
        os.path.basename(img_path)
    )

    cv2.imwrite(save_path, resized)

    if i % 100 == 0:
        print(
            f"Processed {i}/{len(images)}"
        )

print("\nDone")
print("Output:", OUTPUT_DIR)