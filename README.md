# 11 — DGA Domain Detector

Detect **Domain Generation Algorithm (DGA)** style domains using lexical features and a classical ML classifier — a popular threat-hunting building block.

## Why this is useful

Malware families often generate pseudo-random domains for C2. Lexical detectors are fast, explainable, and easy to demo on GitHub.

## Layout

```
11-dga-domain-detector/
├── generate_domains.py
├── train_dga_detector.py
├── data/domains.csv
└── outputs/
```

## Run

```bash
pip install -r requirements.txt
python generate_domains.py
python train_dga_detector.py
```

## Sample outputs

- `outputs/metrics.json`
- `outputs/top_dga_scores.csv`
- `outputs/feature_importance.csv`
