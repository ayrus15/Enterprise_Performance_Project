# Monthly Reporting SOP

1. Confirm the approved reporting cut-off date in `config/project_config.json` and save any source replacement to `data/raw/` without modifying the original file.
2. Run the pipeline from the repository root: `& 'C:\Users\VAMSI\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/runPipeline.py`.
3. Review `outputs/qa/run_log.csv`, `qa_reconciliation.csv`, `exceptions.csv`, and `pipeline.log`. Stop publication for any `Fail` check.
4. Review the synthetic portfolio update dates, overdue actions, red risks, forecast-date changes, and budget variance. The status rules are project assumptions.
5. Build or refresh the workbook from processed outputs. Confirm dashboard figures reconcile to `outputs/processed/kpi_summary.csv`.
6. Update the presentation and decision memo using the same run ID and reporting date. Explicitly separate public retail findings from synthetic portfolio findings.
7. Archive the final workbook, presentation, memo, output files and QA evidence together.
