# Low-Light Image Enhancement for Visual SLAM

## Overview

This repository presents a custom deep-learning-based low-light image enhancement pipeline specifically engineered to stabilize and improve **Visual SLAM** performance under challenging illumination conditions.

By applying our enhancement model to degraded video sequences, we drastically increase the reliability of **ORB-SLAM3** across key robotic vision metrics:

* Image brightness normalization
* ORB feature extraction density
* Robust frame-to-frame feature matching
* Successful map initialization
* Continuous camera tracking (preventing tracking loss)
* Valid keyframe trajectory generation

The project quantitatively demonstrates that targeted image enhancement can rescue SLAM pipelines from complete failure on low-light sequences, enabling reliable localization where standard methods fail.

---

## Project Structure

```text
SLAM_PROJECT/
├── datasets/             # Raw input image sequences
│   ├── daylight/
│   ├── moderate/
│   └── extreme/
├── enhanced/             # Outputs from the enhancement model
│   ├── daylight/
│   ├── moderate/
│   └── extreme/
├── results/              # Parsed evaluation metrics & trajectories
│   ├── daylight/
│   ├── moderate/
│   └── extreme/
├── scripts/              # Automation and preprocessing utilities
│   ├── generate_rgb.py   # Generates ORB-SLAM3 timestamp files
│   ├── resize_images.py  # Standardizes input resolution
│   ├── enhance.sh        # Batch processing enhancement script
│   └── run_slam.sh       # Automation for Docker SLAM execution
├── requirements.txt      # Python dependencies
└── README.md             # Project overview and benchmarks

```

---

## Environment Setup

### 1. Prerequisites

The Python environment handles preprocessing and image enhancement. It was developed and tested using **Python 3.10**.

```bash
python3 --version

```

### 2. Virtual Environment Setup

Initialize and activate an isolated environment:

* **Linux / macOS:**
```bash
python3.10 -m venv venv
source venv/bin/activate

```


* **Windows:**
```bash
python3.10 -m venv venv
venv\Scripts\activate

```



### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

---

## Input Requirements & Dataset Preparation

### Input Requirements

* **Naming Format:** `frame_000000.jpg`, `frame_000001.jpg`, `frame_000002.jpg`, ...
* **Sequence Length:** Minimum 100+ frames required; **300+ frames recommended** for stable SLAM evaluation and trajectory looping.

### Preparation Pipeline

Before running the evaluation, format the datasets to match the expected sensor specifications:

1. **Resize Images:** Standardize the input sequences to a standard evaluation resolution (**752 × 480**):
```bash
python3 scripts/resize_images.py

```


2. **Generate Association File:** ORB-SLAM3 requires timestamps linked to each image. Generate the expected `rgb.txt` file using:
```bash
python3 scripts/generate_rgb.py <dataset_directory>

```


*Output format:*
```text
0.000000 frame_000000.jpg
0.050000 frame_000001.jpg

```



---

## Docker Environment

To isolate dependencies and ensure absolute portability, ORB-SLAM3 runs inside a pre-configured Docker container.

```bash
# Pull the evaluation image
docker pull adeebali521/orbslam3:latest

# Spin up and enter the environment
docker run -it --name orbslam3_work adeebali521/orbslam3:latest bash

# Operational lifecycle commands for later sessions:
docker start orbslam3_work
docker exec -it orbslam3_work bash

```

