"""Controlled reporting pipeline for the synthetic financial portfolio.

Raw files are read-only inputs. All outputs are regenerated in outputs/financial.
Positive financial variance always denotes additional cost versus approved budget.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "financial_raw", ROOT / "outputs" / "financial"
SETTINGS = json.loads((ROOT / "config" / "settings.json").read_text(encoding="utf-8"))
REPORTING_DATE = pd.Timestamp(SETTINGS["reporting_date"])

PROGRAMME_COLUMNS = ["ProgrammeID", "ProgrammeName", "BusinessUnit", "ProgrammeOwner", "StartDate", "EndDate", "DeliveryStatus", "RiskRating"]
FINANCIAL_COLUMNS = ["ProgrammeID", "ApprovedBudget", "ActualExpenditure", "ForecastExpenditure", "PreviousForecast", "ReportingPeriod"]
RISK_COLUMNS = ["RiskID", "RecordType", "ProgrammeID", "RiskDescription", "Owner", "TargetDate", "Status", "Likelihood", "Impact"]
ACTION_COLUMNS = ["ActionID", "ProgrammeID", "ActionDescription", "ActionOwner", "Priority", "DueDate", "Status", "EscalationRequired"]


def read_source(name: str, required: list[str], base: Path = RAW) -> pd.DataFrame:
    """Read a required non-empty CSV, failing before reporting if its shape is invalid."""
    frame = pd.read_csv(base / name)
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"{name} is missing required columns: {', '.join(missing)}")
    if frame.empty:
        raise ValueError(f"{name} has no records")
    return frame


def forecast_rag(variance_pct: pd.Series) -> pd.Series:
    """Classify forecast variance with centrally configured inclusive boundaries."""
    green = SETTINGS["forecast_rag_thresholds"]["green_max"]
    amber = SETTINGS["forecast_rag_thresholds"]["amber_max"]
    return pd.cut(variance_pct, [-float("inf"), green, amber, float("inf")], labels=["Green", "Amber", "Red"], include_lowest=True).astype("string")


def risk_band(score: pd.Series) -> pd.Series:
    bands = SETTINGS["risk_score_bands"]
    return pd.cut(score, [0, bands["green_max"], bands["amber_max"], bands["red_max"]], labels=["Green", "Amber", "Red"], include_lowest=True).astype("string")


def calculate_financials(programmes: pd.DataFrame, financials: pd.DataFrame) -> pd.DataFrame:
    data = financials.copy()
    numeric = ["ApprovedBudget", "ActualExpenditure", "ForecastExpenditure", "PreviousForecast"]
    data[numeric] = data[numeric].apply(pd.to_numeric, errors="coerce")
    consolidated = programmes.merge(data, on="ProgrammeID", how="left", validate="one_to_one")
    consolidated["BudgetVariance"] = consolidated.ActualExpenditure - consolidated.ApprovedBudget
    consolidated["BudgetVariancePct"] = consolidated.BudgetVariance.div(consolidated.ApprovedBudget.where(consolidated.ApprovedBudget.ne(0)))
    consolidated["ForecastVariance"] = consolidated.ForecastExpenditure - consolidated.ApprovedBudget
    consolidated["ForecastVariancePct"] = consolidated.ForecastVariance.div(consolidated.ApprovedBudget.where(consolidated.ApprovedBudget.ne(0)))
    consolidated["BudgetUtilisation"] = consolidated.ActualExpenditure.div(consolidated.ApprovedBudget.where(consolidated.ApprovedBudget.ne(0)))
    consolidated["RemainingBudget"] = consolidated.ApprovedBudget - consolidated.ActualExpenditure
    consolidated["ForecastMovement"] = consolidated.ForecastExpenditure - consolidated.PreviousForecast
    consolidated["ForecastRAG"] = forecast_rag(consolidated["ForecastVariancePct"])
    consolidated["ExceptionFlag"] = consolidated["ForecastRAG"].eq("Red")
    return consolidated


def prepare_risks(risks: pd.DataFrame) -> pd.DataFrame:
    result = risks.copy()
    is_risk = result.RecordType.eq("Risk")
    likelihood = pd.to_numeric(result.Likelihood, errors="coerce")
    impact = pd.to_numeric(result.Impact, errors="coerce")
    valid = likelihood.between(1, 5) & impact.between(1, 5)
    result["RiskScore"] = (likelihood * impact).where(is_risk & valid)
    result["RiskBand"] = risk_band(result["RiskScore"])
    result["RiskScoreValidation"] = "Not applicable: qualitative issue severity"
    result.loc[is_risk & valid, "RiskScoreValidation"] = "Valid"
    result.loc[is_risk & ~valid, "RiskScoreValidation"] = "Invalid likelihood or impact (must be 1-5)"
    result["EscalationFlag"] = (is_risk & result.RiskScore.ge(SETTINGS["risk_escalation"]["minimum_inherent_score"]) & result.Status.ne("Closed")) | result.Owner.isna()
    return result


def prepare_actions(actions: pd.DataFrame) -> pd.DataFrame:
    result = actions.copy()
    result["DueDate"] = pd.to_datetime(result.DueDate, errors="coerce")
    result["Overdue"] = result.DueDate.lt(REPORTING_DATE) & result.Status.ne("Closed")
    # Source escalation status is deliberately separate from overdue status.
    result["EscalationFlag"] = result.EscalationRequired.astype("string").str.strip().str.lower().eq("yes")
    return result


def quality_checks(programmes: pd.DataFrame, financials: pd.DataFrame, risks: pd.DataFrame, actions: pd.DataFrame) -> pd.DataFrame:
    checks: list[dict[str, object]] = []
    def add(area: str, name: str, actual: object, expected: str, passed: bool) -> None:
        checks.append({"CheckArea": area, "Check": name, "ActualValue": actual, "ExpectedCondition": expected, "Status": "Pass" if passed else "Fail", "ExecutionStatus": "Executed"})
    for name, frame in {"programme_master": programmes, "financial_submissions": financials, "risk_issue_register": risks, "corrective_actions": actions}.items():
        add("Source", f"{name} record count", len(frame), "> 0", len(frame) > 0)
    add("Programme", "Duplicate programme IDs", int(programmes.ProgrammeID.duplicated().sum()), "0", not programmes.ProgrammeID.duplicated().any())
    add("Financial", "Duplicate financial submissions", int(financials.ProgrammeID.duplicated().sum()), "0", not financials.ProgrammeID.duplicated().any())
    values = financials[["ApprovedBudget", "ActualExpenditure", "ForecastExpenditure", "PreviousForecast"]].apply(pd.to_numeric, errors="coerce")
    add("Financial", "Missing financial values", int(values.isna().sum().sum()), "0", not values.isna().any().any())
    add("Financial", "Negative financial values", int((values < 0).sum().sum()), "0", not (values < 0).any().any())
    due_dates = pd.to_datetime(actions.DueDate, errors="coerce")
    add("Governance", "Missing programme owners", int(programmes.ProgrammeOwner.isna().sum()), "0", not programmes.ProgrammeOwner.isna().any())
    add("Governance", "Risks or issues without owners", int(risks.Owner.isna().sum()), "0", not risks.Owner.isna().any())
    add("Governance", "Open actions without due dates", int((actions.Status.ne("Closed") & due_dates.isna()).sum()), "0", not (actions.Status.ne("Closed") & due_dates.isna()).any())
    ids = set(programmes.ProgrammeID)
    for label, frame in {"Financial": financials, "Risk/issue": risks, "Action": actions}.items():
        unknown = int((~frame.ProgrammeID.isin(ids)).sum())
        add("Referential integrity", f"{label} programme IDs in master", unknown, "0", unknown == 0)
    add("Governance", "Invalid action dates", int(due_dates.isna().sum()), "0", not due_dates.isna().any())
    return pd.DataFrame(checks)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    programmes = read_source("programme_master.csv", PROGRAMME_COLUMNS)
    financials = read_source("financial_submissions.csv", FINANCIAL_COLUMNS)
    risks = read_source("risk_issue_register.csv", RISK_COLUMNS)
    actions = read_source("corrective_actions.csv", ACTION_COLUMNS)
    qa = quality_checks(programmes, financials, risks, actions)
    portfolio, risk_register, action_tracker = calculate_financials(programmes, financials), prepare_risks(risks), prepare_actions(actions)
    exceptions = portfolio.loc[portfolio.ExceptionFlag, ["ProgrammeID", "ProgrammeName", "ProgrammeOwner", "ForecastVariance", "ForecastVariancePct", "ForecastMovement", "ForecastRAG", "RiskRating", "RiskDescription"]].sort_values("ForecastVariance", ascending=False)
    summary = pd.DataFrame([
        ("Total approved budget", portfolio.ApprovedBudget.sum(), "GBP"), ("Total actual expenditure", portfolio.ActualExpenditure.sum(), "GBP"),
        ("Total forecast expenditure", portfolio.ForecastExpenditure.sum(), "GBP"), ("Portfolio forecast variance", portfolio.ForecastVariance.sum(), "GBP"),
        ("Budget utilisation", portfolio.ActualExpenditure.sum() / portfolio.ApprovedBudget.sum(), "%"), ("Red forecast exceptions", int(portfolio.ForecastRAG.eq("Red").sum()), "count"),
        ("Open red risks", int((risk_register.RiskBand.eq("Red") & risk_register.Status.ne("Closed")).sum()), "count"), ("Overdue actions", int(action_tracker.Overdue.sum()), "count"),
    ], columns=["Metric", "Value", "Unit"])
    source_counts = {"programme_master": len(programmes), "financial_submissions": len(financials), "risk_issue_register": len(risks), "corrective_actions": len(actions)}
    status = "Passed" if qa.Status.eq("Pass").all() else "Review Required"
    refresh = pd.DataFrame([{"RefreshID": f"FIN-{uuid.uuid4().hex[:8].upper()}", "ReportingDate": REPORTING_DATE.date().isoformat(), "ProcessingTimestampUTC": datetime.now(timezone.utc).isoformat(), "SourceFiles": "; ".join(f"{k}.csv ({v})" for k, v in source_counts.items()), "RecordsReceived": sum(source_counts.values()), "ProgrammeRecordsProcessed": len(portfolio), "Exceptions": int(qa.Status.ne("Pass").sum()), "RefreshStatus": status, "Definitions": "Records Received = all source rows across four files; Programme Records Processed = consolidated programme rows.", "Reviewer": "Business Management Analyst"}])
    for name, frame in {"portfolio_financials": portfolio, "risk_issue_register": risk_register, "action_tracker": action_tracker, "financial_exceptions": exceptions, "financial_summary": summary, "data_quality_report": qa, "refresh_control_log": refresh}.items(): frame.to_csv(OUT / f"{name}.csv", index=False)
    (OUT / "run_manifest.json").write_text(json.dumps({"reporting_date": str(REPORTING_DATE.date()), "source_record_counts": source_counts, "settings": SETTINGS, "data_policy": SETTINGS["data_disclosure"]}, indent=2), encoding="utf-8")
    print(f"Financial refresh {status}: {len(portfolio)} programmes, {len(exceptions)} red forecast exceptions, {int(action_tracker.Overdue.sum())} overdue actions.")
    return 0 if status == "Passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
