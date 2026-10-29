# Synthetic portfolio data

> The project portfolio, owners, budgets, risks, milestones, and actions in
> this folder are synthetic examples created for demonstration. They do not
> represent an actual organisation, and no real individuals are named.

These four files are a static, committed snapshot of the fictional project
portfolio defined in `src/runPipeline.py` (`makePortfolio`):

- `projects.csv` — 11 fictional initiatives with workstream, owner role,
  budget, forecast, RAG status, and derived schedule/budget variance.
- `milestones.csv` — baseline/forecast/actual dates and status for each
  project's milestones.
- `risks.csv` — open and closed risk records, with probability, impact, and
  calculated risk score.
- `actions.csv` — issues, dependencies, and actions tracked against the
  portfolio (everything that isn't a `Risk` record type).

They are regenerated (and must stay identical to this snapshot) by:

```powershell
& 'C:\Users\VAMSI\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/exportSyntheticData.py
```

The authoritative source is the Python code in `src/runPipeline.py`, not
these CSVs — if you change the portfolio definition there, re-run the export
script to refresh this folder. The same `makePortfolio` function also feeds
`outputs/processed/project_portfolio.csv`, `milestones.csv`, and
`risks_actions.csv` (gitignored, regenerated on every pipeline run), and in
turn the workbook, presentation, and memo.
