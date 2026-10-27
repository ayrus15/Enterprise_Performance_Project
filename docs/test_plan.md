# Test Plan

| Test | Expected result |
|---|---|
| Missing required source column | Pipeline raises a visible critical schema error. |
| Cancellation invoice | Retained; `IsCancellation=True`; excluded from positive-sales view. |
| Negative quantity | Retained and flagged; excluded from positive-sales view. |
| Zero denominator | Growth or utilisation returns N/A or is not calculated; no divide-by-zero value. |
| Duplicate candidate | Retained and counted in QA. |
| Invalid date | Flagged and visible in QA. |
| Completed project | Requires 100% progress and an actual end date. |
| Budget overrun | Positive forecast budget variance is visible. |
| Overdue action | Open action before reporting date is counted. |
