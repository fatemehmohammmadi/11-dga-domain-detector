"""Generate synthetic legit vs DGA-like domains."""

from __future__ import annotations

import string
from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(101)
OUT = Path(__file__).parent / "data" / "domains.csv"

LEGIT = [
    "google.com", "github.com", "microsoft.com", "amazon.com", "cloudflare.com",
    "wikipedia.org", "linkedin.com", "stackoverflow.com", "openai.com", "python.org",
    "nytimes.com", "bbc.co.uk", "reddit.com", "apple.com", "netflix.com",
]


def random_dga(n: int = 12) -> str:
    alphabet = string.ascii_lowercase + string.digits
    label = "".join(RNG.choice(list(alphabet), size=n))
    tld = RNG.choice(["xyz", "top", "info", "biz", "ru", "cn"])
    return f"{label}.{tld}"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = [{"domain": d, "label": "legit"} for d in LEGIT for _ in range(20)]
    rows += [{"domain": random_dga(int(RNG.integers(10, 20))), "label": "dga"} for _ in range(400)]
    # mild legit-looking generated names
    for w in ["mail", "shop", "news", "blog", "docs", "cdn", "api", "portal"]:
        for _ in range(15):
            rows.append({"domain": f"{w}{RNG.integers(1,99)}.{RNG.choice(['com','net','org'])}", "label": "legit"})
    df = pd.DataFrame(rows).sample(frac=1.0, random_state=101).reset_index(drop=True)
    df.to_csv(OUT, index=False)
    print(f"Wrote {len(df)} domains -> {OUT}")


if __name__ == "__main__":
    main()
