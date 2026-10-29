# Executive Recommendation Memo

**Report:** Enterprise Performance, Portfolio Governance and Automated Reporting System
**Reporting period (transactions):** 2010-12-01 to 2011-12-09, UCI Online Retail dataset
**Portfolio cut-off (synthetic):** 2011-12-09 (`config/project_config.json`)
**Run ID:** see `outputs/qa/run_log.csv` for the latest pipeline execution
**Prepared by:** Independent portfolio analyst (fictional "Analyst" role for this exercise)

This is an independent, self-directed portfolio project. It is not affiliated with,
commissioned by, or representative of JPMorgan Chase or any employer. All project,
owner, budget, milestone, risk and action records are synthetic examples created
for demonstration; the retail transaction figures come from the public UCI Online
Retail dataset and describe historical UK retail activity, not current or audited
revenue.

## 1. Purpose

To give a fictional leadership team one reconciled view of (a) retail transaction
performance over the analysis period and (b) the status of a synthetic delivery
portfolio, with explicit decisions requested where the data indicates risk.

## 2. Executive summary

- Gross positive transaction value across the period was **GBP 10,666,685** on
  **19,960** eligible invoices. Cancellations reduced this by **GBP 896,812**
  (14.8% of invoices).
- United Kingdom customers contributed **84.6%** of gross positive sales; the
  top 10 identified customers account for **14.4%** of that total.
- Of 11 synthetic programmes, **2 are Red** (Off Track) and **3 are Amber**
  (At Risk), with a combined forecast cost overrun of **GBP 439,000** against
  approved budget.
- **2 open risks** exceed the project's high-risk threshold (score >= 15 of 25);
  both sit on the two Red technology programmes.
- Four decisions are requested from leadership this cycle (Section 8).

## 3. Key findings

| # | Finding | Evidence | Limitation |
|---|---|---|---|
| 1 | Sales are heavily UK-concentrated | UK = 84.6% of gross positive sales (`outputs/processed/country_contribution.csv`) | Country is customer-supplied residence, not a verified shipping record |
| 2 | Cancellations are material but not reconciled to the original sale | Cancellation value GBP 896,812; 14.8% of invoices (`kpi_summary.csv`) | The dataset does not link a cancellation line back to its original invoice |
| 3 | A meaningful share of sales has no identified customer | CustomerID populated for 75.1% of rows (`data_completeness.csv`) | Missing IDs are kept missing by design; customer-level analysis excludes them rather than inferring an identity |
| 4 | 10,147 duplicate-candidate rows remain unresolved | QA_Reconciliation flags this as a Warning, not a Fail | No business rule yet distinguishes legitimate repeat orders from true duplicates |
| 5 | Two Critical/High-priority technology programmes are Off Track with unresolved high-scoring risks | PRJ-002 and PRJ-005, RAGStatus = Red, RiskScore 20 and 25 (`project_portfolio.csv`, `risks_actions.csv`) | Portfolio is synthetic; findings describe the simulation's internal consistency, not a real delivery organisation |

## 4. Risks and implications

- **PRJ-005 (Core Integration Stabilisation):** forecast delay of 87 days and a
  forecast budget overrun of GBP 250,000, driven by an external supplier defect
  backlog (risk score 25, Blocked, escalation required).
- **PRJ-002 (Customer Case Routing Upgrade):** forecast delay of 44 days and a
  forecast overrun of GBP 140,000, driven by unresolved integration test
  failures (risk score 20, In Progress, escalation required).
- Left unaddressed, both risks compound: PRJ-004 depends on PRJ-003, and the
  portfolio's two largest programmes by budget (PRJ-002, PRJ-005) also carry
  its only two high-risk-threshold risks, concentrating delivery risk in the
  Technology workstream.
- The duplicate-row and cancellation-linkage limitations mean any customer- or
  order-level metric derived from this dataset should be treated as a
  reporting-method demonstration, not an audited transaction record.

## 5. Options considered

1. **Do nothing this cycle** — rejected; the combined forecast overrun (GBP
   439,000) and two unresolved high-scoring risks would carry into the next
   reporting period without a documented decision.
2. **Escalate only the two Red programmes** — partial fix; leaves the
   duplicate-row and decision-backlog issues open.
