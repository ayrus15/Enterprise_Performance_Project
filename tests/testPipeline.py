import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from runPipeline import cleanTransactions, makePortfolio


def testCancellationAndNegativeAreTraceable():
    source = pd.DataFrame({"InvoiceNo": ["C100", "200"], "StockCode": ["A", "B"], "Description": ["x", "y"], "Quantity": [-1, 2], "InvoiceDate": ["2011-01-01", "2011-01-02"], "UnitPrice": [2, 3], "CustomerID": [1, 2], "Country": ["UK", "UK"]})
    clean = cleanTransactions(source)
    assert clean.loc[0, "IsCancellation"]
    assert not clean.loc[0, "IsValidForSalesAnalysis"]
    assert clean.loc[1, "IsValidForSalesAnalysis"]


def testCompletedProjectConsistency():
    portfolio, _, _ = makePortfolio(pd.Timestamp("2011-12-09"))
    completed = portfolio[portfolio.Status == "Complete"]
    assert (completed.PercentComplete == 1).all()
    assert completed.ActualEndDate.notna().all()
