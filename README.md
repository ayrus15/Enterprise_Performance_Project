# Enterprise Performance, Portfolio Governance and Automated Reporting System

An independent portfolio simulation that combines analysis of the public UCI Online Retail dataset with a clearly labelled synthetic delivery portfolio. It is not affiliated with, commissioned by, or representative of JPMorgan Chase or any employer.

## Quick start

Use the bundled Python runtime and run:

```powershell
& 'C:\Users\VAMSI\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/runPipeline.py
```

The pipeline reads the immutable `data/raw/Online Retail.xlsx`, writes clean data and reporting tables to `outputs/`, and produces QA evidence.

To create the Excel command centre after a successful run:

```powershell
& 'C:\Users\VAMSI\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/prepareWorkbookData.py
& 'C:\Users\VAMSI\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' src/buildWorkbook.mjs
& 'C:\Users\VAMSI\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/addWorkbookCharts.py
```

The generated workbook is `workbook/Enterprise_Performance_Command_Center.xlsx`. It contains dashboard and governance tables plus 100-row display subsets for raw and clean transactions. The full immutable source and clean output remain on disk outside the workbook.

To build the ten-slide executive review deck from the same verified outputs:

```powershell
& 'C:\Users\VAMSI\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/buildPresentation.py
```

The deck is written to `presentation/Monthly_Business_Performance_Review.pptx` and reads only `outputs/processed/*.csv` and `config/project_config.json`; every figure on a slide traces to one of those files.

## Source

UCI Machine Learning Repository, *Online Retail*, Daqing Chen (2015), DOI: 10.24432/C5BW33. Downloaded 2026-10-27 from https://archive.ics.uci.edu/dataset/352/online+retail. CC BY 4.0. The raw workbook is preserved unchanged in `data/raw/`.

## Limitations

The source describes retail transactions, not banking data. Project portfolio data is entirely synthetic. Findings demonstrate reporting method and controls, not company results, benchmarks, or impacts.
