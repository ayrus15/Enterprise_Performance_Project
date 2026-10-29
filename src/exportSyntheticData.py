"""Write a static, committed snapshot of the synthetic portfolio to data/synthetic/.

The portfolio itself is defined once in runPipeline.makePortfolio(); this
script only exports that same definition so a reviewer can see the synthetic
source data without having to run the full transaction pipeline.
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from runPipeline import loadConfig, makePortfolio  # noqa: E402


def export() -> None:
    cfg = loadConfig()
    portfolio, milestones, records = makePortfolio(pd.Timestamp(cfg["reporting_date"]))
    out = ROOT / "data" / "synthetic"
    out.mkdir(parents=True, exist_ok=True)
    portfolio.to_csv(out / "projects.csv", index=False)
    milestones.to_csv(out / "milestones.csv", index=False)
    records[records.RecordType == "Risk"].to_csv(out / "risks.csv", index=False)
    records[records.RecordType != "Risk"].to_csv(out / "actions.csv", index=False)
    print(
        f"Exported {len(portfolio)} projects, {len(milestones)} milestones, "
        f"{(records.RecordType == 'Risk').sum()} risks, "
        f"{(records.RecordType != 'Risk').sum()} actions to {out}"
    )


if __name__ == "__main__":
    export()
