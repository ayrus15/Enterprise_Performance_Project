"""Prepare compact workbook inputs from verified pipeline outputs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_PACKAGES = ROOT / ".python_packages"
if LOCAL_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_PACKAGES))

import pandas as pd

OUT = ROOT / "outputs" / "reports" / "workbook_data.json"


def records(path: Path, limit: int | None = None) -> list[list[object]]:
    frame = pd.read_csv(path, nrows=limit)
    return [frame.columns.tolist()] + frame.fillna("").values.tolist()


def main() -> None:
    raw = pd.read_excel(ROOT / "data" / "raw" / "Online Retail.xlsx", engine="calamine", nrows=100, dtype={"InvoiceNo": "string", "StockCode": "string"})
    inputs = {
        "rawTransactions": [raw.columns.tolist()] + raw.fillna("").values.tolist(),
        "cleanTransactions": records(ROOT / "outputs" / "processed" / "clean_transactions.csv", 100),
        "monthlySales": records(ROOT / "outputs" / "processed" / "monthly_sales.csv"),
        "countries": records(ROOT / "outputs" / "processed" / "country_contribution.csv", 12),
        "products": records(ROOT / "outputs" / "processed" / "top_products.csv", 12),
        "customers": records(ROOT / "outputs" / "processed" / "top_customers.csv", 12),
        "completeness": records(ROOT / "outputs" / "processed" / "data_completeness.csv"),
        "kpis": records(ROOT / "outputs" / "processed" / "kpi_summary.csv"),
        "portfolio": records(ROOT / "outputs" / "processed" / "project_portfolio.csv"),
        "milestones": records(ROOT / "outputs" / "processed" / "milestones.csv"),
        "risks": records(ROOT / "outputs" / "processed" / "risks_actions.csv"),
        "qa": records(ROOT / "outputs" / "qa" / "qa_reconciliation.csv"),
        "runLog": records(ROOT / "outputs" / "qa" / "run_log.csv"),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(inputs, default=str), encoding="utf-8")
    print(f"Prepared workbook inputs: {OUT}")


if __name__ == "__main__":
    main()
