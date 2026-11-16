# Financial Reporting Methodology

All financial and governance data in this reporting extension is synthetic and illustrative. It does not represent any company, client, employer, or JPMorgan Chase data.

## Source and refresh controls

The four immutable input files are in `data/financial_raw/`: `programme_master.csv`, `financial_submissions.csv`, `risk_issue_register.csv`, and `corrective_actions.csv`. `src/financial_pipeline.py` validates and reads those files, then writes controlled reporting outputs to `outputs/financial/`.

The reporting date is 9 December 2021. Processing timestamp is recorded separately in `refresh_control_log.csv`; this is a historical synthetic reporting scenario, not a current-period performance report. Records Received means every row from the four source files. Programme Records Processed means the consolidated programme-level financial records.

## Financial definitions

- Budget variance = actual expenditure − approved budget.
- Forecast variance = forecast expenditure − approved budget.
- Budget utilisation = actual expenditure ÷ approved budget.
- Remaining budget = approved budget − actual expenditure.
- Forecast movement = forecast expenditure − previous forecast.

Positive cost variance denotes additional cost. Division by zero is reported as blank rather than a fabricated ratio. Forecast RAG assumptions are centrally stored in `config/settings.json`: Green ≤2%, Amber >2% and ≤5%, Red >5%.

## Governance definitions

Risk score equals likelihood × impact, with both inputs restricted to 1–5. Green is 1–5, Amber 6–14 and Red 15–25. Issues use qualitative severity and do not receive numerical scores. Inherent and residual ratings remain distinct. Risk escalation follows the configured inherent-score and ownership rules; action escalation is a separate source status.

An action is overdue only when its due date is earlier than the reporting date and it is not closed. Thus ACT-003 is not overdue but is escalated; ACT-005 is overdue but is not escalated.

## Data quality controls

Executed checks display an actual value, expected condition and status. The pipeline detects duplicate programme IDs and financial submissions, missing financial values, missing owners, open actions without due dates, invalid action dates and unknown programme references. A check is never labelled Pass merely because a value was omitted.
