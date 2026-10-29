# QA Checklist

Run this checklist before publishing a reporting cycle. Each item should be
verifiable from a file in this repository, not asserted from memory.

- [x] Source citation and licence included (`README.md`, UCI Online Retail, CC BY 4.0, DOI 10.24432/C5BW33).
- [x] Dataset period and actual row count recorded (`README.md`, `docs/assumptions_and_limitations.md`; 541,909 raw rows, `outputs/qa/qa_reconciliation.csv`).
- [x] Raw data preserved unchanged (`data/raw/Online Retail.xlsx` is read-only input to `src/runPipeline.py`; never written by the pipeline).
- [x] Missing values and cancellations handled transparently (`docs/assumptions_and_limitations.md`; `outputs/qa/exceptions.csv`).
- [x] Derived-field definitions documented (`docs/data_dictionary.md`, `docs/kpi_definitions.md`).
- [x] Headline metrics independently recalculated and reconciled (`outputs/qa/qa_reconciliation.csv`: raw row count, clean row count, duplicate count, and portfolio referential-integrity checks all Pass or explained Warning).
- [x] Distinct invoice and customer counts verified (`outputs/processed/kpi_summary.csv`; `outputs/processed/data_completeness.csv`).
- [x] No unexplained row-count or reconciliation difference (`outputs/qa/qa_reconciliation.csv`; the one Warning — 10,147 duplicate candidates — is explained, not hidden, in `docs/executive_recommendation_memo.md` Section 3).
- [x] Dashboard refresh works (workbook KPI, pivot, and chart sheets are generated from `outputs/processed/*.csv` by `src/prepareWorkbookData.py` and `src/buildWorkbook.mjs`, not hand-typed).
- [x] Filters, slicers, and formulas work (workbook `Project_Portfolio`, `Risks_Actions`, and `QA_Reconciliation` sheets carry structured tables and status-based conditional formatting built by the same scripts).
- [x] Synthetic project data clearly labelled (`ReadMe_Control` sheet; `README.md`; `docs/assumptions_and_limitations.md`; every synthetic-data section in this memo and presentation).
- [x] Project references and dates validated (`outputs/qa/qa_reconciliation.csv`: unique project IDs = 11; completed projects have 100% progress and an actual end date).
- [x] RAG status rules consistently applied (`docs/kpi_definitions.md`; RAG values in `outputs/processed/project_portfolio.csv` match the Amber/Red thresholds used in the presentation and memo).
- [x] Risks and actions have owners and due dates (`outputs/processed/risks_actions.csv`).
- [x] Presentation conclusions trace to evidence (every slide footer in `presentation/Monthly_Business_Performance_Review.pptx` names its source file; built by `src/buildPresentation.py` directly from `outputs/processed/*.csv`, not typed by hand).
- [x] Recommendations distinguish estimates from facts (`docs/executive_recommendation_memo.md` Section 6 labels each benefit as an estimate).
- [x] Memo and SOP agree with workbook definitions (`docs/executive_recommendation_memo.md`, `docs/monthly_reporting_sop.md`, and `docs/kpi_definitions.md` use the same KPI names and formulas; cross-checked manually for this cycle).
- [ ] File names, links, and references are correct — re-check before each external distribution; not yet independently re-verified for this cycle.
- [x] Confidential data is not included (dataset is public; portfolio is synthetic; no real names, emails, or identifiers appear anywhere in the repository).
- [x] Public case study includes limitations (`docs/portfolio_case_study.md` Section 11).
- [ ] Final version is backed up — pending: push this branch to `origin` after this cycle's commits.

## Known open items carried into the next cycle

1. Duplicate-row disposition rule not yet documented as a formal business
   rule (tracked as a decision request in the memo).
2. Overdue-action and overdue-milestone counts are 0 this cycle because the
   portfolio reporting cut-off (2011-12-09) sits before every synthetic due
   date; this is a documented limitation, not a verified "on time" claim —
   see `docs/assumptions_and_limitations.md`.
3. No independent peer review has been recorded for this cycle. If one is
   obtained, record it in `docs/portfolio_case_study.md` Section 12 rather
   than implying it occurred.
