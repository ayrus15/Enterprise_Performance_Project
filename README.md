# Enterprise Performance, Portfolio Governance and Automated Reporting System

An independent portfolio simulation that combines analysis of the public UCI Online Retail dataset with a clearly labelled synthetic delivery portfolio. It is not affiliated with, commissioned by, or representative of JPMorgan Chase or any employer.

## Quick start

Use the bundled Python runtime and run:

```powershell
& 'C:\Users\VAMSI\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' src/runPipeline.py
```

The pipeline reads the immutable `data/raw/Online Retail.xlsx`, writes clean data and reporting tables to `outputs/`, and produces QA evidence. Build the workbook and presentation after the pipeline succeeds.

## Source

UCI Machine Learning Repository, *Online Retail*, Daqing Chen (2015), DOI: 10.24432/C5BW33. Downloaded 2026-10-27 from https://archive.ics.uci.edu/dataset/352/online+retail. CC BY 4.0. The raw workbook is preserved unchanged in `data/raw/`.

## Limitations

The source describes retail transactions, not banking data. Project portfolio data is entirely synthetic. Findings demonstrate reporting method and controls, not company results, benchmarks, or impacts.
