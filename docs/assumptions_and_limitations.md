# Assumptions and Limitations

- UCI Online Retail represents a UK-based non-store retailer and is used only to demonstrate analytical method.
- Invoice numbers beginning with `C` indicate cancellations, following UCI metadata.
- Positive-sales analysis excludes cancellations, negative quantities, non-positive price, and unparseable dates. These rows remain in clean output and reconciliation.
- Missing CustomerID values remain in sales totals but are excluded from customer concentration.
- Reporting date is a configurable simulation cut-off, initially 2011-12-09 for alignment with the transaction source period.
- The 11-project portfolio, milestones, budget values, owners, risks, actions, status thresholds, and dates are synthetic.
- The workbook may use a documented transaction subset for detailed display to preserve usability; full raw and clean data remain in `data/raw` and `outputs/processed`.
