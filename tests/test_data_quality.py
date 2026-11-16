import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from financial_pipeline import quality_checks


def test_invalid_action_date_is_reported_as_failed_executed_check():
    programmes = pd.DataFrame({"ProgrammeID":["P1"], "ProgrammeOwner":["Owner"]})
    financials = pd.DataFrame({"ProgrammeID":["P1"], "ApprovedBudget":[1], "ActualExpenditure":[1], "ForecastExpenditure":[1], "PreviousForecast":[1]})
    risks = pd.DataFrame({"ProgrammeID":["P1"], "Owner":["Owner"]})
    actions = pd.DataFrame({"ProgrammeID":["P1"], "Status":["Open"], "DueDate":["not-a-date"]})
    check = quality_checks(programmes, financials, risks, actions).query("Check == 'Invalid action dates'").iloc[0]
    assert check.Status == "Fail"
    assert check.ExecutionStatus == "Executed"
