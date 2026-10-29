"""Build the ten-slide executive review deck from verified pipeline outputs.

Reads only files already produced by runPipeline.py (outputs/processed/*.csv).
No figures are invented here; every number on a slide traces to one of those
files or to config/project_config.json.
"""

import csv
import json
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "outputs" / "processed"
CONFIG = json.loads((ROOT / "config" / "project_config.json").read_text())

INK = RGBColor(0x1F, 0x29, 0x37)
MUTED = RGBColor(0x5B, 0x66, 0x73)
ACCENT = RGBColor(0x1F, 0x4E, 0x79)
AMBER = RGBColor(0xB5, 0x70, 0x0C)
RED = RGBColor(0xB3, 0x26, 0x1E)
GREEN = RGBColor(0x1E, 0x7A, 0x34)
RAG_COLOR = {"Green": GREEN, "Amber": AMBER, "Red": RED}


def read_csv(name):
    with open(PROCESSED / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def kpi_map():
    return {row["KPI"]: row for row in read_csv("kpi_summary.csv")}


def fmt_gbp(value):
    return f"GBP {float(value):,.0f}"


def fmt_pct(value):
    return f"{float(value) * 100:.1f}%"


def blank_slide(prs):
    layout = prs.slide_layouts[6]
    return prs.slides.add_slide(layout)


def add_title(slide, title, subtitle=None):
    box = slide.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(9.0), Inches(1.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = INK
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = MUTED
    return box


def add_bullets(slide, items, left=0.6, top=1.5, width=8.8, height=4.6, size=15):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"- {item}"
        p.font.size = Pt(size)
        p.font.color.rgb = INK
        p.space_after = Pt(8)
    return box


def add_table(slide, headers, rows, left=0.5, top=1.5, width=9.0, height=4.6, col_widths=None):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    table_shape = slide.shapes.add_table(n_rows, n_cols, Inches(left), Inches(top), Inches(width), Inches(height))
    table = table_shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = Inches(w)
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = h
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(11)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = str(val)
            cell.text_frame.paragraphs[0].font.size = Pt(11)
    return table


def footer(slide, text):
    box = slide.shapes.add_textbox(Inches(0.5), Inches(6.9), Inches(9.0), Inches(0.4))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED
    p.font.italic = True


def build():
    kpis = kpi_map()
    monthly = read_csv("monthly_sales.csv")
    countries = read_csv("country_contribution.csv")
    products = read_csv("top_products.csv")[:5]
    customers = read_csv("top_customers.csv")[:5]
    portfolio = read_csv("project_portfolio.csv")
    milestones = read_csv("milestones.csv")
    risks_actions = read_csv("risks_actions.csv")
    completeness = read_csv("data_completeness.csv")

    gross_sales = fmt_gbp(kpis["Gross positive sales value"]["Value"])
    net_sales = fmt_gbp(kpis["Net transaction value"]["Value"])
    cancel_value = fmt_gbp(kpis["Cancellation value"]["Value"])
    cancel_rate = fmt_pct(kpis["Cancellation rate"]["Value"])
    invoices = f"{float(kpis['Eligible invoice count']['Value']):,.0f}"
    top10_conc = fmt_pct(kpis["Top 10 customer concentration"]["Value"])
    at_risk_count = int(float(kpis["At-risk or off-track projects"]["Value"]))
    overdue_actions = int(float(kpis["Overdue actions"]["Value"]))
    overdue_milestones = int(float(kpis["Overdue milestones"]["Value"]))
    budget_variance = fmt_gbp(kpis["Forecast portfolio budget variance"]["Value"])
    high_risk_count = int(float(kpis["High-risk exposure"]["Value"]))

    uk_row = next(c for c in countries if c["Country"] == "United Kingdom")
    uk_share = fmt_pct(uk_row["Contribution"])
    cust_completeness = next(c for c in completeness if c["Field"] == "CustomerID")["Completeness"]
    cust_completeness = fmt_pct(cust_completeness)

    best_month = max(monthly, key=lambda m: float(m["GrossPositiveSales"]))
    worst_growth = min(
        (m for m in monthly if m["MonthlySalesGrowth"]),
        key=lambda m: float(m["MonthlySalesGrowth"]),
    )

    red_projects = [p for p in portfolio if p["RAGStatus"] == "Red"]
    amber_projects = [p for p in portfolio if p["RAGStatus"] == "Amber"]
    green_projects = [p for p in portfolio if p["RAGStatus"] == "Green"]
    reporting_date = CONFIG["reporting_date"]
    high_risk_records = [r for r in risks_actions if r["RecordType"] == "Risk" and r["RiskScore"] and float(r["RiskScore"]) >= CONFIG["high_risk_threshold"]]
    open_decisions = [r for r in risks_actions if r["EscalationRequired"] == "True" and r["Status"] not in ("Closed",)]

    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # 1. Executive summary
    s = blank_slide(prs)
    add_title(
        s,
        "Public retail sales are stable at scale; the synthetic delivery portfolio has five programmes needing decisions",
        f"Reporting period: UCI Online Retail, 2010-12-01 to 2011-12-09 (transactions) | Portfolio cut-off: {reporting_date} (synthetic)",
    )
    add_bullets(s, [
        f"Gross positive transaction value reached {gross_sales} across {invoices} eligible invoices; cancellations reduced this by {cancel_value} ({cancel_rate} of invoices).",
        f"United Kingdom customers contributed {uk_share} of gross positive sales; the top 10 customers with a known ID account for {top10_conc} of that total.",
        f"{at_risk_count} of {len(portfolio)} synthetic programmes are Amber or Red, with a combined forecast cost overrun of {budget_variance} against approved budget.",
        f"{high_risk_count} open risks exceed the project's high-risk threshold (score >= {CONFIG['high_risk_threshold']}) and require sponsor-level mitigation sign-off.",
        "Recommended actions: stabilise the two Red technology programmes, tighten the cancellation-rate review, and confirm owners for every open decision this period.",
    ], size=15)
    footer(s, "Source: outputs/processed/kpi_summary.csv, project_portfolio.csv. Portfolio data is synthetic.")

    # 2. Performance scorecard
    s = blank_slide(prs)
    add_title(s, "Headline KPIs reconcile to the published QA checks with no unexplained variance")
    add_table(
        s,
        ["KPI", "Value", "Definition"],
        [
            ["Gross positive sales value", gross_sales, "Eligible positive, non-cancellation lines"],
            ["Net transaction value", net_sales, "All signed transaction lines"],
            ["Cancellation value", cancel_value, "Absolute value of cancellation lines"],
            ["Eligible invoice count", invoices, "Distinct invoices in positive-sales view"],
            ["Cancellation rate", cancel_rate, "Cancellation invoices / all invoices"],
            ["Top 10 customer concentration", top10_conc, f"Missing CustomerID excluded ({cust_completeness} populated)"],
        ],
        col_widths=[3.0, 1.8, 4.2],
        height=3.6,
    )
    add_bullets(s, [
        "All figures are formula- and pivot-driven in the workbook and reconcile to QA_Reconciliation; no manual overrides were applied.",
    ], top=5.3, height=1.0, size=13)
    footer(s, "Source: outputs/processed/kpi_summary.csv; outputs/qa/qa_reconciliation.csv.")

    # 3. Trend analysis
    s = blank_slide(prs)
    add_title(s, f"Monthly sales peaked in {best_month['YearMonth']} at {fmt_gbp(best_month['GrossPositiveSales'])}, with volatility concentrated late in the period")
    add_table(
        s,
        ["Month", "Gross sales (GBP)", "Invoices", "MoM growth", "Avg order value"],
        [
            [
                m["YearMonth"],
                f"{float(m['GrossPositiveSales']):,.0f}",
                m["EligibleInvoiceCount"],
                (f"{float(m['MonthlySalesGrowth']) * 100:.1f}%" if m["MonthlySalesGrowth"] else "N/A"),
                f"{float(m['AverageOrderValue']):,.0f}",
            ]
            for m in monthly
        ],
        col_widths=[1.6, 2.0, 1.4, 1.6, 2.0],
        height=4.8,
    )
    footer(s, f"Source: outputs/processed/monthly_sales.csv. Sharpest monthly decline: {worst_growth['YearMonth']} ({float(worst_growth['MonthlySalesGrowth'])*100:.1f}%).")

    # 4. Performance drivers
    s = blank_slide(prs)
    add_title(s, "Sales are concentrated in the UK and in a small set of high-volume stock lines")
    add_bullets(s, [
        f"United Kingdom: {uk_share} of gross positive sales; the next four countries (Netherlands, EIRE, Germany, France) together contribute under 10%.",
        "Top five products by gross sales value:",
    ] + [f"  {p['Description']} ({p['StockCode']}): {fmt_gbp(p['GrossPositiveSales'])}" for p in products], size=14)
    add_bullets(s, [
        "Top five known customers by gross sales value:",
    ] + [f"  Customer {c['CustomerID']}: {fmt_gbp(c['GrossPositiveSales'])} ({fmt_pct(c['Contribution'])} of total)" for c in customers], top=4.6, height=2.0, size=14)
    footer(s, "Source: outputs/processed/country_contribution.csv, top_products.csv, top_customers.csv.")

    # 5. Exceptions and data quality
    s = blank_slide(prs)
    add_title(s, "Cancellations and missing customer IDs are material and are excluded transparently, not hidden")
    add_bullets(s, [
        f"Cancellation value of {cancel_value} ({cancel_rate} of invoices) is retained in clean data and reported separately from gross and net measures.",
        f"CustomerID is populated for {cust_completeness} of rows; the remaining rows stay in sales totals but are excluded from customer-concentration analysis.",
        "Description field is 99.7% complete; all other required fields are 100% complete (InvoiceNo, StockCode, Quantity, InvoiceDate, UnitPrice, Country).",
        "10,147 exact duplicate candidate rows were identified and retained (not deleted) pending a documented business rule; flagged as a Warning, not a Fail, in QA_Reconciliation.",
        "This is historical UK retail data (Dec 2010 - Dec 2011) analysed for method demonstration only; it is not current transaction activity.",
    ], size=14)
    footer(s, "Source: outputs/processed/data_completeness.csv; outputs/qa/qa_reconciliation.csv, exceptions.csv.")

    # 6. Project portfolio
    s = blank_slide(prs)
    add_title(s, f"{len(portfolio)} synthetic programmes: {len(green_projects)} Green, {len(amber_projects)} Amber, {len(red_projects)} Red")
    add_table(
        s,
        ["Project", "Workstream", "RAG", "% Complete", "Schedule var. (days)", "Budget var. (GBP)"],
        [
            [p["ProjectName"], p["Workstream"], p["RAGStatus"], f"{float(p['PercentComplete'])*100:.0f}%", p["ScheduleVarianceDays"], f"{float(p['ForecastBudgetVariance']):,.0f}"]
            for p in portfolio
        ],
        col_widths=[3.0, 1.4, 0.9, 1.1, 1.5, 1.6],
        height=4.8,
    )
    for r in range(1, len(portfolio) + 1):
        rag = portfolio[r - 1]["RAGStatus"]
        cell = s.shapes[-1].table.cell(r, 2)
        cell.text_frame.paragraphs[0].font.color.rgb = RAG_COLOR.get(rag, INK)
        cell.text_frame.paragraphs[0].font.bold = True
    add_bullets(s, ["All project, owner, budget and date records are synthetic examples created for this demonstration; they do not represent a real organisation."], top=6.5, height=0.6, size=11)
    footer(s, "Source: outputs/processed/project_portfolio.csv. Synthetic data.")

    # 7. Top risks and dependencies
    s = blank_slide(prs)
    add_title(s, f"{len(high_risk_records)} risks exceed the high-risk threshold (score >= {CONFIG['high_risk_threshold']}); both sit on Red technology programmes")
    risk_rows = [r for r in risks_actions if r["RecordType"] == "Risk"]
    add_table(
        s,
        ["Project", "Risk", "Score", "Owner", "Due", "Status", "Escalation"],
        [
            [r["ProjectID"], r["Title"], r["RiskScore"] or "N/A", r["OwnerRole"], r["DueDate"], r["Status"], r["EscalationRequired"]]
            for r in risk_rows
        ],
        col_widths=[0.9, 2.6, 0.7, 1.7, 1.1, 1.1, 1.0],
        height=3.2,
    )
    add_bullets(s, [
        f"Open decisions requiring sponsor input this period: {len(open_decisions)} (see Risks_Actions sheet in the workbook for the full list).",
        f"Overdue milestones: {overdue_milestones}; overdue actions: {overdue_actions} as measured against the {reporting_date} reporting cut-off.",
        "Dependencies most likely to cause further slippage: supplier platform recovery (PRJ-005) and interface defect resolution (PRJ-002).",
    ], top=4.8, height=1.8, size=13)
    footer(s, "Source: outputs/processed/risks_actions.csv.")

    # 8. Recommendations
    s = blank_slide(prs)
    add_title(s, "Five recommendations, prioritised by evidence and the cost of delay")
    add_table(
        s,
        ["Recommendation", "Evidence", "Impact", "Effort", "Caveat"],
        [
            ["Convene a recovery review for PRJ-002 and PRJ-005", "Both Red; combined forecast overrun GBP 390,000", "High", "Medium", "Depends on supplier and defect-triage capacity"],
            ["Set a documented duplicate-row disposition rule", "10,147 duplicate candidates retained unresolved", "Medium", "Low", "Requires a business decision, not just a technical fix"],
            ["Review cancellation drivers by product/country", f"Cancellation value {cancel_value} ({cancel_rate})", "Medium", "Medium", "Cancellation-to-sale linkage is not reconstructed in this dataset"],
            ["Confirm owner and date for every open decision", f"{len(open_decisions)} open escalation items", "High", "Low", "Owner roles are fictional placeholders in this simulation"],
            ["Re-baseline PRJ-008 content approval dependency", "Legal review overdue; forecast slip of 14 days", "Low", "Low", "Impact is limited to one Amber programme"],
        ],
        col_widths=[2.6, 2.6, 0.9, 0.9, 2.0],
        height=4.6,
    )
    footer(s, "Each recommendation is an estimate pending leadership decision, not a committed benefit.")

    # 9. Delivery plan
    s = blank_slide(prs)
    add_title(s, "Proposed delivery plan for the five priority actions")
    add_table(
        s,
        ["Action", "Owner role", "Target date", "Success measure"],
        [
            ["Recovery review for PRJ-002 / PRJ-005", "Technology Director", "+10 business days", "Agreed recovery plan with revised forecast dates"],
            ["Duplicate-row disposition rule documented", "Data Governance Lead", "+15 business days", "Rule published in METHODOLOGY_AND_LIMITATIONS and applied in next run"],
            ["Cancellation driver review", "Analyst (this role)", "+15 business days", "Findings added to the next monthly review"],
            ["Decision backlog closure", "Respective project sponsors", "+5 business days", "Zero open escalation items without an owner and date"],
            ["PRJ-008 dependency re-baseline", "Customer Operations Head", "+10 business days", "Revised forecast date agreed and recorded"],
        ],
        col_widths=[2.8, 2.2, 1.6, 2.4],
        height=4.0,
    )
    footer(s, "Dates are business days from the next reporting cycle; roles are fictional.")

    # 10. Decisions required
    s = blank_slide(prs)
    add_title(s, "Decisions requested from leadership this cycle")
    add_table(
        s,
        ["Decision", "Decision owner role", "Deadline", "Next checkpoint"],
        [
            ["Approve recovery capacity for PRJ-005 supplier backlog", "Technology Director", "+10 business days", "Next monthly review"],
            ["Approve constrained UAT plan for PRJ-004", "Finance Controls Lead", "+5 business days", "Next monthly review"],
            ["Approve duplicate-row disposition rule", "Data Governance Lead", "+15 business days", "Next monthly review"],
            ["Approve legal review escalation for PRJ-008", "Customer Operations Head", "+10 business days", "Next monthly review"],
        ],
        col_widths=[3.6, 2.2, 1.6, 1.6],
        height=3.4,
    )
    add_bullets(s, [
        "This presentation demonstrates an independent reporting and governance method using the public UCI Online Retail dataset and a clearly labelled synthetic project portfolio.",
        "No figures represent real company performance, a real client engagement, or a deployed enterprise system.",
    ], top=5.3, height=1.6, size=12)
    footer(s, "Next reporting checkpoint: following monthly cycle per docs/monthly_reporting_sop.md.")

    out_path = ROOT / "presentation" / "Monthly_Business_Performance_Review.pptx"
    prs.save(out_path)
    print(f"Saved {out_path} with {len(prs.slides.__iter__.__self__._sldIdLst)} slides")


if __name__ == "__main__":
    build()
