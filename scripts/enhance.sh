set -e

IN_DIR="/Users/adeebsmac/SLAM_PROJECT/datasets/extreme"
OUT_DIR="/Users/adeebsmac/SLAM_PROJECT/enhanced/extreme"

DOCKER_IMG="adeebali521/lowlight-denoise-enhancer:latest"

mkdir -p "$OUT_DIR"

if [ -d "$IN_DIR" ]; then
    echo "========================================================="
    echo "🚀 Launching Single Batch Container for Moderate Dataset"
    echo "   Input  -> $IN_DIR"
    echo "   Output -> $OUT_DIR"
    echo "========================================================="
    
    docker run --rm \
      -v "$IN_DIR:/input" \
      -v "$OUT_DIR:/output" \
      $DOCKER_IMG \
      --input /input \
      --output /output \
      --max-size 520

    echo "[+] Batch processing for moderate dataset complete!"
else
    echo "❌ Error: Input directory not found at $IN_DIR"
    exit 1
fi