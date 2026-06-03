#!/bin/bash

DATASET=$1

echo "Enhancement..."
bash scripts/enhance.sh $DATASET

echo "Resize..."
python scripts/resize_images.py $DATASET

echo "RGB..."
python scripts/generate_rgb.py $DATASET

echo "Done."