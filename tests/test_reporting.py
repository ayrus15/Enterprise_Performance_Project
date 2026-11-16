from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "financial"


def test_reporting_outputs_reconcile_to_the_portfolio_and_action_tracker():
    portfolio = pd.read_csv(OUT / "portfolio_financials.csv")
    summary = pd.read_csv(OUT / "financial_summary.csv").set_index("Metric").Value
    actions = pd.read_csv(OUT / "action_tracker.csv")
    exceptions = pd.read_csv(OUT / "financial_exceptions.csv")
    assert portfolio.ApprovedBudget.sum() == summary["Total approved budget"]
    assert portfolio.ForecastExpenditure.sum() == summary["Total forecast expenditure"]
    assert len(exceptions) == summary["Red forecast exceptions"] == 5
    overdue = actions.loc[actions.Overdue.astype(str).str.lower() == "true", "ActionID"].tolist()
    assert overdue == ["ACT-001", "ACT-002", "ACT-004", "ACT-005"]


def test_executive_deck_is_six_slides_and_contains_correct_overdue_actions():
    from pptx import Presentation
    deck = Presentation(ROOT / "presentation" / "Financial_Portfolio_Executive_Review.pptx")
    assert len(deck.slides) == 6
    text_parts = []
    for shape in deck.slides[4].shapes:
        if hasattr(shape, "text"):
            text_parts.append(shape.text)
        if getattr(shape, "has_table", False):
            text_parts.extend(cell.text for row in shape.table.rows for cell in row.cells)
    slide_text = " ".join(text_parts)
    assert "ACT-005" in slide_text
    assert "ACT-003" not in slide_text
