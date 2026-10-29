# Portfolio Case Study: Enterprise Performance & Delivery Office

## 1. Title

Enterprise Performance, Portfolio Governance and Automated Reporting System

## 2. Project type

Independent business management and executive reporting portfolio project.
Not affiliated with, commissioned by, or representative of JPMorgan Chase or
any employer.

## 3. Business question

What should a fictional leadership team monitor, investigate, and decide each
reporting cycle, given a public transaction dataset and a simulated delivery
portfolio?

## 4. Problem framing

Organisations often run separate, inconsistent spreadsheets for sales
performance and for project delivery status, which makes it hard for
leadership to see where attention and decisions are actually needed. This
project simulates a single reconciled reporting system that answers that
question for both a transactional dataset and a project portfolio, using the
same KPI definitions, QA checks, and review cadence for both.

## 5. Approach

1. Preserve the raw UCI Online Retail source unchanged and profile it before
   any cleaning (`src/runPipeline.py`, `docs/data_dictionary.md`).
2. Build a repeatable, configuration-driven cleaning and KPI pipeline that
   documents every inclusion/exclusion rule (`docs/assumptions_and_limitations.md`,
   `docs/kpi_definitions.md`).
3. Design a clearly labelled synthetic project, milestone, risk, and action
   portfolio with varied statuses and realistic dependencies.
4. Generate an Excel command centre, a ten-slide executive deck, and an
   executive memo directly from the same reconciled pipeline outputs, so no
   figure is typed by hand into more than one place.
5. Run QA and reconciliation checks against both the transaction data and the
   portfolio data before treating any finding as reportable.

## 6. Data sources

- **Real data:** Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine
  Learning Repository. https://doi.org/10.24432/C5BW33. CC BY 4.0. Historical
  UK-based online retail transactions, 2010-12-01 to 2011-12-09.
- **Synthetic data:** 11 fictional projects, their milestones, risks, and
  actions, created for this exercise. They do not represent an actual
  organisation, and no real individuals are named.

## 7. Deliverables

- `workbook/Enterprise_Performance_Command_Center.xlsx` — ten-sheet Excel
  command centre (control notes, raw and clean transactions, sales pivots,
  executive dashboard, project portfolio, milestones, risks/actions, QA
  reconciliation, KPI dictionary).
- `presentation/Monthly_Business_Performance_Review.pptx` — ten-slide
  executive review generated from the same reconciled outputs.
- `docs/executive_recommendation_memo.md` — recommendation memo with evidence,
  owners, dates, and decisions requested.
- `docs/monthly_reporting_sop.md`, `docs/kpi_definitions.md`,
  `docs/data_dictionary.md`, `docs/assumptions_and_limitations.md`,
  `docs/qa_checklist.md` — governance and process documentation.
- `src/runPipeline.py`, `src/prepareWorkbookData.py`, `src/buildWorkbook.mjs`,
  `src/addWorkbookCharts.py`, `src/buildPresentation.py` — the reproducible
  build chain, plus `tests/testPipeline.py`.

## 8. Key findings

- Gross positive transaction value was GBP 10,666,685 across 19,960 eligible
  invoices for the analysis period; cancellations reduced this by GBP 896,812
  (14.8% of invoices).
- Sales are heavily concentrated: the United Kingdom contributed 84.6% of
  gross positive sales, and the top 10 identified customers contributed 14.4%
  of that total.
- 75.1% of transaction rows carry a CustomerID; the remainder are kept in
  sales totals but excluded from customer-level analysis, per the project's
  data-integrity rules.
- In the synthetic portfolio, 2 of 11 projects are Red (Off Track) and 3 are
  Amber (At Risk), with a combined forecast cost overrun of GBP 439,000; two
  open risks exceed the documented high-risk threshold (score >= 15 of 25),
  and both sit on the two Red programmes.
- All findings and the reconciliation checks that support them are listed in
  `outputs/qa/qa_reconciliation.csv` and `docs/executive_recommendation_memo.md`.

## 9. Recommendations

See `docs/executive_recommendation_memo.md` Section 6 for the full,
evidence-linked list. In priority order: stabilise the two Red technology
programmes, document a duplicate-row disposition rule, review cancellation
drivers, close the open decision backlog, and re-baseline one Amber
programme's dependency.

## 10. Controls

- Reconciliation: `outputs/qa/qa_reconciliation.csv` checks schema
  completeness, raw-to-clean row parity, date parsing, duplicate retention,
  sales-eligibility traceability, and portfolio referential integrity.
- Refresh process: `docs/monthly_reporting_sop.md` defines the run order,
  required QA review before publication, and what must be archived together.
- Status rules: RAG thresholds, high-risk scoring, and stale-update rules are
  documented as project assumptions in `docs/kpi_definitions.md` and
  `config/project_config.json`, not presented as industry standards.
- Automated tests: `tests/testPipeline.py` exercises the cleaning and KPI
  logic; results are logged under `outputs/qa/`.

## 11. Limitations

- The transaction data is historical UK retail data (Dec 2010-Dec 2011), not
  current activity, banking data, or audited revenue; no cost-of-goods data
  is available, so no profit figure is calculated or implied.
- The entire project portfolio — projects, owners, budgets, milestones,
  risks, and actions — is synthetic.
- The portfolio's reporting cut-off is aligned to the transaction period
  rather than to a current date; under that cut-off, every synthetic due date
  falls after the cut-off, so overdue-action and overdue-milestone counts are
  0 this cycle. This is a disclosed artefact of the configuration, not a
  claim that the simulated portfolio can never run late.
- 10,147 duplicate-candidate transaction rows remain retained and unresolved
  pending a documented business rule.
- This project has not been deployed in any organisation and does not claim
  real financial savings, stakeholder adoption, or business impact.

## 12. Review and iteration

No formal external review has been recorded for this cycle. If a peer,
mentor, or professional reviews the workbook or presentation, their feedback
and the resulting changes will be added here rather than claimed in advance.

## 13. What I learned

- Reconciling a public transactional dataset to formula-driven KPIs surfaces
  data-quality issues (missing IDs, duplicate rows, unlinked cancellations)
  that are easy to overlook if a dashboard is built directly from a
  spreadsheet pivot without a documented inclusion rule for every number.
- Keeping real and synthetic data in clearly separated tables and documents —
  rather than blending them into one narrative — made it straightforward to
  disclose which findings are evidence-based and which are simulation
  assumptions.
- Generating the presentation and memo programmatically from the same
  `outputs/processed/*.csv` files the workbook uses removed an entire class
  of "the deck doesn't match the dashboard" risk.

## 14. Links or screenshots

See `workbook/Enterprise_Performance_Command_Center.xlsx` and
`presentation/Monthly_Business_Performance_Review.pptx` in this repository
for the finished artefacts.
