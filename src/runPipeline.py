"""Repeatable local reporting pipeline for the enterprise performance portfolio."""
from __future__ import annotations

import json
import logging
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LOCAL_PACKAGES = ROOT / ".python_packages"
if LOCAL_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_PACKAGES))
EXPECTED = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]


def loadConfig() -> dict:
    return json.loads((ROOT / "config" / "project_config.json").read_text(encoding="utf-8"))


def makePortfolio(reportingDate: pd.Timestamp) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    projects = [
        ("PRJ-001", "Contact Centre Workflow Simplification", "Operations", "Operations Director", "Delivery Manager", "High", "2021-07-01", "2021-11-30", "2021-12-16", None, 420000, 310000, 468000, .76, "At Risk", "Amber", "Pilot readiness", "2021-11-25", "Telephony migration", "2021-11-30", "Pilot staffing dependency may delay the forecast."),
        ("PRJ-002", "Customer Case Routing Upgrade", "Technology", "Technology Director", "Product Manager", "Critical", "2021-06-15", "2021-12-15", "2022-01-28", None, 780000, 670000, 920000, .68, "Off Track", "Red", "Integration testing", "2021-12-06", "PRJ-005", "2021-12-02", "Unresolved interface defects block end-to-end testing."),
        ("PRJ-003", "Sales Data Quality Controls", "Data", "Data Governance Lead", "Data Product Owner", "High", "2021-08-01", "2021-12-20", "2021-12-20", None, 260000, 190000, 245000, .71, "On Track", "Green", "Control sign-off", "2021-12-15", "Data steward capacity", "2021-12-04", "Control evidence is progressing to plan."),
        ("PRJ-004", "Month-End Reporting Automation", "Controls", "Finance Controls Lead", "Reporting Manager", "High", "2021-07-15", "2021-12-10", "2021-12-22", None, 340000, 305000, 370000, .82, "At Risk", "Amber", "User acceptance testing", "2021-12-09", "PRJ-003", "2021-12-01", "Late source mapping remediation creates a compressed test window."),
        ("PRJ-005", "Core Integration Stabilisation", "Technology", "Technology Director", "Engineering Manager", "Critical", "2021-05-01", "2021-11-15", "2022-02-10", None, 1100000, 980000, 1350000, .60, "Off Track", "Red", "Defect remediation", "2021-12-17", "External platform supplier", "2021-12-01", "Supplier defect backlog exceeds approved recovery capacity."),
        ("PRJ-006", "Returns Process Redesign", "Customer", "Customer Operations Head", "Process Owner", "Medium", "2021-09-01", "2022-02-28", "2022-02-28", None, 180000, 60000, 175000, .33, "On Track", "Green", "Future-state design", "2021-12-20", "Policy approval", "2021-12-05", "Discovery remains within approved scope and budget."),
        ("PRJ-007", "Vendor Access Recertification", "Controls", "Risk and Controls Lead", "Control Manager", "High", "2021-04-01", "2021-10-31", "2021-10-29", "2021-10-29", 150000, 142000, 142000, 1.0, "Complete", "Green", "Closure evidence archived", "2021-10-29", "None", "2021-11-02", "Completed with closure evidence recorded."),
        ("PRJ-008", "Knowledge Base Renewal", "Customer", "Customer Operations Head", "Content Lead", "Medium", "2021-10-15", "2022-03-31", "2022-04-14", None, 120000, 25000, 133000, .18, "At Risk", "Amber", "Content taxonomy approval", "2021-12-14", "Legal review", "2021-11-25", "Content approval is overdue and delays migration."),
        ("PRJ-009", "Demand Forecasting Prototype", "Data", "Data Governance Lead", "Analytics Manager", "Medium", "2021-09-15", "2022-01-31", "2022-01-28", None, 300000, 110000, 290000, .41, "On Track", "Green", "Model validation", "2021-12-22", "Data extracts", "2021-12-03", "Validation milestones remain achievable."),
        ("PRJ-010", "Operational Resilience Playbooks", "Operations", "Operations Director", "Resilience Manager", "High", "2021-08-15", "2022-01-15", "2022-01-15", None, 230000, 150000, 228000, .58, "On Track", "Green", "Scenario exercise", "2021-12-16", "Business participation", "2021-12-06", "Exercise participants have confirmed attendance."),
        ("PRJ-011", "Supplier Invoice Controls", "Controls", "Finance Controls Lead", "Control Manager", "Low", "2022-01-10", "2022-05-31", "2022-05-31", None, 90000, 0, 88000, .0, "Not Started", "Green", "Kick-off", "2022-01-10", "None", "2021-12-08", "Approved but not yet started."),
    ]
    cols = ["ProjectID", "ProjectName", "Workstream", "SponsorRole", "ProjectManagerRole", "Priority", "StartDate", "BaselineEndDate", "ForecastEndDate", "ActualEndDate", "Budget", "ActualCost", "ForecastCost", "PercentComplete", "Status", "RAGStatus", "KeyMilestone", "NextMilestoneDate", "Dependency", "LastUpdated", "StatusCommentary"]
    portfolio = pd.DataFrame(projects, columns=cols)
    for c in ["StartDate", "BaselineEndDate", "ForecastEndDate", "ActualEndDate", "NextMilestoneDate", "LastUpdated"]: portfolio[c] = pd.to_datetime(portfolio[c])
    portfolio["ScheduleVarianceDays"] = (portfolio["ForecastEndDate"] - portfolio["BaselineEndDate"]).dt.days
    portfolio["BudgetUtilisation"] = portfolio["ActualCost"] / portfolio["Budget"]
    portfolio["ForecastBudgetVariance"] = portfolio["ForecastCost"] - portfolio["Budget"]
    portfolio["StatusAgeDays"] = (reportingDate - portfolio["LastUpdated"]).dt.days
    milestones = []
    for _, p in portfolio.iterrows():
        completed = p.Status == "Complete"
        milestones.extend([
          [f"MS-{p.ProjectID[-3:]}-01", p.ProjectID, "Design / planning complete", p.StartDate + pd.Timedelta(days=30), p.StartDate + pd.Timedelta(days=32), p.StartDate + pd.Timedelta(days=32) if completed else pd.NaT, "Complete" if completed else "In Progress", p.ProjectManagerRole, "Synthetic portfolio evidence"],
          [f"MS-{p.ProjectID[-3:]}-02", p.ProjectID, p.KeyMilestone, p.NextMilestoneDate - pd.Timedelta(days=max(0, p.ScheduleVarianceDays)), p.NextMilestoneDate, p.NextMilestoneDate if completed else pd.NaT, "Complete" if completed else ("Overdue" if p.NextMilestoneDate < reportingDate else ("At Risk" if p.RAGStatus != "Green" else "In Progress")), p.ProjectManagerRole, "Synthetic portfolio evidence"]
        ])
    milestoneDf = pd.DataFrame(milestones, columns=["MilestoneID", "ProjectID", "MilestoneName", "BaselineDate", "ForecastDate", "ActualDate", "MilestoneStatus", "OwnerRole", "EvidenceLink"])
    milestoneDf["ScheduleVarianceDays"] = (milestoneDf.ForecastDate - milestoneDf.BaselineDate).dt.days
    records = [
      ["REC-001", "Risk", "PRJ-005", "Supplier defect backlog", "External supplier defects threaten recovery plan.", 5, 5, "Critical", "Engineering Manager", "2021-11-10", "2021-11-30", "Blocked", "Agree capacity and recovery plan with supplier.", True, None],
      ["REC-002", "Risk", "PRJ-002", "Integration test failure", "Interface failures block customer routing release.", 4, 5, "Critical", "Product Manager", "2021-11-15", "2021-12-03", "In Progress", "Prioritise defect triage and daily recovery review.", True, None],
      ["REC-003", "Issue", "PRJ-004", "Test window compressed", "Late source mapping reduces user acceptance test time.", None, None, "High", "Reporting Manager", "2021-11-20", "2021-12-09", "Open", "Approve constrained test plan.", True, None],
      ["REC-004", "Action", "PRJ-001", "Confirm pilot staffing", "Operations must confirm trained pilot staff.", None, None, "High", "Operations Director", "2021-11-18", "2021-11-29", "Open", "Confirm staffing roster and training dates.", True, None],
      ["REC-005", "Dependency", "PRJ-008", "Legal content review", "Legal approval is needed before content migration.", None, None, "Medium", "Content Lead", "2021-11-12", "2021-12-01", "In Progress", "Escalate review capacity request.", False, None],
      ["REC-006", "Risk", "PRJ-003", "Steward capacity", "Control sign-off depends on allocated data steward capacity.", 3, 4, "High", "Data Product Owner", "2021-11-21", "2021-12-15", "In Progress", "Reserve sign-off sessions.", False, None],
      ["REC-007", "Action", "PRJ-010", "Run resilience exercise", "Business teams must complete the scheduled scenario exercise.", None, None, "Medium", "Resilience Manager", "2021-11-25", "2021-12-16", "Open", "Facilitate exercise and capture actions.", False, None],
      ["REC-008", "Action", "PRJ-007", "Archive closure evidence", "Archive closure evidence for completed control work.", None, None, "Low", "Control Manager", "2021-10-20", "2021-10-29", "Closed", "Evidence archived.", False, "2021-10-29"],
    ]
    riskDf = pd.DataFrame(records, columns=["RecordID", "RecordType", "ProjectID", "Title", "Description", "Probability", "Impact", "Priority", "OwnerRole", "DateRaised", "DueDate", "Status", "MitigationOrNextStep", "EscalationRequired", "ClosedDate"])
    for c in ["DateRaised", "DueDate", "ClosedDate"]: riskDf[c] = pd.to_datetime(riskDf[c])
    riskDf["RiskScore"] = riskDf["Probability"] * riskDf["Impact"]
    riskDf["IsOverdue"] = (riskDf.RecordType == "Action") & (riskDf.Status != "Closed") & (riskDf.DueDate < reportingDate)
    return portfolio, milestoneDf, riskDf