3. **Address the two Red programmes, the open decision backlog, and the
   duplicate-row disposition rule together** — selected; each item has clear
   evidence, an identifiable owner role, and a bounded effort estimate.

## 6. Recommended actions

| Recommendation | Evidence | Expected benefit (estimate) | Effort / dependency | Risk if deferred | Owner role | Target date | Success measure |
|---|---|---|---|---|---|---|---|
| Convene a recovery review for PRJ-002 and PRJ-005 | Both Red; combined forecast overrun GBP 390,000 of the portfolio's GBP 439,000 total | Estimated reduction in further schedule slippage; not a guaranteed saving | Medium; needs supplier and engineering capacity | Continued overrun and risk score growth | Technology Director | +10 business days | Agreed recovery plan with revised forecast dates recorded in `project_portfolio.csv` |
| Document a duplicate-row disposition rule | 10,147 duplicate candidates retained, unresolved (Warning in QA_Reconciliation) | Removes one open Warning from QA sign-off | Low; policy decision, not a technical rebuild | Metrics remain ambiguous on repeat-order treatment | Data Governance Lead | +15 business days | Rule published in `METHODOLOGY_AND_LIMITATIONS` equivalent and applied in the next pipeline run |
| Review cancellation drivers by product and country | Cancellation value GBP 896,812 (14.8% of invoices) | Better-targeted root-cause action in the next cycle (estimate only) | Medium; needs a follow-up cut of `Clean_Transactions` | Cancellation rate stays unexplained | Analyst (this role) | +15 business days | Driver findings added to the next monthly review |
| Close the open decision backlog | 4 open escalation items without a confirmed owner/date at memo time | Clears the backlog measure to zero | Low; requires sponsor sign-off, not new analysis | Decisions continue rolling over between cycles | Respective project sponsors | +5 business days | Zero open escalation items without an owner and date in `risks_actions.csv` |
| Re-baseline the PRJ-008 legal-review dependency | Forecast slip of 14 days tied to an overdue legal review | Restores a credible forecast date for one Amber programme | Low; single-dependency fix | Forecast date understates true risk | Customer Operations Head | +10 business days | Revised `ForecastEndDate` agreed and recorded |

## 7. Assumptions and limitations

- UCI Online Retail describes a UK-based non-store retailer's historical
  transactions (Dec 2010-Dec 2011); it is used only to demonstrate analytical
  method and is not current or company transaction data.
- The 11-project portfolio, its owners, budgets, milestones, risks and actions
  are entirely synthetic and created for this exercise.
- The portfolio reporting cut-off (2011-12-09) is aligned to the transaction
  period rather than to a current date. Under this cut-off, synthetic
  milestone and action due dates fall after the cut-off, so overdue-milestone
  and overdue-action counts are 0 in this cycle; this is a documented artefact
  of the chosen cut-off, not a claim that no items can ever be overdue.
- "Sales" and "transaction value" are retail measures, not audited revenue or
  profit; no cost-of-goods data is available in this dataset.
- High-risk threshold (score >= 15 of 25) is a project assumption, documented
  in `config/project_config.json` and `docs/kpi_definitions.md`, not an
  industry standard.

## 8. Decisions requested

| Decision | Decision owner role | Deadline | Next reporting checkpoint |
|---|---|---|---|
| Approve recovery capacity for the PRJ-005 supplier defect backlog | Technology Director | +10 business days | Next monthly review |
| Approve a constrained user-acceptance-test plan for PRJ-004 | Finance Controls Lead | +5 business days | Next monthly review |
| Approve the duplicate-row disposition rule | Data Governance Lead | +15 business days | Next monthly review |
| Approve escalation of the PRJ-008 legal review | Customer Operations Head | +10 business days | Next monthly review |

## 9. Owners and next steps

All five recommended actions have a named role, target date and success
measure in Section 6. The reporting SOP (`docs/monthly_reporting_sop.md`)
governs how these items are tracked into the next cycle: each must be
reflected in the next pipeline run's `project_portfolio.csv` and
`risks_actions.csv` before the next memo is issued, and the QA
reconciliation (`outputs/qa/qa_reconciliation.csv`) must show no new
unexplained variance.
