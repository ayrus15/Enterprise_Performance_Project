# Data Dictionary

## Source provenance

The public retail source is **Online Retail.xlsx**, downloaded on 2026-10-27 from the [UCI Online Retail dataset page](https://archive.ics.uci.edu/dataset/352/online+retail). UCI identifies 541,909 instances, 8 fields, a 2010-12-01 to 2011-12-09 retail transaction period, and a CC BY 4.0 licence. Citation: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. DOI: 10.24432/C5BW33.

The source remains immutable in `data/raw/Online Retail.xlsx`. It is retail data, not banking data.

## Transaction fields

| Field | Source or derived | Rule |
|---|---|---|
| InvoiceNo | Source | Text. A value beginning `C` identifies a cancellation. |
| StockCode | Source | Text product code. |
| Description | Source | Trimmed text description. |
| Quantity | Source | Signed numeric quantity. Negative values remain traceable. |
| InvoiceDate | Source | Original source value. |
| UnitPrice | Source | Signed numeric price in sterling. |
| CustomerID | Source | Identifier; missing values are retained. |
| Country | Source | Trimmed country text. |
| InvoiceDateParsed | Derived | Parsed datetime; parsing failures receive a quality flag. |
| YearMonth | Derived | `YYYY-MM` from parsed invoice date. |
| LineValue | Derived | `Quantity * UnitPrice`. |
| IsCancellation | Derived | Invoice number starts with `C`, case-insensitive. |
| IsNegativeQuantity | Derived | `Quantity < 0`. |
| IsZeroOrNegativePrice | Derived | `UnitPrice <= 0`. |
| IsMissingCustomer | Derived | `CustomerID` is missing. |
| IsValidForSalesAnalysis | Derived | Not cancellation, not negative quantity, positive price, valid date and valid quantity. |
| DataQualityFlags | Derived | Semicolon-separated transparent flags. |

## Synthetic governance fields

`Project_Portfolio`, `Milestones`, and `Risks_Actions` are fictional simulated data. They are never company or client data. Project IDs are stable keys. Schedule variance is `ForecastEndDate - BaselineEndDate`; a positive number indicates delay. Forecast budget variance is `ForecastCost - Budget`; a positive number indicates overspend. RiskScore only applies to risk records and equals `Probability * Impact`.
