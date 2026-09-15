# DGA Domain Detector

Lexical detector for Domain Generation Algorithm style names (high entropy, weird length, odd TLDs, etc.).

I use this pattern a lot in DNS hunting: cheap features, fast model, easy to explain to an analyst.

## Run

```bash
pip install -r requirements.txt
python generate_domains.py
python train_dga_detector.py
```

## Features

- domain / label length
- digit ratio, vowel ratio, unique-char ratio
- Shannon entropy on the left-most label
- hyphen + digit counts

## Outputs

`outputs/metrics.json`, `outputs/top_dga_scores.csv`, `outputs/feature_importance.csv`

## Limits

Won't catch word-based DGAs that look like real brand tokens. Pair with NXDOMAIN rates and newly observed domains in production.

## License

MIT
