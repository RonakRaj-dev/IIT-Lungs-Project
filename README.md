# 🫁 Multi-Label Chest X-Ray Diagnostic System

> An automated clinical decision-support system that detects **14 distinct lung pathologies** from chest X-rays using a **Teacher-Student active learning framework**. The system fuses deep-learning pixel features with clinical metadata (age, gender, X-ray view position) to deliver high-precision diagnostic insights — developed as an **IIT academic research project**.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C?logo=pytorch)](https://pytorch.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-Academic-green)](./LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Detected Pathologies](#-detected-pathologies)
- [How It Works](#-how-it-works)
- [Architecture](#-architecture)
- [Teacher-Student Framework](#-teacher-student-active-learning-framework)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [Prerequisites](#-prerequisites)
- [Setup & Installation](#-setup--installation)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [Model Training](#-model-training)
- [API Reference](#-api-reference)
- [Evaluation Metrics](#-evaluation-metrics)
- [Results](#-results)
- [Troubleshooting](#-troubleshooting)
- [Known Limitations](#-known-limitations)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

Chest X-rays are one of the most common and cost-effective diagnostic tools in medicine, but interpreting them accurately requires significant clinical expertise. This system addresses the challenge of:

- **Scale** — Large medical image datasets with limited expert annotations
- **Multi-label complexity** — A single X-ray can show multiple co-occurring pathologies
- **Clinical variability** — Patient age, gender, and imaging view position affect appearance

### Key Innovations

| Innovation | Description |
|---|---|
| 🎓 **Teacher-Student Learning** | A pre-trained "Teacher" model generates pseudo-labels for unlabeled X-rays, allowing the "Student" model to train on a much larger effective dataset |
| 🔬 **Feature Fusion** | Deep CNN pixel features are fused with structured clinical metadata for context-aware predictions |
| 🏷️ **14-Class Multi-Label Output** | Simultaneous detection of 14 pathologies with per-class confidence scores |
| 📉 **Active Learning Loop** | Iterative selection of the most informative unlabeled samples for expert annotation |

---

## 🫀 Detected Pathologies

The system classifies the following **14 thoracic pathologies** (based on the NIH ChestX-ray14 / CheXpert taxonomy):

| # | Pathology | # | Pathology |
|---|---|---|---|
| 1 | Atelectasis | 8 | Pleural Thickening |
| 2 | Cardiomegaly | 9 | Pneumonia |
| 3 | Effusion | 10 | Pneumothorax |
| 4 | Infiltration | 11 | Consolidation |
| 5 | Mass | 12 | Edema |
| 6 | Nodule | 13 | Emphysema |
| 7 | Pleural Effusion | 14 | Fibrosis |

> A chest X-ray can be labeled with **multiple pathologies simultaneously** (multi-label classification), or labeled as `No Finding` when no abnormality is detected.

---

## 🔄 How It Works

```
Raw Chest X-Ray (DICOM / PNG / JPG)
            │
            ▼
  ┌─────────────────────┐
  │   Preprocessing     │  ── Resize, Normalize, CLAHE Enhancement
  └─────────┬───────────┘
            │
            ▼
  ┌─────────────────────┐     ┌──────────────────────┐
  │   CNN Backbone      │     │  Clinical Metadata   │
  │  (DenseNet-121 /    │     │  - Patient Age       │
  │   ResNet-50)        │     │  - Gender            │
  │                     │     │  - View Position     │
  │  → Pixel Features   │     │    (PA / AP / LL)    │
  └─────────┬───────────┘     └──────────┬───────────┘
            │                            │
            └────────────┬───────────────┘
                         │  Feature Fusion
                         ▼
              ┌─────────────────────┐
              │  Fusion Network     │  ── Concat + FC Layers
              └─────────┬───────────┘
                        │
                        ▼
              ┌─────────────────────┐
              │  Multi-Label Head   │  ── 14 Sigmoid Outputs
              └─────────┬───────────┘
                        │
                        ▼
          Per-Pathology Confidence Scores
          (e.g., Pneumonia: 0.87, Effusion: 0.43)
```

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   CLIENT (React 18 + Vite)                  │
│                                                             │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  X-Ray Upload │  │  Prediction  │  │    Dashboard /   │  │
│  │  (DICOM/PNG)  │  │  Results UI  │  │  Session History │  │
│  └───────────────┘  └──────────────┘  └──────────────────┘  │
│              │              ▲                                │
│              │    Axios     │ JSON responses                 │
└──────────────┼──────────────┼────────────────────────────────┘
               │   HTTP/REST  │
┌──────────────▼──────────────┴────────────────────────────────┐
│                    SERVER (FastAPI)                          │
│                                                             │
│  ┌───────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │ POST /predict │  │  GET /sessions  │  │ POST /feedback│  │
│  │ (X-Ray infer) │  │  (History CRUD) │  │ (Active Learn)│  │
│  └───────┬───────┘  └────────┬────────┘  └───────┬───────┘  │
│          │                   │                    │          │
│  ┌───────▼───────────────────▼────────────────────▼───────┐  │
│  │               Model Inference Engine                   │  │
│  │   preprocess → feature extraction → fusion → predict  │  │
│  └───────────────────────────┬─────────────────────────── ┘  │
└──────────────────────────────┼──────────────────────────────┘
                               │
          ┌────────────────────┼─────────────────────┐
          │                    │                      │
┌─────────▼──────────┐ ┌───────▼────────┐ ┌──────────▼───────┐
│  Teacher Model     │ │ Student Model  │ │  Session / Label  │
│  (DenseNet-121     │ │ (Fine-tuned,   │ │  Storage          │
│   pre-trained)     │ │  active-learn) │ │  (JSON / MongoDB) │
│  Pseudo-labeler    │ │  Final Predict │ │                   │
└────────────────────┘ └────────────────┘ └──────────────────┘
```

### Layer Responsibilities

| Layer | Technology | Responsibility |
|---|---|---|
| **Frontend** | React 18, Tailwind CSS, Axios | Upload X-rays, display multi-label predictions, visualize heatmaps |
| **Backend** | FastAPI, Uvicorn, Pydantic | REST endpoints, image preprocessing, model orchestration |
| **Teacher Model** | PyTorch, DenseNet-121 | Generates pseudo-labels for unlabeled X-ray data |
| **Student Model** | PyTorch, ResNet/DenseNet | Final diagnostic model trained with active learning |
| **Feature Fusion** | PyTorch FC Layers | Combines CNN image features with clinical metadata |
| **Storage** | JSON / MongoDB | Persist prediction sessions, annotations, feedback |

---

## 🎓 Teacher-Student Active Learning Framework

The core methodological innovation of this project:

```
Phase 1 — Teacher Pre-training
──────────────────────────────
Large labeled dataset (e.g., NIH ChestX-ray14)
        │
        ▼
   Train Teacher Model (DenseNet-121)
        │
        ▼
   Teacher generates soft pseudo-labels
   for UNLABELED X-rays (confidence scores per class)


Phase 2 — Active Learning Loop
───────────────────────────────
Unlabeled Pool
        │
        ▼
  Teacher scores all unlabeled samples
        │
        ▼
  Uncertainty Sampling → select top-K most
  uncertain images for expert annotation
        │
        ▼
  Expert annotates selected K images
        │
        ▼
  Student Model retrains on:
  ├── Original labeled data
  ├── Expert-annotated K images
  └── High-confidence pseudo-labels
        │
        ▼
  Repeat until budget exhausted or
  performance converges


Phase 3 — Inference
─────────────────────
New X-Ray + Clinical Metadata
        │
        ▼
  Student Model → 14 sigmoid outputs
        │
        ▼
  Grad-CAM heatmap generation
  (shows which region triggered each pathology)
```

### Why Teacher-Student?

| Challenge | Solution |
|---|---|
| Limited expert annotations | Teacher pseudo-labels expand effective training set |
| Annotation cost | Active learning targets only the most informative images |
| Overfitting on small labeled set | Knowledge distillation from Teacher regularizes Student |
| Distribution shift | Iterative retraining adapts to new data distributions |

---

## 🛠 Tech Stack

### Deep Learning & ML
| Library | Version | Purpose |
|---|---|---|
| `torch` | 2.0+ | Core deep learning framework |
| `torchvision` | 0.15+ | Pretrained CNN backbones (DenseNet, ResNet) |
| `numpy` | 1.24+ | Array operations |
| `scikit-learn` | 1.3+ | Metrics (AUC-ROC, F1), data splitting |
| `albumentations` | 1.3+ | Medical image augmentation |
| `Pillow` / `pydicom` | latest | Image loading (PNG, DICOM) |
| `matplotlib` / `seaborn` | latest | Plotting, heatmaps |
| `grad-cam` | latest | Gradient-weighted Class Activation Maps |
| `pandas` | 2.0+ | Metadata handling (CSV labels, patient info) |

### Backend
| Library | Version | Purpose |
|---|---|---|
| `fastapi` | 0.100+ | REST API framework |
| `uvicorn` | latest | ASGI server |
| `pydantic` | v2 | Schema validation |
| `python-multipart` | latest | Image file upload |
| `python-dotenv` | latest | Environment variable management |
| `opencv-python` | 4.x | Image preprocessing, CLAHE enhancement |

### Frontend
| Package | Version | Purpose |
|---|---|---|
| `react` | 18.x | UI framework |
| `vite` | 4.x | Build tool and dev server |
| `tailwindcss` | 3.x | Utility-first styling |
| `axios` | latest | HTTP API client |
| `react-router-dom` | v6 | Client-side routing |
| `recharts` | latest | AUC/performance charts on Dashboard |

---

## 📁 Project Structure

```
IIT Project/
│
├── README.md
│
├── notebooks/                              # Jupyter notebooks for exploration
│   ├── 01_data_exploration.ipynb           # Dataset statistics, label distribution
│   ├── 02_teacher_training.ipynb           # Teacher model training walkthrough
│   ├── 03_active_learning_loop.ipynb       # Active learning experiment
│   └── 04_evaluation.ipynb                 # AUC-ROC curves, confusion matrices
│
├── src/                                    # Core ML source code
│   ├── models/
│   │   ├── teacher_model.py                # DenseNet-121 Teacher architecture
│   │   ├── student_model.py                # Student model with feature fusion
│   │   ├── fusion_network.py               # Metadata + CNN feature fusion layers
│   │   └── multi_label_head.py             # 14-class sigmoid output head
│   │
│   ├── training/
│   │   ├── train_teacher.py                # Teacher pre-training script
│   │   ├── train_student.py                # Student active learning training
│   │   ├── active_learning.py              # Uncertainty sampling strategies
│   │   └── loss_functions.py               # BCE, weighted loss for imbalance
│   │
│   ├── data/
│   │   ├── dataset.py                      # PyTorch Dataset class (ChestXray14)
│   │   ├── transforms.py                   # Augmentation pipelines
│   │   ├── metadata_encoder.py             # Age normalization, gender/view encoding
│   │   └── data_splits.py                  # Train/val/test split utilities
│   │
│   ├── evaluation/
│   │   ├── metrics.py                      # AUC-ROC, F1, precision, recall per class
│   │   ├── gradcam.py                      # Grad-CAM heatmap generation
│   │   └── visualize.py                    # Prediction visualization utilities
│   │
│   └── utils/
│       ├── config.py                       # Hyperparameters and config loader
│       ├── checkpoint.py                   # Save/load model checkpoints
│       └── logger.py                       # Training logging (TensorBoard / W&B)
│
├── backend/                                # FastAPI server
│   ├── main.py                             # App factory, CORS, router setup
│   ├── routes/
│   │   ├── predict.py                      # POST /predict — run inference
│   │   ├── sessions.py                     # GET|POST /sessions — history
│   │   └── feedback.py                     # POST /feedback — active learning input
│   ├── services/
│   │   ├── inference_service.py            # Load model, preprocess, predict
│   │   ├── gradcam_service.py              # Generate heatmap overlays
│   │   └── session_manager.py              # Persist prediction records
│   ├── models/
│   │   └── schemas.py                      # Pydantic request/response models
│   ├── checkpoints/                        # Saved .pth model weight files
│   ├── requirements.txt
│   └── .env
│
├── frontend/                               # React + Vite web application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── XRayUpload.jsx              # Drag-and-drop X-ray image uploader
│   │   │   ├── PredictionCard.jsx          # Per-pathology score display
│   │   │   ├── HeatmapViewer.jsx           # Grad-CAM overlay on X-ray
│   │   │   ├── MetadataForm.jsx            # Age, gender, view position inputs
│   │   │   └── SessionHistory.jsx          # Past prediction sessions list
│   │   ├── pages/
│   │   │   ├── Home.jsx                    # Landing and upload page
│   │   │   ├── Results.jsx                 # Prediction results and heatmap
│   │   │   └── Dashboard.jsx               # Analytics and session history
│   │   ├── services/
│   │   │   └── api.js                      # Axios API call definitions
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── configs/
│   ├── teacher_config.yaml                 # Teacher model hyperparameters
│   └── student_config.yaml                 # Student model hyperparameters
│
├── data/                                   # Data directory (not committed to git)
│   ├── raw/                                # Original NIH ChestX-ray14 images
│   ├── processed/                          # Preprocessed & resized images
│   └── labels/
│       ├── Data_Entry_2017.csv             # NIH official label file
│       └── train_val_test_split.csv        # Our data split
│
└── .gitignore
```

---

## 📦 Dataset

This project is designed to work with the **NIH ChestX-ray14** dataset:

| Property | Detail |
|---|---|
| **Name** | NIH ChestX-ray14 |
| **Source** | [NIH Clinical Center](https://nihcc.app.box.com/v/ChestXray-NIHCC) |
| **Images** | 112,120 frontal-view chest X-rays |
| **Patients** | 30,805 unique patients |
| **Labels** | 14 disease labels (multi-label, text-mined from reports) |
| **Metadata** | Patient age, gender, view position (PA/AP), follow-up number |
| **Format** | PNG (1024×1024), CSV label file |

### Download & Prepare Data

```bash
# Create data directories
mkdir -p data/raw data/processed data/labels

# Download the dataset (requires registration at NIH)
# Follow instructions at: https://nihcc.app.box.com/v/ChestXray-NIHCC

# After downloading, place images in data/raw/
# Place Data_Entry_2017.csv in data/labels/

# Run preprocessing script
python src/data/preprocess.py --input data/raw/ --output data/processed/ --size 224
```

---

## ✅ Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| **Python** | 3.10+ | [python.org](https://python.org) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org) |
| **CUDA** | 11.8+ | Required for GPU training (recommended) |
| **GPU VRAM** | 8GB+ | 12GB+ recommended for DenseNet-121 |
| **RAM** | 16GB+ | 32GB recommended for full dataset |
| **Disk Space** | ~50GB | NIH dataset (~42GB) + processed images |

> 💡 CPU-only inference is supported but significantly slower. GPU is **strongly recommended** for training.

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/chest-xray-diagnostic.git
cd "IIT Project"
```

### 2. Backend & ML Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

### 4. Configure `.gitignore`

```gitignore
# Environment files
backend/.env
frontend/.env

# Python
venv/
__pycache__/
*.pyc
*.pth          # Model checkpoints (large files — use Git LFS or cloud storage)

# Data (never commit patient data)
data/raw/
data/processed/
data/labels/

# Node
frontend/node_modules/
frontend/dist/

# Jupyter
.ipynb_checkpoints/

# Logs
*.log
runs/
wandb/
```

---

## 🔐 Environment Variables

### Backend — `backend/.env`

```env
# ── Model ─────────────────────────────────────────────
# Path to the trained Student model checkpoint
MODEL_CHECKPOINT_PATH=./checkpoints/student_best.pth

# Model backbone: densenet121 | resnet50 | resnet101
MODEL_BACKBONE=densenet121

# Input image size (must match training config)
IMAGE_SIZE=224

# Classification threshold per class (0.0–1.0)
PREDICTION_THRESHOLD=0.5

# ── Server ────────────────────────────────────────────
HOST=0.0.0.0
PORT=8000
DEBUG=False

# ── CORS ──────────────────────────────────────────────
ALLOWED_ORIGINS=http://localhost:5173

# ── Storage ───────────────────────────────────────────
STORAGE_TYPE=json
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=chest_xray_diagnostic
```

### Frontend — `frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## ▶️ Running the Application

### Terminal 1 — Backend

```bash
cd backend
venv\Scripts\activate         # Windows
source venv/bin/activate      # macOS / Linux

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

| URL | Description |
|---|---|
| `http://localhost:8000` | API root |
| `http://localhost:8000/docs` | Swagger interactive docs |
| `http://localhost:8000/redoc` | ReDoc documentation |

### Terminal 2 — Frontend

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## 🏋️ Model Training

### Step 1 — Train the Teacher Model

```bash
cd src/training

python train_teacher.py \
  --config ../../configs/teacher_config.yaml \
  --data_dir ../../data/processed \
  --labels_csv ../../data/labels/Data_Entry_2017.csv \
  --output_dir ../../backend/checkpoints \
  --epochs 30 \
  --batch_size 32 \
  --lr 1e-4
```

### Step 2 — Run Active Learning with Student Model

```bash
python train_student.py \
  --config ../../configs/student_config.yaml \
  --teacher_checkpoint ../../backend/checkpoints/teacher_best.pth \
  --data_dir ../../data/processed \
  --labels_csv ../../data/labels/Data_Entry_2017.csv \
  --output_dir ../../backend/checkpoints \
  --active_learning_rounds 5 \
  --queries_per_round 500 \
  --uncertainty_strategy entropy
```

### Uncertainty Sampling Strategies

| Strategy | Flag | Description |
|---|---|---|
| **Entropy** | `entropy` | Select samples with highest prediction entropy |
| **Least Confident** | `least_confident` | Select samples where max class score is lowest |
| **Margin Sampling** | `margin` | Select samples where top-2 class scores are closest |
| **Random Baseline** | `random` | Random selection (baseline comparison) |

### Training Configuration (`configs/student_config.yaml`)

```yaml
model:
  backbone: densenet121
  pretrained: true
  num_classes: 14
  metadata_dim: 4           # age, gender (binary), view_PA, view_AP

training:
  epochs: 50
  batch_size: 32
  learning_rate: 0.0001
  weight_decay: 0.0001
  scheduler: cosine
  
  # Class imbalance handling
  pos_weight_scale: 2.0     # Upweight positive (disease) samples

active_learning:
  rounds: 5
  queries_per_round: 500
  strategy: entropy

augmentation:
  random_horizontal_flip: true
  random_rotation: 10
  color_jitter: true
  clahe: true               # Medical imaging contrast enhancement
```

---

## 📡 API Reference

### Base URL: `http://localhost:8000`

---

#### `POST /predict` — Run Diagnosis on Chest X-Ray

```
Content-Type: multipart/form-data

Body:
  - file: <image file — PNG, JPG, or DICOM>
  - age: 45                        (integer, required)
  - gender: M                      (M | F, required)
  - view_position: PA              (PA | AP | LL, required)
```

**Response:**
```json
{
  "prediction_id": "uuid-...",
  "timestamp": "2024-01-15T10:30:00",
  "pathologies": {
    "Atelectasis":         { "score": 0.73, "positive": true  },
    "Cardiomegaly":        { "score": 0.12, "positive": false },
    "Effusion":            { "score": 0.89, "positive": true  },
    "Infiltration":        { "score": 0.45, "positive": false },
    "Mass":                { "score": 0.08, "positive": false },
    "Nodule":              { "score": 0.31, "positive": false },
    "Pneumonia":           { "score": 0.67, "positive": true  },
    "Pneumothorax":        { "score": 0.04, "positive": false },
    "Consolidation":       { "score": 0.55, "positive": true  },
    "Edema":               { "score": 0.22, "positive": false },
    "Emphysema":           { "score": 0.09, "positive": false },
    "Fibrosis":            { "score": 0.15, "positive": false },
    "Pleural Thickening":  { "score": 0.38, "positive": false },
    "No Finding":          { "score": 0.03, "positive": false }
  },
  "heatmap_url": "/heatmaps/uuid-....png",
  "model_version": "student_v3"
}
```

---

#### `GET /predict/{prediction_id}/heatmap` — Get Grad-CAM Heatmap

```
Returns: image/png — Grad-CAM overlay on original X-ray
Query param: pathology=Pneumonia  (which class to visualize)
```

---

#### `GET /sessions` — Get All Prediction Sessions

**Response:**
```json
{
  "sessions": [
    {
      "prediction_id": "uuid-...",
      "timestamp": "2024-01-15T10:30:00",
      "positive_findings": ["Effusion", "Pneumonia", "Atelectasis"],
      "top_score": 0.89,
      "metadata": { "age": 45, "gender": "M", "view_position": "PA" }
    }
  ]
}
```

---

#### `POST /feedback` — Submit Expert Annotation (Active Learning)

```json
{
  "prediction_id": "uuid-...",
  "expert_labels": {
    "Atelectasis": true,
    "Effusion": true,
    "Pneumonia": false
  },
  "annotator_id": "radiologist_01",
  "notes": "Mild atelectasis in right lower lobe"
}
```

---

## 📊 Evaluation Metrics

The system is evaluated using standard medical imaging benchmarks:

| Metric | Description |
|---|---|
| **AUC-ROC** | Area Under the ROC Curve per pathology (primary metric) |
| **Mean AUC** | Average AUC across all 14 classes |
| **F1 Score** | Harmonic mean of precision and recall per class |
| **Precision / Recall** | At threshold 0.5 per class |
| **Hamming Loss** | Fraction of incorrectly predicted labels |

### Run Evaluation

```bash
python src/evaluation/metrics.py \
  --checkpoint backend/checkpoints/student_best.pth \
  --test_csv data/labels/test_split.csv \
  --data_dir data/processed \
  --output_dir results/
```

---

## 📈 Results

Expected performance benchmarks on NIH ChestX-ray14 test set:

| Pathology | AUC-ROC |
|---|---|
| Atelectasis | ~0.81 |
| Cardiomegaly | ~0.90 |
| Effusion | ~0.88 |
| Infiltration | ~0.72 |
| Mass | ~0.86 |
| Nodule | ~0.78 |
| Pneumonia | ~0.77 |
| Pneumothorax | ~0.89 |
| Consolidation | ~0.79 |
| Edema | ~0.88 |
| Emphysema | ~0.92 |
| Fibrosis | ~0.83 |
| Pleural Thickening | ~0.80 |
| **Mean AUC** | **~0.84** |

> 📌 Actual results may vary based on hardware, random seed, and training duration.

---

## 🐛 Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| `CUDA out of memory` | Batch size too large for GPU | Reduce `batch_size` in config to 16 or 8 |
| `FileNotFoundError` on images | Wrong data path | Verify `data_dir` points to `data/processed/` |
| Model returns all zeros | Threshold too high | Lower `PREDICTION_THRESHOLD` to 0.3 in `.env` |
| DICOM images not loading | `pydicom` not installed | Run `pip install pydicom` |
| CORS error in browser | Origin mismatch | Add `http://localhost:5173` to `ALLOWED_ORIGINS` in `backend/.env` |
| `ModuleNotFoundError` | Venv not activated | Run `venv\Scripts\activate` then retry |
| Heatmap all black | Wrong target layer | Check `gradcam_service.py` target layer matches your backbone |
| Training loss NaN | Learning rate too high | Reduce `learning_rate` to `1e-5` |

---

## ⚠️ Known Limitations

- **Not a medical device** — This system is a **research prototype** and must not be used for clinical diagnosis without regulatory approval
- **NIH label noise** — ChestX-ray14 labels are NLP-mined from radiology reports and contain ~10–20% noise
- **No lateral view training** — The model is primarily trained on PA/AP views; lateral (LL) view performance may be lower
- **Population bias** — Trained on NIH dataset demographics; may not generalize equally to all populations
- **Single institution data** — Generalizing to X-rays from different scanners/hospitals may require domain adaptation

---

## 🤝 Contributing

1. **Fork** this repository
2. **Create a branch**: `git checkout -b feature/your-feature`
3. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: add CheXpert dataset support
   fix: correct AUC calculation for negative-only batches
   docs: add training configuration explanation
   ```
4. **Push**: `git push origin feature/your-feature`
5. **Open a Pull Request** with a clear description

---

## 📄 License

This project was developed as part of an **IIT academic research project**.  
For academic or research use, please cite this work appropriately.

> ⚠️ **Medical Disclaimer:** This system is intended for **research purposes only**. It is not approved for clinical use and should not be used as a substitute for professional medical diagnosis.

---

## 👥 Authors

- **Team IIT** — Research design, model development, backend API, and frontend interface

---

> 💡 **Quick Start Tip:** If you just want to test inference without training, download a pre-trained checkpoint from the releases page and place it in `backend/checkpoints/student_best.pth`, then run the backend server directly.