def cleanTransactions(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    for c in ["InvoiceNo", "StockCode", "Description", "Country"]: df[c] = df[c].astype("string").str.strip()
    df["InvoiceDateParsed"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["YearMonth"] = df["InvoiceDateParsed"].dt.to_period("M").astype("string")
    df["LineValue"] = df["Quantity"] * df["UnitPrice"]
    df["IsCancellation"] = df["InvoiceNo"].str.upper().str.startswith("C", na=False)
    df["IsNegativeQuantity"] = df["Quantity"] < 0
    df["IsZeroOrNegativePrice"] = df["UnitPrice"] <= 0
    df["IsMissingCustomer"] = df["CustomerID"].isna()
    df["IsValidForSalesAnalysis"] = (~df.IsCancellation & ~df.IsNegativeQuantity & ~df.IsZeroOrNegativePrice & df.InvoiceDateParsed.notna() & df.Quantity.notna())
    flags = pd.DataFrame({"invalid_date": df.InvoiceDateParsed.isna(), "negative_or_zero_price": df.IsZeroOrNegativePrice, "missing_customer": df.IsMissingCustomer, "cancellation": df.IsCancellation, "negative_quantity": df.IsNegativeQuantity})
    df["DataQualityFlags"] = flags.apply(lambda r: "; ".join(k for k, v in r.items() if v) or "None", axis=1)
    return df


def calculateKpis(df: pd.DataFrame, portfolio: pd.DataFrame, milestones: pd.DataFrame, records: pd.DataFrame, reportingDate: pd.Timestamp) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    valid = df[df.IsValidForSalesAnalysis].copy()
    gross = valid.LineValue.sum(); cancellation = abs(df.loc[df.IsCancellation, "LineValue"].sum()); net = df.LineValue.sum()
    monthly = valid.groupby("YearMonth", dropna=True).agg(GrossPositiveSales=("LineValue", "sum"), EligibleInvoiceCount=("InvoiceNo", "nunique")).reset_index().sort_values("YearMonth")
    monthly["MonthlySalesGrowth"] = monthly.GrossPositiveSales.pct_change().replace([float("inf"), -float("inf")], pd.NA)
    monthly["AverageOrderValue"] = monthly.GrossPositiveSales / monthly.EligibleInvoiceCount
    countries = valid.groupby("Country").LineValue.sum().sort_values(ascending=False).rename("GrossPositiveSales").reset_index(); countries["Contribution"] = countries.GrossPositiveSales / gross
    products = valid.groupby(["StockCode", "Description"], dropna=False).LineValue.sum().sort_values(ascending=False).head(20).rename("GrossPositiveSales").reset_index()
    customers = valid.dropna(subset=["CustomerID"]).groupby("CustomerID").LineValue.sum().sort_values(ascending=False).head(20).rename("GrossPositiveSales").reset_index(); customers["Contribution"] = customers.GrossPositiveSales / gross
    completeness = pd.DataFrame({"Field": EXPECTED, "Completeness": [1 - df[x].isna().mean() for x in EXPECTED]})
    kpis = [
      ["Gross positive sales value", gross, "GBP", "Valid positive transaction lines"], ["Cancellation value", cancellation, "GBP", "Absolute cancellation line value"], ["Net transaction value", net, "GBP", "All signed transaction lines"], ["Eligible invoice count", valid.InvoiceNo.nunique(), "count", "Distinct eligible invoices"], ["Cancellation rate", df.loc[df.IsCancellation, "InvoiceNo"].nunique() / max(1, df.InvoiceNo.nunique()), "%", "Cancellation invoices / all invoices"], ["Top 10 customer concentration", customers.head(10).GrossPositiveSales.sum() / gross, "%", "Missing CustomerID excluded"],
      ["At-risk or off-track projects", portfolio.Status.isin(["At Risk", "Off Track"]).sum(), "count", "Synthetic portfolio"], ["Overdue actions", records.IsOverdue.sum(), "count", "Open synthetic actions due before reporting date"], ["Forecast portfolio budget variance", portfolio.ForecastBudgetVariance.sum(), "GBP", "Forecast cost minus budget"], ["High-risk exposure", ((records.RecordType == "Risk") & (records.RiskScore >= 15) & (records.Status != "Closed")).sum(), "count", "Risk score >= 15 assumption"], ["Overdue milestones", (milestones.MilestoneStatus == "Overdue").sum(), "count", "Synthetic portfolio"],
    ]
    return pd.DataFrame(kpis, columns=["KPI", "Value", "Unit", "Definition"]), {"monthly_sales": monthly, "country_contribution": countries, "top_products": products, "top_customers": customers, "data_completeness": completeness}


def main() -> int:
    cfg = loadConfig(); reportingDate = pd.Timestamp(cfg["reporting_date"]); runId = f"RUN-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:6]}"
    out, qa = ROOT / "outputs" / "processed", ROOT / "outputs" / "qa"; out.mkdir(parents=True, exist_ok=True); qa.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=qa / "pipeline.log", level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    rawPath = ROOT / cfg["raw_file"]
    if not rawPath.exists(): raise FileNotFoundError(f"Raw source missing: {rawPath}")
    raw = pd.read_excel(rawPath, engine="calamine", dtype={"InvoiceNo": "string", "StockCode": "string"})
    missing = [x for x in EXPECTED if x not in raw.columns]
    if missing: raise ValueError(f"Critical schema failure. Missing required columns: {missing}")
    clean = cleanTransactions(raw); portfolio, milestones, records = makePortfolio(reportingDate); kpis, summaries = calculateKpis(clean, portfolio, milestones, records, reportingDate)
    duplicateCount = int(raw.duplicated(subset=EXPECTED, keep=False).sum()); dateFailures = int(clean.InvoiceDateParsed.isna().sum()); invalidSales = int((~clean.IsValidForSalesAnalysis).sum())
    clean.to_csv(out / "clean_transactions.csv", index=False); portfolio.to_csv(out / "project_portfolio.csv", index=False); milestones.to_csv(out / "milestones.csv", index=False); records.to_csv(out / "risks_actions.csv", index=False); kpis.to_csv(out / "kpi_summary.csv", index=False)
    for name, table in summaries.items(): table.to_csv(out / f"{name}.csv", index=False)
    checks = pd.DataFrame([
      ["Schema", "Required columns present", "Pass", len(EXPECTED), len(EXPECTED), "Critical"], ["Rows", "Raw rows equal clean output rows", "Pass" if len(raw) == len(clean) else "Fail", len(raw), len(clean), "Critical"], ["Date parsing", "Unparseable invoice dates", "Pass" if dateFailures == 0 else "Warning", 0, dateFailures, "Non-critical"], ["Duplicates", "Exact duplicate candidates retained", "Warning" if duplicateCount else "Pass", 0, duplicateCount, "Non-critical"], ["Sales eligibility", "Rows excluded from positive-sales view remain traceable", "Pass", len(clean), invalidSales, "Control"], ["Portfolio", "Unique project IDs", "Pass" if portfolio.ProjectID.is_unique else "Fail", len(portfolio), portfolio.ProjectID.nunique(), "Critical"], ["Portfolio", "Completed projects have 100% progress and actual end date", "Pass" if ((portfolio.Status != "Complete") | ((portfolio.PercentComplete == 1) & portfolio.ActualEndDate.notna())).all() else "Fail", 1, 1, "Critical"]
    ], columns=["CheckArea", "Check", "Status", "Expected", "Actual", "Severity"])
    checks.to_csv(qa / "qa_reconciliation.csv", index=False)
    exceptions = checks[checks.Status != "Pass"].copy(); exceptions.to_csv(qa / "exceptions.csv", index=False)
    run = pd.DataFrame([[runId, datetime.now(timezone.utc).isoformat(), rawPath.name, len(raw), len(clean), invalidSales, len(exceptions), int((checks.Status == "Fail").sum()), "Fail" if (checks.Status == "Fail").any() else ("Warning" if len(exceptions) else "Pass"), "Failed" if (checks.Status == "Fail").any() else ("Partial Success" if len(exceptions) else "Success"), "Raw rows retained; sales view excludes cancellations, negative quantities, zero/negative prices and invalid dates."]], columns=["RunID", "RunTimestamp", "SourceName", "SourceRowCount", "OutputRowCount", "RejectedRowCount", "WarningCount", "ErrorCount", "ReconciliationStatus", "RunStatus", "Notes"])
    run.to_csv(qa / "run_log.csv", index=False)
    logging.info("%s completed with %s warnings", runId, len(exceptions)); print(f"{runId}: {run.RunStatus.iloc[0]}. {len(raw):,} raw rows; {len(clean):,} clean rows; {len(exceptions)} QA warnings.")
    return 1 if (checks.Status == "Fail").any() else 0


if __name__ == "__main__": sys.exit(main())
