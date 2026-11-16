import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from financial_pipeline import prepare_actions, prepare_risks


def test_invalid_risk_inputs_are_flagged_not_scored():
    risks = pd.DataFrame({"RiskID":["R1"], "RecordType":["Risk"], "ProgrammeID":["P1"], "RiskDescription":["Test"], "Owner":["Owner"], "TargetDate":["2021-12-01"], "Status":["Open"], "Likelihood":[6], "Impact":[1]})
    output = prepare_risks(risks).iloc[0]
    assert pd.isna(output.RiskScore)
    assert output.RiskScoreValidation.startswith("Invalid")


def test_closed_action_is_not_overdue():
    actions = pd.DataFrame({"ActionID":["A1"], "ProgrammeID":["P1"], "ActionDescription":["Test"], "ActionOwner":["Owner"], "Priority":["Critical"], "DueDate":["2021-11-01"], "Status":["Closed"], "EscalationRequired":["Yes"]})
    output = prepare_actions(actions).iloc[0]
    assert not output.Overdue
    assert output.EscalationFlag
