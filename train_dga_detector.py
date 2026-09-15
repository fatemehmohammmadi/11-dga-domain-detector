"""Train a lexical DGA domain detector."""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split

DATA = Path(__file__).parent / "data" / "domains.csv"
OUT = Path(__file__).parent / "outputs"


def entropy(s: str) -> float:
    if not s:
        return 0.0
    c = Counter(s)
    n = len(s)
    return -sum((v / n) * math.log2(v / n) for v in c.values())


def feats(domain: str) -> dict:
    # mostly look at the left-most label; TLD alone isn't very discriminative here
    host = domain.split(".")[0]
    return {
        "length": len(domain),
        "label_length": len(host),
        "digit_ratio": sum(ch.isdigit() for ch in host) / max(len(host), 1),
        # DGA strings are often light on vowels
        "vowel_ratio": sum(ch in "aeiou" for ch in host.lower()) / max(len(host), 1),
        "unique_char_ratio": len(set(host.lower())) / max(len(host), 1),
        "entropy": entropy(host.lower()),
        "hyphen_count": host.count("-"),
        "digit_count": sum(ch.isdigit() for ch in host),
    }


def main() -> None:
    if not DATA.exists():
        raise SystemExit("Run generate_domains.py first.")
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    X = pd.DataFrame([feats(d) for d in df["domain"]])
    y = df["label"]
    X_train, X_test, y_train, y_test, d_train, d_test = train_test_split(
        X, y, df["domain"], test_size=0.25, random_state=42, stratify=y
    )
    clf = RandomForestClassifier(n_estimators=300, random_state=42)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    report = classification_report(y_test, pred, digits=3)
    metrics = {"f1_macro": round(float(f1_score(y_test, pred, average="macro")), 4), "n": int(len(df)), "report": report}
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    proba = clf.predict_proba(X_test)[:, list(clf.classes_).index("dga")]
    pd.DataFrame({"domain": d_test.values, "dga_proba": proba, "true": y_test.values}).sort_values(
        "dga_proba", ascending=False
    ).head(25).to_csv(OUT / "top_dga_scores.csv", index=False)
    pd.DataFrame({"feature": X.columns, "importance": clf.feature_importances_}).sort_values(
        "importance", ascending=False
    ).to_csv(OUT / "feature_importance.csv", index=False)
    print(json.dumps({"f1_macro": metrics["f1_macro"], "n": metrics["n"]}, indent=2))
    print(report)


if __name__ == "__main__":
    main()
