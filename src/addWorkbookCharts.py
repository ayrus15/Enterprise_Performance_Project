"""Fallback native-chart insertion after artifact-tool chart export failure."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".python_packages"))

from openpyxl import load_workbook
from openpyxl.chart import BarChart, LineChart, Reference


def main() -> None:
    path = ROOT / "workbook" / "Enterprise_Performance_Command_Center.xlsx"
    workbook = load_workbook(path)
    dashboard = workbook["Executive_Dashboard"]
    dashboard._charts = []

    trend = LineChart()
    trend.title = "Monthly gross positive sales (GBP)"
    trend.y_axis.title = "GBP"
    trend.x_axis.title = "Month"
    trend.style = 13
    trend.height, trend.width = 8, 15
    trend.add_data(Reference(dashboard, min_col=2, min_row=22, max_row=35), titles_from_data=True)
    trend.set_categories(Reference(dashboard, min_col=1, min_row=23, max_row=35))
    dashboard.add_chart(trend, "G21")

    status = BarChart()
    status.type = "bar"
    status.style = 10
    status.title = "Synthetic project status"
    status.x_axis.title = "Project count"
    status.y_axis.title = "Status"
    status.height, status.width = 8, 15
    status.add_data(Reference(dashboard, min_col=2, min_row=38, max_row=43), titles_from_data=True)
    status.set_categories(Reference(dashboard, min_col=1, min_row=39, max_row=43))
    dashboard.add_chart(status, "G38")
    workbook.save(path)
    print("Added 2 editable native charts")


if __name__ == "__main__":
    main()
