import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from financial_pipeline import (calculate_financials, forecast_rag, prepare_actions,
                                prepare_risks, quality_checks, read_source, risk_band)


def programmes():
    return pd.DataFrame({"ProgrammeID": ["P1"], "ProgrammeName": ["Example"], "BusinessUnit": ["A"], "ProgrammeOwner": ["Owner"], "StartDate": ["2021-01-01"], "EndDate": ["2021-12-31"], "DeliveryStatus": ["On Track"], "RiskRating": ["Green"]})


def financials(budget=100, actual=110, forecast=106, previous=102):
    return pd.DataFrame({"ProgrammeID": ["P1"], "ApprovedBudget": [budget], "ActualExpenditure": [actual], "ForecastExpenditure": [forecast], "PreviousForecast": [previous], "ReportingPeriod": ["2021-12-09"]})


def test_financial_calculations_and_aggregation():
    row = calculate_financials(programmes(), financials()).iloc[0]
    assert (row.ApprovedBudget, row.ActualExpenditure, row.ForecastExpenditure) == (100, 110, 106)
    assert (row.BudgetVariance, row.ForecastVariance, row.ForecastMovement) == (10, 6, 4)
    assert row.BudgetUtilisation == 1.1


def test_zero_budget_and_missing_values_are_safe():
    zero = calculate_financials(programmes(), financials(budget=0)).iloc[0]
    assert pd.isna(zero.BudgetUtilisation) and pd.isna(zero.ForecastVariancePct)
    missing = calculate_financials(programmes(), financials(actual=None)).iloc[0]
    assert pd.isna(missing.BudgetVariance)


def test_forecast_rag_boundaries():
    assert forecast_rag(pd.Series([.02, .02001, .05, .05001])).tolist() == ["Green", "Amber", "Amber", "Red"]


def test_risk_score_boundaries_and_issues_are_not_scored():
    assert risk_band(pd.Series([5, 6, 14, 15, 25])).tolist() == ["Green", "Amber", "Amber", "Red", "Red"]
    data = pd.DataFrame({"RiskID": ["R", "I"], "RecordType": ["Risk", "Issue"], "ProgrammeID": ["P1", "P1"], "RiskDescription": ["x", "y"], "Owner": ["a", "b"], "TargetDate": ["2021-12-01", "2021-12-01"], "Status": ["Open", "Open"], "Likelihood": [5, None], "Impact": [5, None]})
    result = prepare_risks(data)
    assert result.loc[0, "RiskScore"] == 25 and pd.isna(result.loc[1, "RiskScore"])


def test_overdue_and_escalation_are_separate():
    actions = pd.DataFrame({"ActionID": ["ACT-003", "ACT-005"], "ProgrammeID": ["P1", "P1"], "ActionDescription": ["x", "y"], "ActionOwner": ["a", "b"], "Priority": ["High", "Medium"], "DueDate": ["2021-12-09", "2021-12-01"], "Status": ["Open", "In Progress"], "EscalationRequired": ["Yes", "No"]})
    result = prepare_actions(actions)
    assert result.Overdue.tolist() == [False, True]
    assert result.EscalationFlag.tolist() == [True, False]


def test_quality_checks_detect_duplicates_unknown_references_and_missing_owner():
    ps = programmes()
    fs = pd.concat([financials(), financials()], ignore_index=True)
    rs = pd.DataFrame({"RiskID": ["R"], "RecordType": ["Risk"], "ProgrammeID": ["UNKNOWN"], "RiskDescription": ["x"], "Owner": [None], "TargetDate": ["2021-12-01"], "Status": ["Open"], "Likelihood": [5], "Impact": [5]})
    ac = pd.DataFrame({"ActionID": ["A"], "ProgrammeID": ["P1"], "ActionDescription": ["x"], "ActionOwner": ["a"], "Priority": ["Low"], "DueDate": [None], "Status": ["Open"], "EscalationRequired": ["No"]})
    report = quality_checks(ps, fs, rs, ac)
    assert (report.Status == "Fail").sum() >= 4


def test_required_columns_and_empty_inputs_raise(tmp_path):
    (tmp_path / "bad.csv").write_text("ProgrammeID\nP1\n")
    with pytest.raises(ValueError, match="missing required columns"):
        read_source("bad.csv", ["ProgrammeID", "Owner"], tmp_path)
    (tmp_path / "empty.csv").write_text("ProgrammeID,Owner\n")
    with pytest.raises(ValueError, match="no records"):
        read_source("empty.csv", ["ProgrammeID", "Owner"], tmp_path)
