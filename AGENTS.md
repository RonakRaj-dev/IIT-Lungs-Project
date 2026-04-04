# AGENTS.md

## What this repo *actually* is
- Despite `README.md` describing a React/FastAPI “interview prep platform”, the checked-in code is a **Python data + CV/ML workspace** for NIH Chest X-ray processing, bounding-box auditing, and model training/inference.
- Primary working areas:
  - `utils/`: one-off but *runnable* scripts for dataset prep/auditing/training/inference.
  - `Datasets/`: downloaded datasets + metadata (`*.csv`), annotations (`annotated/`), and model artifacts (`*.pth`, `*.pkl`, `*.h5`, `*.npy`).
  - `DataProcessing/*.ipynb`: phase notebooks for analysis/experiments.

## Data flow / pipelines (follow these files)
- Download dataset (Kaggle): `Datasets/dataRetrieving.py` uses `kagglehub.dataset_download("nih-chest-xrays/data")` and sets `KAGGLEHUB_CACHE`.
- Prepare 512x512 images from NIH 1024px originals:
  - `utils/BBOX_512.py` scans NIH folders, then resizes images to `Datasets/datasets/bbox_resized_512`.
- Audit bounding boxes interactively (human-in-the-loop):
  - `utils/BBOX_VALIDATION.py` renders boxes from `BBox_Final.csv`, then copies images into `Datasets/datasets/bbox_audited/{Correct,Re-annotate,Garbage}`.
- Train “heavy teacher” model (DenseNet121, multi-label + bbox regression):
  - `utils/BBOX_MODEL_CODE.py` loads audited `Correct/` images + `utils/updated_annotations.csv`, trains, and saves `heavy_teacher_final.h5`.
- Run inference + verified sorting:
  - `utils/BBOX_EXE.py` loads `heavy_teacher_final.h5`, predicts `[class_out, bbox_out]`, computes IoU vs reference boxes, and copies images into `Sorted_Results/{Identified,Unidentified}` plus `verification_log.csv`.
- Merge member COCO-style annotations back into a master training CSV:
  - `utils/update_coco_from_csv.py` reads per-member `Datasets/annotated/*/annotation.coco`, unions labels, one-hot encodes pathologies, and writes `train_final_updated.csv`.

## Project-specific conventions (important)
- Many scripts hard-code **absolute Windows paths** (e.g., `C:\Users\gamer\OneDrive\Desktop\IIT Project\...`). When editing/adding scripts, prefer:
  - a `PROJECT_ROOT = Path(__file__).resolve().parents[1]` pattern, and/or
  - CLI args for input/output roots (so others can run without editing source).
- Image/bbox coordinate convention:
  - Original imagery assumed `1024x1024`; scripts normalize boxes as `[x,y,w,h] / 1024` (see `BBOX_EXE.py`, `BBOX_MODEL_CODE.py`).
  - Resized imagery typically `512x512` (see `BBOX_512.py`, `BBOX_VALIDATION.py`).
- CSV schema expectations are implicit and critical:
  - Must include `Image Index`; bbox CSVs include `x,y,w,h`; label CSVs may include multi-hot columns for pathologies (see `update_coco_from_csv.py`).

## Developer workflow (PowerShell)
```powershell
# from repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # NOTE: currently empty; install based on imports

# common scripts
python .\Datasets\dataRetrieving.py
python .\utils\BBOX_512.py
python .\utils\BBOX_VALIDATION.py   # interactive
python .\utils\BBOX_MODEL_CODE.py   # training (TensorFlow)
python .\utils\BBOX_EXE.py
python .\utils\update_coco_from_csv.py
```

## External dependencies / integration points
- Data download: `kagglehub` (requires Kaggle auth configured for your environment).
- ML stack is mixed:
  - TensorFlow/Keras (`*.h5` model) in bbox teacher scripts.
  - PyTorch + scikit-learn artifacts exist under `Datasets/mce_models*/` (`*.pth`, `*.pkl`, `*.npy`).
- Visualization/interactivity: `matplotlib` with `plt.ion()` + `input()` loops (see `BBOX_VALIDATION.py`).

## Where to look first when making changes
- If changing bbox logic/metrics: start from `utils/BBOX_EXE.py` (IoU + thresholds).
- If changing label sets / one-hot encoding: start from `utils/update_coco_from_csv.py` (`PATHOLOGIES`, `MINORITY_CLASSES`).
- If portability is required: remove absolute paths in `utils/*.py` and `Datasets/dataRetrieving.py`.

