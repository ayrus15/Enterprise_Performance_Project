# KPI Definitions

| KPI | Formula and grain | Inclusion rules | Limitation |
|---|---|---|---|
| Gross positive sales value | Sum `LineValue`, line grain | `IsValidForSalesAnalysis = True` | Retail metric; does not represent banking revenue. |
| Cancellation value | Absolute sum of cancellation `LineValue`, line grain | `IsCancellation = True` | Cancellation link to original sale is not reconstructed. |
| Net transaction value | Sum signed `LineValue`, line grain | All records with usable numeric values | Includes transactions outside positive-sales view. |
| Monthly sales growth | Current month gross sales / prior month gross sales - 1 | Positive-sales monthly totals | N/A where prior month is unavailable or zero. |
| Eligible invoice count | Distinct InvoiceNo | Positive-sales view | Invoice-level metric differs from line count. |
| Average order value | Gross positive sales / eligible invoices | Positive-sales view | Does not include cancellations. |
| Top 10 customer concentration | Top 10 customer gross sales / gross positive sales | CustomerID present; positive-sales view | Missing IDs excluded. |
| Cancellation rate | Cancellation invoice count / all invoice count | Defined cancellation rule | Invoice rather than line denominator. |
| Country contribution | Country gross sales / total gross sales | Positive-sales view | Country is customer residence as supplied. |
| Forecast budget variance | ForecastCost - Budget | Synthetic projects with budget | Positive means forecast overspend. |
| Schedule variance | ForecastEndDate - BaselineEndDate | Synthetic projects with both dates | Positive means forecast delay. |
| Overdue actions | Open action due before reporting date | Synthetic action records only | Uses fixed reporting cut-off. |
| High-risk exposure | Open risks where score >= 15 | Synthetic risk records | 15 is a project assumption, not an industry standard. |
