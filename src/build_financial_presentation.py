"""Generate the six-slide financial executive review from validated CSV outputs."""
from pathlib import Path
import pandas as pd
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT = Path(__file__).resolve().parents[1]; OUT = ROOT / "outputs" / "financial"; DEST = ROOT / "presentation" / "Financial_Portfolio_Executive_Review.pptx"
NAVY, BLUE, GREEN, AMBER, RED, INK, GREY = ("17365D", "1F4E78", "1E7A34", "B5700C", "B3261E", "1F2937", "5B6673")
rgb = lambda h: RGBColor.from_string(h)

def money(x): return f"GBP {x:,.0f}"
def add_text(slide, text, x, y, w, h, size=14, color=INK, bold=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = box.text_frame; tf.clear(); tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = str(text); p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = rgb(color); return box
def title(slide, text, sub=""):
    add_text(slide, text, .45, .25, 12.3, .45, 25, NAVY, True)
    if sub: add_text(slide, sub, .47, .76, 12, .25, 10, GREY)
def footer(slide): add_text(slide, "Synthetic illustrative data only | Reporting date: 9 December 2021 | Not a current-period business performance report", .45, 7.12, 12, .18, 8, GREY)
def table(slide, headers, rows, x, y, w, h, widths=None):
    shape = slide.shapes.add_table(len(rows)+1, len(headers), Inches(x), Inches(y), Inches(w), Inches(h)); t = shape.table
    if widths:
        for i, width in enumerate(widths): t.columns[i].width = Inches(width)
    for j, head in enumerate(headers):
        c=t.cell(0,j); c.text=head; c.fill.solid(); c.fill.fore_color.rgb=rgb(NAVY); p=c.text_frame.paragraphs[0]; p.font.bold=True; p.font.size=Pt(9); p.font.color.rgb=rgb("FFFFFF")
    for i,row in enumerate(rows,1):
        for j,val in enumerate(row):
            c=t.cell(i,j); c.text=str(val); p=c.text_frame.paragraphs[0]; p.font.size=Pt(8.5); p.font.color.rgb=rgb(INK)
    return t
def card(slide, label, value, x, color=BLUE):
    shp=slide.shapes.add_shape(1, Inches(x), Inches(1.25), Inches(2.25), Inches(1.05)); shp.fill.solid(); shp.fill.fore_color.rgb=rgb("EAF1F8"); shp.line.color.rgb=rgb(color)
    add_text(slide,label,x+.12,1.43,2,.2,9,GREY,True); add_text(slide,value,x+.12,1.74,2,.3,16,color,True)

def build():
    summary=pd.read_csv(OUT/"financial_summary.csv").set_index("Metric").Value
    p=pd.read_csv(OUT/"portfolio_financials.csv"); e=pd.read_csv(OUT/"financial_exceptions.csv").sort_values("ForecastVariance",ascending=False)
    r=pd.read_csv(OUT/"risk_issue_register.csv"); a=pd.read_csv(OUT/"action_tracker.csv"); refresh=pd.read_csv(OUT/"refresh_control_log.csv").iloc[0]
    prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
    # 1
    s=prs.slides.add_slide(prs.slide_layouts[6]); title(s,"Financial Performance & Portfolio Governance","Executive management review | Historical synthetic reporting scenario")
    add_text(s,"11",.7,1.45,1.2,.6,34,BLUE,True); add_text(s,"synthetic programmes",.7,2.05,2.4,.3,12,GREY)
    add_text(s,"Executive summary",3.15,1.35,4,.3,17,NAVY,True)
    add_text(s,f"Forecast expenditure is {money(summary['Total forecast expenditure'])}, {money(summary['Portfolio forecast variance'])} above approved budget. Five programmes are Red forecast exceptions; two Red inherent risks and four overdue actions require governance attention.",3.15,1.85,7.8,1.25,16)
    add_text(s,f"Reporting date: {refresh.ReportingDate}\nProcessed: {refresh.ProcessingTimestampUTC}\nAll figures are illustrative and synthetic; they do not represent an organisation, client, employer or JPMorgan Chase.",3.15,3.55,7.8,1.1,12,GREY)
    footer(s)
    # 2
    s=prs.slides.add_slide(prs.slide_layouts[6]); title(s,"Portfolio financial position","Positive variance denotes additional cost versus approved budget")
    for i,(lab,key) in enumerate([("Approved budget","Total approved budget"),("Actual expenditure","Total actual expenditure"),("Forecast expenditure","Total forecast expenditure"),("Forecast overrun","Portfolio forecast variance"),("Budget utilisation","Budget utilisation")]): card(s,lab,(f"{summary[key]*100:.1f}%" if key=="Budget utilisation" else money(summary[key])),.45+i*2.55, RED if key=="Portfolio forecast variance" else BLUE)
    data=CategoryChartData(); data.categories=["Approved budget","Actual expenditure","Forecast expenditure"]; data.add_series("GBP",[summary["Total approved budget"],summary["Total actual expenditure"],summary["Total forecast expenditure"]])
    ch=s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(.65), Inches(2.75), Inches(6.1), Inches(3.65), data).chart; ch.has_legend=False; ch.value_axis.tick_labels.number_format="£#,##0"; ch.chart_title.has_text_frame=True; ch.chart_title.text_frame.text="Portfolio cost position (GBP)"
    add_text(s,f"Management commentary\nForecast expenditure exceeds approved budget by {money(summary['Portfolio forecast variance'])}. Actual spend is {summary['Budget utilisation']*100:.1f}% of budget; recovery plans should focus on the largest forecast drivers.",7.25,3.1,5.2,1.6,15)
    footer(s)
    # 3
    s=prs.slides.add_slide(prs.slide_layouts[6]); title(s,"Variance drivers","Five Red forecast exceptions, ranked by forecast variance")
    data=CategoryChartData(); data.categories=e.ProgrammeID.tolist(); data.add_series("Forecast variance",e.ForecastVariance.tolist())
    ch=s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(.55), Inches(1.25), Inches(6), Inches(5.5), data).chart; ch.has_legend=False; ch.value_axis.tick_labels.number_format="£#,##0"; ch.category_axis.reverse_order=True; ch.chart_title.has_text_frame=True; ch.chart_title.text_frame.text="Forecast variance (GBP)"
    rows=[[x.ProgrammeName, money(x.ForecastVariance), f"{x.ForecastVariancePct:.1%}", money(x.ForecastMovement)] for _,x in e.iterrows()]
    table(s,["Programme","Variance","Variance %","Movement"],rows,6.8,1.4,5.95,4.4,[2.8,1.05,1.0,1.1]); add_text(s,"Largest drivers: Core Integration Stabilisation (GBP 250,000) and Customer Case Routing Upgrade (GBP 140,000).",6.8,6.05,5.7,.45,11,GREY); footer(s)
    #4
    s=prs.slides.add_slide(prs.slide_layouts[6]); title(s,"Risk and issue exposure","Numerical inherent risk scoring is used for risks only; issues retain qualitative severity")
    risks=r[r.RecordType=="Risk"]; issues=r[r.RecordType=="Issue"]
    table(s,["Risk","Owner","L × I","Inherent","Residual","Mitigation status"],[[x.RiskID,x.Owner,f"{int(x.Likelihood)} × {int(x.Impact)}",x.RiskBand,x.ResidualRating,x.Status] for _,x in risks.iterrows()],.55,1.35,7.1,2.15,[.7,1.5,.7,1,1,2.2])
    table(s,["Issue","Owner","Severity","Status","Description"],[[x.RiskID,x.Owner,x.InherentRating,x.Status,x.RiskDescription] for _,x in issues.iterrows()],.55,4.05,11.9,1.35,[.8,1.5,1,1,7.6])
    add_text(s,"Risk matrix\nRed: 15–25\nAmber: 6–14\nGreen: 1–5\n\nTwo Red inherent risks are open.",8.25,1.5,3.4,1.9,16,NAVY,True); footer(s)
    #5
    s=prs.slides.add_slide(prs.slide_layouts[6]); title(s,"Governance status","Overdue and escalation statuses are intentionally reported separately")
    card(s,"Total overdue actions",str(int(summary["Overdue actions"])),.55,RED); card(s,"Open Red risks",str(int(summary["Open red risks"])),3.1,RED)
    status=a.Status.value_counts(); add_text(s,"Action status breakdown\n"+"\n".join(f"{k}: {v}" for k,v in status.items()),6.1,1.35,2.6,1.35,14,NAVY,True)
    overdue=a[a.Overdue.astype(str).str.lower()=="true"].sort_values("DueDate")
    table(s,["Action","Description","Owner","Due date","Escalation"],[[x.ActionID,x.ActionDescription,x.ActionOwner,pd.Timestamp(x.DueDate).strftime("%d %b %Y").lstrip("0"),"Yes" if str(x.EscalationFlag).lower()=="true" else "No"] for _,x in overdue.iterrows()],.55,3.05,12.1,2.7,[1,5.3,1.8,1.2,1.1]); footer(s)
    #6
    s=prs.slides.add_slide(prs.slide_layouts[6]); title(s,"Decisions and next steps","Recommendations are proposed actions, not implemented outcomes")
    recs=[["Approve supplier recovery capacity", "PRJ-005 red forecast variance and RISK-001", "Technology Director", "Critical", "30 Nov 2021"],["Confirm release path after defect triage", "PRJ-002 red forecast variance and RISK-002", "Technology Director", "Critical", "3 Dec 2021"],["Confirm pilot staffing roster", "ACT-004 overdue action", "Operations Director", "High", "29 Nov 2021"],["Escalate legal review capacity", "ACT-005 overdue action / ISSUE-002", "Customer Operations Head", "Medium", "1 Dec 2021"]]
    table(s,["Decision required","Business rationale","Accountable owner","Priority","Target date"],recs,.55,1.35,12.1,4.1,[2.65,3.6,2.1,1.2,1.55]); add_text(s,"Each recommendation is linked to a validated financial exception, risk, issue or action in the reporting outputs.",.65,5.95,10.8,.35,12,GREY); footer(s)
    DEST.parent.mkdir(exist_ok=True); prs.save(DEST); print(f"Created {DEST}")
if __name__ == "__main__": build()