> [!NOTE]
> For a deep dive into container optimization, custom dataset mounting, and structural configuration details, please refer to the explicit **[SLAM_EVALUATION.md](https://www.google.com/search?q=SLAM_EVALUATION.md)**.

---

## ORB-SLAM3 Evaluation Workflow

Execute the evaluation workflow by passing data across the host/container bridge:

```bash
# 1. Copy raw and enhanced datasets into the container environment
docker cp datasets/extreme/. orbslam3_work:/workspace/extreme_raw/
docker cp enhanced/extreme/. orbslam3_work:/workspace/extreme_enhanced/

# 2. Inside the Docker container, clear old states and launch the SLAM node
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
cd ~/ORB_SLAM3
rm -f KeyFrameTrajectory.txt

./Examples/Monocular/mono_tum Vocabulary/ORBvoc.txt Examples/Monocular/TUM1.yaml /workspace/extreme_enhanced

```

---

## Benchmark Results

### 1. Daylight Dataset (Baseline)

| Metric | Without Model (Raw) | With Model (Enhanced) | Status / Impact |
| --- | --- | --- | --- |
| **Brightness Avg** | 5.76 | 77.71 | Enhanced Exposure |
| **ORB Features Avg** | 715.39 | 1000.00 | Frame Saturation Reached |
| **ORB Matches Avg** | 596.80 | 787.80 | Enhanced Tracking Consistency |
| **Map Created** | **Yes** | **Yes** | System Stable |
| **Tracking** | **Yes** | **Yes** | System Stable |

### 2. Moderate Low-Light Dataset

| Metric | Without Model (Raw) | With Model (Enhanced) | Status / Impact |
| --- | --- | --- | --- |
| **Brightness Avg** | 1.59 | 86.89 | **54.6× Brightness Boost** |
| **ORB Features Avg** | 24.27 | 261.35 | Massive Feature Recovery |
| **ORB Matches Avg** | 68.07 | 95.24 | Consistency Restored |
| **Map Created** | **No** | **Yes** | **Map Initialization Rescued** |
| **Map Points** | 0 | 81 | Map Populated |
| **Tracking** | **Failed** | **Partial** | Substantial Longevity Gain |

### 3. Extreme Low-Light Dataset

| Metric | Without Model (Raw) | With Model (Enhanced) | Status / Impact |
| --- | --- | --- | --- |
| **Brightness Avg** | 18.26 | 97.94 | Clear Structure Recovery |
| **ORB Features Avg** | 39.53 | 851.38 | **21.5× Keypoint Increase** |
| **ORB Matches Avg** | 25.98 | 499.09 | **19.2× Match Reliability** |
| **Map Created** | **No** | **Yes** | Initialization Enabled |
| **Map Points** | 0 | 77 | Map Populated |
| **Tracking** | **Failed** | **Success** | **Full Tracking Restored** |
| **Trajectory Generated** | **No** | **Yes** | Complete Path Exported |
| **Trajectory Entries** | 0 | 58 | 58 Camera Poses Resolved |

---

## Key Findings

* **Brightness Scaling:** Maximum observed optimization reached a **54.6× increase** on the Moderate Dataset, restoring contrast to underexposed structural boundaries.
* **Feature Extraction Boost:** Achieved up to a **21.5× increase** in usable keypoint tracking points on the Extreme Dataset.
* **The Definitive Result:** On the *Extreme Low-Light Dataset*, raw images triggered instantaneous tracking loss ($0$ map points, $0$ trajectory entries). Passing those exact frames through our enhancement model allowed ORB-SLAM3 to successfully initialize, map local spatial boundaries, sustain tracking, and resolve a valid **58-pose camera trajectory**.

---

## Results Directory Structure

All benchmark run metrics are saved locally under the `results/` path for post-analysis:

```text
results/<dataset_type>/
├── brightness_features.csv  # Combined brightness vs feature correlation matrix
├── orb_matches.csv          # Sequence step tracking logs
├── slam_summary.txt         # Loop closure and map metrics summary
├── KeyFrameTrajectory.txt   # Final estimated camera trajectory coordinates
└── images/
    ├── sample.jpg           # Reference video frame
    └── orb_features.jpg     # Rendered keypoints overlay visualization

```

---

## Real-World Applications

This pipeline directly addresses critical operational bottlenecks in fields including:

* **Autonomous Robots & AGVs:** Safe indoor navigation during facility blackouts or variable lighting.
* **UAV Inspection Mapping:** Nighttime infrastructure evaluation and low-altitude reconnaissance.
* **Search and Rescue Robotics:** Reliable tracking through smoke-degraded or unlit environments.
* **Embedded Vision Systems:** Optimization targeted for low-power edge deployment (FPGA / Jetson architecture).

---

## Author

**Adeeb Ali** *B.Tech in Electronics and Communication Engineering* **Core Technical Focus Areas:** * Computer Vision & Pattern Recognition

* Robust Visual SLAM Exploration
* FPGA Acceleration & Embedded AI Architectures
* Autonomous Robotics Systems
* Deep Machine Learning Systems
