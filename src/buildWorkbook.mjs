import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = process.cwd();
const data = JSON.parse(await fs.readFile(`${root}/outputs/reports/workbook_data.json`, "utf8"));
const outPath = `${root}/workbook/Enterprise_Performance_Command_Center.xlsx`;
const wb = Workbook.create();
const navy = "#17365D", blue = "#1F4E78", lightBlue = "#D9EAF7", amber = "#FFF2CC", red = "#F4CCCC", green = "#D9EAD3", grey = "#F2F2F2";
const font = "Arial";

function addSheet(name) { const s = wb.worksheets.add(name); s.showGridLines = false; s.getRange("A1:Z200").format.font = { name: font, size: 10, color: "#1F1F1F" }; return s; }
function title(s, text, subtitle) { s.getRange("A2").values = [[text]]; s.getRange("A2").format.font = { name: font, size: 16, bold: true, color: navy }; s.getRange("A3").values = [[subtitle]]; s.getRange("A3").format.font = { name: font, size: 10, italic: true, color: "#666666" }; s.getRange("A4:Z4").format.borders = { bottom: { style: "thin", color: navy } }; }
function writeTable(s, start, matrix, name, widths = []) { const rows = matrix.length, cols = matrix[0].length; const startCell = s.getRange(start); const r0 = startCell.rowIndex, c0 = startCell.columnIndex; const range = s.getRangeByIndexes(r0, c0, rows, cols); range.values = matrix; const head = s.getRangeByIndexes(r0, c0, 1, cols); head.format = { fill: blue, font: { name: font, size: 10, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true }; range.format.verticalAlignment = "center"; range.format.borders = { preset: "outside", style: "thin", color: "#B7C9D6" }; s.tables.add(range, true, name); widths.forEach((w, i) => { s.getRangeByIndexes(r0, c0 + i, rows, 1).format.columnWidth = w; }); return range; }
function card(s, label, value, cell, fmt = "#,##0") { const anchor = s.getRange(cell); const r = s.getRangeByIndexes(anchor.rowIndex, anchor.columnIndex, 2, 1); r.values = [[label], [value]]; r.getRow(0).format = { fill: navy, font: { name: font, size: 9, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center" }; r.getRow(1).format = { fill: "#EAF1F8", font: { name: font, size: 14, bold: true, color: navy }, horizontalAlignment: "center", verticalAlignment: "center", numberFormat: fmt }; r.format.borders = { preset: "outside", style: "thin", color: navy }; r.getRow(1).format.rowHeight = 30; }
function findKpi(name) { const r = data.kpis.find(x => x[0] === name); return r ? Number(r[1]) : null; }

const readme = addSheet("ReadMe_Control");
title(readme, "Enterprise Performance Command Centre", "Independent business-management simulation | Public retail transactions and synthetic portfolio governance");
const readmeRows = [["Control", "Detail"], ["Reporting date", "2011-12-09"], ["Reporting period", "December 2010 to December 2011"], ["Source", "UCI Online Retail, CC BY 4.0; downloaded 2026-10-27"], ["Source file", "data/raw/Online Retail.xlsx (immutable)"], ["Latest pipeline run", data.runLog[1][0]], ["Run status", data.runLog[1][9]], ["Refresh instruction", "Run src/runPipeline.py, then src/prepareWorkbookData.py and src/buildWorkbook.mjs"], ["Synthetic-data warning", "All project, milestone, risk, issue, dependency and action data are simulated."], ["Positive-sales rule", "Excludes cancellation invoices, negative quantity, non-positive price and invalid date; retained in clean output."], ["Workbook detail", "Raw and clean transaction tabs show 100-row display subsets. Full files remain in data/raw and outputs/processed."], ["Status convention", "Green / On Track; Amber / At Risk; Red / Off Track. Thresholds are project assumptions."]];
writeTable(readme, "A6", readmeRows, "ReadMeTable", [24, 95]); readme.getRange("B14").format.fill = amber; readme.getRange("B15").format.fill = amber;

const dashboard = addSheet("Executive_Dashboard");
title(dashboard, "Executive Dashboard", "Public UCI retail results | Synthetic portfolio governance | Reporting date: 2011-12-09");
card(dashboard, "Gross positive sales (GBP)", findKpi("Gross positive sales value"), "A6", "£#,##0");
card(dashboard, "Eligible invoices", findKpi("Eligible invoice count"), "D6", "#,##0");
card(dashboard, "Cancellation rate", findKpi("Cancellation rate"), "G6", "0.0%");
card(dashboard, "At-risk / off-track projects", findKpi("At-risk or off-track projects"), "J6", "0");
card(dashboard, "Forecast budget variance (GBP)", findKpi("Forecast portfolio budget variance"), "A10", "£#,##0");
card(dashboard, "High-risk exposure", findKpi("High-risk exposure"), "D10", "0");
card(dashboard, "Pipeline status", data.runLog[1][9], "G10", "@");
card(dashboard, "QA warnings", Number(data.runLog[1][6]), "J10", "0");
dashboard.getRange("A14").values = [["Management attention"]]; dashboard.getRange("A14:D14").merge(); dashboard.getRange("A14:D14").format = { fill: navy, font: { name: font, size: 11, bold: true, color: "#FFFFFF" } };
dashboard.getRange("A15:D18").values = [["Priority item", "Evidence", "Owner role", "Due date"], ["Supplier recovery plan", "Risk score 25 on PRJ-005", "Engineering Manager", "2021-11-30"], ["Integration defect triage", "Risk score 20 on PRJ-002", "Product Manager", "2021-12-03"], ["Reporting test approval", "Compressed test window on PRJ-004", "Reporting Manager", "2021-12-09"]];
dashboard.getRange("A15:D15").format = { fill: blue, font: { name: font, bold: true, color: "#FFFFFF" } }; dashboard.getRange("A15:D18").format.borders = { preset: "outside", style: "thin", color: "#B7C9D6" };
writeTable(dashboard, "A22", data.monthlySales, "DashboardMonthlySales", [12, 20, 18, 18, 18]);
const trend = dashboard.charts.add("line", dashboard.getRange("A22:B35")); trend.title = "Monthly gross positive sales (GBP)"; trend.hasLegend = false; trend.titleTextStyle.typeface = font; trend.yAxis = { numberFormatCode: "£0.0,,\"M\"", numberFormatSourceLinked: false, textStyle: { typeface: font } }; trend.setPosition("G21", "N36");
dashboard.getRange("A38:B38").values = [["Status", "Project count"]]; dashboard.getRange("A39:B43").values = [["On Track", 4], ["At Risk", 3], ["Off Track", 2], ["Complete", 1], ["Not Started", 1]]; const statusChart = dashboard.charts.add("bar", dashboard.getRange("A38:B43")); statusChart.title = "Synthetic project status"; statusChart.hasLegend = false; statusChart.titleTextStyle.typeface = font; statusChart.setPosition("G38", "N52");
dashboard.getRange("A1:N55").format.columnWidth = 14; dashboard.getRange("A1:N55").format.wrapText = false;

const sales = addSheet("Sales_Pivots"); title(sales, "Sales Summary Tables", "Calculated from the full cleaned output using the documented positive-sales rule");
writeTable(sales, "A6", data.monthlySales, "MonthlySales", [12, 20, 18, 18, 18]);
writeTable(sales, "H6", data.countries, "CountryContribution", [22, 20, 16]);
writeTable(sales, "L6", data.products, "TopProducts", [15, 36, 20]);
writeTable(sales, "A24", data.customers, "TopCustomers", [18, 20, 16]);
writeTable(sales, "F24", data.completeness, "DataCompleteness", [26, 16]);
sales.getRange("B7:B19").format.numberFormat = "£#,##0"; sales.getRange("D7:D19").format.numberFormat = "0.0%"; sales.getRange("E7:E19").format.numberFormat = "£#,##0";

const portfolio = addSheet("Project_Portfolio"); title(portfolio, "Synthetic Project Portfolio", "Fictional projects for governance demonstration only"); writeTable(portfolio, "A6", data.portfolio, "ProjectPortfolio", [12, 34, 14, 22, 22, 12, 14, 15, 15, 15, 14, 14, 14, 14, 13, 11, 26, 15, 22, 14, 48, 16, 14, 16, 14]); portfolio.freezePanes.freezeRows(6); portfolio.getRange("A7:Y17").format.wrapText = true; portfolio.getRange("J7:N17").format.numberFormat = "£#,##0"; portfolio.getRange("O7:O17").format.numberFormat = "0.0%"; portfolio.getRange("V7:V17").format.numberFormat = "0.0%"; portfolio.getRange("W7:W17").format.numberFormat = "£#,##0";
portfolio.getRange("P7:P17").conditionalFormats.add("containsText", { text: "Off Track", format: { fill: red, font: { bold: true, color: "#9C0006" } } }); portfolio.getRange("P7:P17").conditionalFormats.add("containsText", { text: "At Risk", format: { fill: amber, font: { bold: true, color: "#7F6000" } } });

const milestones = addSheet("Milestones"); title(milestones, "Synthetic Milestone Register", "Forecast and actual completion dates remain separate"); writeTable(milestones, "A6", data.milestones, "MilestoneRegister", [16, 12, 34, 15, 15, 15, 16, 22, 30, 18]); milestones.freezePanes.freezeRows(6); milestones.getRange("A7:J28").format.wrapText = true;

const risks = addSheet("Risks_Actions"); title(risks, "Synthetic Risks, Issues, Dependencies and Actions", "Risk scores only apply where probability and impact are provided"); writeTable(risks, "A6", data.risks, "RisksActions", [14, 14, 12, 30, 50, 12, 12, 12, 12, 22, 14, 14, 14, 45, 16, 14, 12]); risks.freezePanes.freezeRows(6); risks.getRange("A7:Q14").format.wrapText = true; risks.getRange("H7:H14").conditionalFormats.add("cellIs", { operator: "greaterThanOrEqual", formula: 15, format: { fill: red, font: { bold: true, color: "#9C0006" } } });

const qa = addSheet("QA_Reconciliation"); title(qa, "QA and Reconciliation", "Terminal reporting controls. Warnings remain visible and do not feed business metrics."); writeTable(qa, "A6", data.qa, "QAChecks", [20, 48, 14, 14, 14, 16]); writeTable(qa, "A18", data.runLog, "RunLog", [28, 30, 24, 16, 16, 18, 14, 14, 20, 18, 80]); qa.getRange("C7:C13").conditionalFormats.add("containsText", { text: "Warning", format: { fill: amber, font: { bold: true, color: "#7F6000" } } }); qa.getRange("C7:C13").conditionalFormats.add("containsText", { text: "Fail", format: { fill: red, font: { bold: true, color: "#9C0006" } } });

const raw = addSheet("Raw_Transactions"); title(raw, "Raw Transaction Display Subset", "First 100 records shown. Immutable full source: data/raw/Online Retail.xlsx"); writeTable(raw, "A6", data.rawTransactions, "RawTransactions", [15, 15, 38, 12, 22, 14, 15, 24]); raw.freezePanes.freezeRows(6);
const clean = addSheet("Clean_Transactions"); title(clean, "Clean Transaction Display Subset", "First 100 records shown. Full clean data: outputs/processed/clean_transactions.csv"); writeTable(clean, "A6", data.cleanTransactions, "CleanTransactions", [15, 15, 34, 12, 22, 14, 15, 22, 22, 12, 15, 16, 16, 18, 16, 24]); clean.freezePanes.freezeRows(6);

const dict = addSheet("KPI_Dictionary"); title(dict, "KPI Dictionary", "Definitions align to src/runPipeline.py and the reporting outputs"); const dictRows = [["KPI", "Business purpose", "Formula", "Grain", "Inclusion rule", "Source fields", "Refresh", "Owner role", "Limitation"], ["Gross positive sales value", "Positive retail sales view", "Sum LineValue", "Transaction line", "IsValidForSalesAnalysis", "Quantity, UnitPrice", "Each run", "Reporting Manager", "Retail data only"], ["Cancellation value", "Monitor cancellations", "Absolute cancellation LineValue", "Transaction line", "IsCancellation", "InvoiceNo, Quantity, UnitPrice", "Each run", "Reporting Manager", "No original-sale matching"], ["Net transaction value", "Signed transaction result", "Sum LineValue", "Transaction line", "All signed lines", "Quantity, UnitPrice", "Each run", "Reporting Manager", "Different from gross positive sales"], ["Average order value", "Invoice size", "Gross sales / eligible invoices", "Invoice", "Eligible positive sales", "InvoiceNo, LineValue", "Each run", "Reporting Manager", "Excludes cancellations"], ["Top 10 customer concentration", "Customer dependency", "Top 10 sales / gross sales", "Customer", "CustomerID present", "CustomerID, LineValue", "Each run", "Commercial Lead", "Missing IDs excluded"], ["Schedule variance", "Delivery outlook", "Forecast end - baseline end", "Project", "Both dates present", "Project dates", "Monthly", "Delivery Manager", "Synthetic only"], ["Forecast budget variance", "Budget outlook", "Forecast cost - budget", "Project", "Valid budget", "Cost fields", "Monthly", "Finance Controls Lead", "Synthetic only"], ["Overdue actions", "Management follow-up", "Open action due before cut-off", "Action", "Open synthetic actions", "DueDate, Status", "Monthly", "Action owner", "Fixed reporting date"], ["High-risk exposure", "Escalation priority", "Open risks with score >=15", "Risk", "Score threshold is assumption", "Probability, Impact", "Monthly", "Risk and Controls Lead", "Synthetic threshold"]]; writeTable(dict, "A6", dictRows, "KpiDictionary", [28, 26, 34, 16, 30, 28, 14, 24, 32]); dict.getRange("A7:I16").format.wrapText = true;

for (const s of wb.worksheets.items) { s.getUsedRange().format.verticalAlignment = "center"; }
wb.recalculate();
const xlsx = await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(outPath);
console.log(`Created ${outPath}`);
