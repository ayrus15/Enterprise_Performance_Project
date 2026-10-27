# Enterprise Performance, Portfolio Governance and Automated Reporting System

## Integrated Portfolio Project for JPMorgan Chase Business Management Analyst Applications

**Project type:** Independent business management and analytics
simulation\
**Duration:** 14 days\
**Suggested effort:** 6--8 hours per day\
**Primary audience:** Business Management, COO Office, Portfolio
Governance, Operations and Management Reporting teams\
**Status:** Portfolio project; not affiliated with or commissioned by
JPMorgan Chase\
**Data policy:** Use a public transaction dataset for commercial
analysis and clearly labelled synthetic data for the project portfolio.
Never represent synthetic project outcomes as real company results.

------------------------------------------------------------------------

## 1. Project Overview

### 1.1 Project concept

Build a practical business management command centre that combines four
capabilities:

1.  **Business performance analysis:** Analyse real retail transaction
    data to identify revenue patterns, customer concentration,
    cancellations, product performance and other decision-relevant
    trends.
2.  **Project portfolio governance:** Monitor a synthetic portfolio of
    10--12 projects using milestones, budgets, delivery status, risks,
    dependencies, owners and action tracking.
3.  **Automated data pipeline and reporting controls:** Use Python to
    ingest, clean, validate, reconcile and refresh reporting tables.
    Record refresh history and surface exceptions rather than silently
    accepting poor-quality data.
4.  **Executive decision support:** Turn the analysis into a concise
    monthly business review with evidence-based insights, risks,
    decisions required, named owners and due dates.

The goal is to demonstrate that the candidate can connect analysis,
operational governance, reporting controls and executive communication
in one coherent workflow.

### 1.2 Business problem

Business management teams often receive information from separate
spreadsheets, operational systems and project owners. Reporting can
become slow, inconsistent and difficult to audit. Leaders may see a KPI
change without knowing whether it is a genuine business movement, a data
quality problem or a delivery risk.

This project simulates a lightweight operating model that answers:

-   What is happening in business performance?
-   Which projects are on track, at risk or overdue?
-   Which risks require management attention?
-   Can the reported numbers be trusted and reproduced?
-   What decisions or actions should leadership take next?

### 1.3 Final deliverables

Create the following artefacts:

  ----------------------------------------------------------------------------------------------
  Deliverable             Target filename                                Purpose
  ----------------------- ---------------------------------------------- -----------------------
  Main workbook           `Enterprise_Performance_Command_Center.xlsx`   Analysis, project
                                                                         governance, controls
                                                                         and executive dashboard

  Executive presentation  `Monthly_Business_Performance_Review.pptx`     10-slide management
                                                                         review

  Decision memo           `Executive_Decision_Memo.md`                   Concise findings,
                                                                         decisions, owners and
                                                                         deadlines

  Data pipeline           `src/` Python scripts                          Repeatable ingestion,
                                                                         transformation, QA and
                                                                         output generation

  Data dictionary         `docs/data_dictionary.md`                      Definitions, fields,
                                                                         sources and assumptions

  Operating procedure     `docs/monthly_reporting_sop.md`                Repeatable reporting
                                                                         steps and control
                                                                         checks

  QA evidence             `outputs/qa/`                                  Reconciliation results,
                                                                         exceptions and run logs

  Portfolio case study    `README.md` or portfolio webpage               Problem, approach,
                                                                         outputs, findings and
                                                                         limitations
  ----------------------------------------------------------------------------------------------

### 1.4 Success criteria

The project is complete when:

-   The transaction dataset is sourced from a public source and its
    provenance is documented.
-   Raw data is preserved separately from cleaned data.
-   All transformations can be rerun from documented commands.
-   Key metrics have written definitions and reproducible calculations.
-   Reconciliation and data-quality checks run automatically.
-   The synthetic portfolio contains 10--12 projects with realistic,
    internally consistent statuses, milestones, budgets, risks and
    actions.
-   The Excel dashboard communicates the most important trends without
    requiring the reader to inspect every data tab.
-   The presentation distinguishes facts, calculations, assumptions and
    recommendations.
-   Every major recommendation is linked to evidence, an owner role, a
    due date and a proposed success measure.
-   No fictional portfolio data is described as real employer or client
    data.

------------------------------------------------------------------------

## 2. Scope and Boundaries

### In scope

-   Public UCI Online Retail transaction data.
-   Data cleaning, transformation and validation using Python.
-   Revenue and transaction analysis in Excel.
-   Synthetic project portfolio of 10--12 projects.
-   Milestone and schedule tracking.
-   Budget utilisation and forecast-at-completion tracking where
    assumptions are provided.
-   Risk, issue, dependency and action management.
-   Automated KPI table refresh and exception reporting.
-   Refresh logs and reconciliation controls.
-   Management dashboard, executive presentation and decision memo.
-   Documentation and a repeatable operating procedure.

### Out of scope

-   Any claim that this was performed for JPMorgan Chase or another
    financial institution.
-   Use of confidential, personal, client or employer data.
-   Connecting to live banking, HR, Workday or corporate systems.
-   A production-grade enterprise integration platform.
-   Financial advice or investment recommendations.
-   Unsupported claims of business impact, cost savings or deployment.
-   Treating retail revenue metrics as bank financial metrics.

### Important interpretation

The UCI Online Retail dataset is a retail transaction dataset, not
banking data. Use it to demonstrate analytical method and management
reporting discipline. The synthetic project portfolio demonstrates
governance. Explain this separation clearly in the workbook and
presentation.

------------------------------------------------------------------------

## 3. Data Sources and Data Model

### 3.1 Transaction dataset

Use the UCI Machine Learning Repository's **Online Retail** dataset.
Obtain it from the official repository and document the exact download
page, access date, file name, licence or usage terms shown by the
repository, and any dataset version details.

Official source: https://archive.ics.uci.edu/dataset/352/online+retail

Expected source fields include:

  -----------------------------------------------------------------------
  Field                   Meaning                 Initial treatment
  ----------------------- ----------------------- -----------------------
  `InvoiceNo`             Invoice identifier      Preserve as text;
                                                  identify cancellation
                                                  patterns

  `StockCode`             Product code            Preserve as text

  `Description`           Product description     Trim whitespace; assess
                                                  missing values

  `Quantity`              Quantity on invoice     Preserve sign; inspect
                          line                    negative quantities

  `InvoiceDate`           Invoice timestamp       Parse to datetime

  `UnitPrice`             Unit price              Numeric; inspect zero
                                                  and negative values

  `CustomerID`            Customer identifier     Preserve missingness;
                                                  avoid fabricating
                                                  identities

  `Country`               Customer country        Standardise whitespace
                                                  and inspect categories
  -----------------------------------------------------------------------

The original source may have encoding and file-format considerations.
Handle them explicitly and document the method used.

### 3.2 Transaction derived fields

Add the following fields to the cleaned analysis table:

-   `InvoiceDateParsed`
-   `YearMonth`
-   `LineValue = Quantity * UnitPrice`
-   `IsCancellation`
-   `IsNegativeQuantity`
-   `IsZeroOrNegativePrice`
-   `IsMissingCustomer`
-   `IsValidForSalesAnalysis`
-   `DataQualityFlags`

Do not automatically discard cancellations or negative quantities.
Preserve them and define separate gross sales, cancellation and
net-value views. Explain how each view treats negative quantities and
cancellation invoices.

### 3.3 Synthetic project portfolio

Create a fictional portfolio of 10--12 projects across operational
improvement, technology enablement, data quality, customer operations,
reporting automation and control enhancement. Use fictional project
names and clearly label the data as synthetic.

Suggested project schema:

  -----------------------------------------------------------------------
  Field                   Type                    Definition
  ----------------------- ----------------------- -----------------------
  `ProjectID`             Text                    Unique stable
                                                  identifier,
                                                  e.g. `PRJ-001`

  `ProjectName`           Text                    Fictional project name

  `Workstream`            Category                Operations, Technology,
                                                  Data, Controls or
                                                  Customer

  `SponsorRole`           Text                    Accountable sponsor
                                                  role, not a real
                                                  person's name

  `ProjectManagerRole`    Text                    Responsible delivery
                                                  role

  `Priority`              Category                Critical, High, Medium
                                                  or Low

  `StartDate`             Date                    Baseline or approved
                                                  start date

  `BaselineEndDate`       Date                    Approved baseline
                                                  completion date

  `ForecastEndDate`       Date                    Current forecast
                                                  completion date

  `ActualEndDate`         Date or blank           Actual completion date,
                                                  if completed

  `Budget`                Currency                Synthetic approved
                                                  budget

  `ActualCost`            Currency                Synthetic cost to date

  `ForecastCost`          Currency                Synthetic expected
                                                  final cost

  `PercentComplete`       Decimal                 Progress from 0 to 1

  `Status`                Category                Not Started, On Track,
                                                  At Risk, Off Track,
                                                  Complete

  `RAGStatus`             Category                Green, Amber, Red

  `KeyMilestone`          Text                    Next significant
                                                  milestone

  `NextMilestoneDate`     Date                    Next milestone target

  `Dependency`            Text or ID              Dependency on another
                                                  project or team

  `LastUpdated`           Date                    Last status update

  `StatusCommentary`      Text                    Concise evidence-based
                                                  status explanation
  -----------------------------------------------------------------------

Make the fictional portfolio internally consistent. For example,
completed projects should have 100% progress and an actual end date;
forecast end dates should not precede start dates; costs should not be
negative unless a documented credit convention is used.

### 3.4 Milestone table

Use a separate milestone table rather than relying only on one "next
milestone" field.

  -----------------------------------------------------------------------
  Field                   Type                    Definition
  ----------------------- ----------------------- -----------------------
  `MilestoneID`           Text                    Unique milestone
                                                  identifier

  `ProjectID`             Text                    Parent project

  `MilestoneName`         Text                    Deliverable or
                                                  checkpoint

  `BaselineDate`          Date                    Approved baseline date

  `ForecastDate`          Date                    Latest forecast date

  `ActualDate`            Date or blank           Actual completion date

  `MilestoneStatus`       Category                Not Started, In
                                                  Progress, Complete, At
                                                  Risk, Overdue

  `OwnerRole`             Text                    Accountable role

  `EvidenceLink`          Text                    Optional path to
                                                  supporting evidence
  -----------------------------------------------------------------------

### 3.5 Risk, issue and action register

Use a unified table with a `RecordType` field, or separate tables if
that makes the workbook easier to maintain. If using a unified table,
use these fields:

  ------------------------------------------------------------------------
  Field                    Type                    Definition
  ------------------------ ----------------------- -----------------------
  `RecordID`               Text                    Unique identifier

  `RecordType`             Category                Risk, Issue, Dependency
                                                   or Action

  `ProjectID`              Text                    Related project

  `Title`                  Text                    Short description

  `Description`            Text                    Clear statement of the
                                                   problem or exposure

  `Probability`            Integer 1--5            Likelihood for risks

  `Impact`                 Integer 1--5            Consequence severity

  `RiskScore`              Integer                 Probability × impact
                                                   for risks

  `Priority`               Category                Critical, High, Medium
                                                   or Low

  `OwnerRole`              Text                    Responsible role

  `DateRaised`             Date                    Date identified

  `DueDate`                Date                    Required resolution
                                                   date

  `Status`                 Category                Open, In Progress,
                                                   Blocked, Closed

  `MitigationOrNextStep`   Text                    Concrete next action

  `EscalationRequired`     Boolean                 Whether management
                                                   escalation is required

  `ClosedDate`             Date or blank           Closure date
  ------------------------------------------------------------------------

Use `RiskScore = Probability × Impact` only for records where both
values are applicable. Do not calculate a misleading risk score for
ordinary actions.

### 3.6 Reporting run log

  ------------------------------------------------------------------------
  Field                    Type                    Definition
  ------------------------ ----------------------- -----------------------
  `RunID`                  Text                    Unique execution
                                                   identifier

  `RunTimestamp`           Datetime                Pipeline start or
                                                   completion time

  `SourceName`             Text                    Dataset or input file

  `SourceRowCount`         Integer                 Number of input rows

  `OutputRowCount`         Integer                 Number of output rows

  `RejectedRowCount`       Integer                 Rows excluded from a
                                                   defined analytical view

  `WarningCount`           Integer                 Non-fatal validation
                                                   warnings

  `ErrorCount`             Integer                 Failed checks or
                                                   processing errors

  `ReconciliationStatus`   Category                Pass, Warning or Fail

  `RunStatus`              Category                Success, Partial
                                                   Success or Failed

  `Notes`                  Text                    Short explanation of
                                                   exceptions
  ------------------------------------------------------------------------

Never log sensitive data unnecessarily. This simulation should use
public and synthetic data only.

------------------------------------------------------------------------

## 4. KPI Catalogue and Definitions

Every KPI must have a business definition, formula, grain, time period,
data source, interpretation and known limitation. Do not display a
metric merely because it is easy to calculate.

### 4.1 Retail transaction KPIs

**Gross positive sales value**

Sum `Quantity * UnitPrice` for transaction lines included in the
positive-sales definition. Explicitly document whether cancellation
invoices and negative quantities are excluded.

**Cancellation value**

Calculate the absolute value of the line values associated with
cancellation transactions, using the defined cancellation identification
rule. Keep the cancellation count and value separate from sales.

**Net transaction value**

Sum line values under a documented treatment of positive sales and
negative transactions. Show this separately from gross positive sales
and explain the distinction.

**Monthly sales growth**

`(Current month gross positive sales - Previous month gross positive sales) / Previous month gross positive sales`

If the previous month is zero or missing, return N/A rather than divide
by zero.

**Invoice count**

Count distinct invoice identifiers under the chosen inclusion rule.
Exclude or separately report cancellation invoices where appropriate.

**Average order value**

`Gross positive sales value / Number of eligible positive-sales invoices`

State the invoice eligibility rules. Do not divide by all rows if the
metric is intended to represent average invoice value.

**Customer concentration**

For customers with usable IDs, calculate each customer's share of gross
positive sales and the combined share of the top 10 customers. State
that customers with missing IDs are excluded from customer-level
concentration analysis.

**Country contribution**

`Country gross positive sales / Total gross positive sales`

Confirm that country values are standardised and that the denominator
uses the same inclusion rules.

**Data completeness**

`Non-missing values / Expected values` for required fields, reported
field by field.

**Cancellation rate**

Choose one consistent definition, such as cancellation invoices divided
by eligible invoices. Label the denominator and avoid mixing
invoice-level and line-level measures.

### 4.2 Project portfolio KPIs

**On-time delivery rate**

`Projects completed on or before baseline end date / Projects due or completed in the reporting cohort`

Define the cohort explicitly. Do not count future-due projects as
overdue failures.

**Schedule variance in days**

`ForecastEndDate - BaselineEndDate`

Positive values indicate a forecast delay; negative values indicate an
earlier forecast. Report only where both dates exist.

**Budget utilisation**

`ActualCost / Budget`

Use N/A when the budget is zero or missing. Do not interpret high
utilisation alone as overspending.

**Forecast budget variance**

`ForecastCost - Budget`

Positive values indicate forecast overspend; negative values indicate
forecast underspend. Show both currency and percentage variance where
the budget is valid.

**Milestone slippage**

`ForecastDate - BaselineDate`

Report in days. Keep actual completion and current forecast distinct.

**At-risk project count**

Count projects with a status of At Risk or Off Track, based on
documented status rules.

**Overdue action count**

Count open actions whose due date is earlier than the reporting date.

**High-risk exposure**

Count open risks meeting the defined high-risk threshold. A possible
simulation rule is risk score 15 or higher on a 5 × 5 matrix. Label this
as a project assumption, not an industry standard.

**Status freshness**

`ReportingDate - LastUpdated`

Flag stale project updates based on a documented threshold, such as more
than 7 calendar days.

**Project completion**

Average `PercentComplete` only if the calculation is meaningful for the
chosen cohort. Also show the number of projects included and avoid
implying that an unweighted average is equivalent to weighted portfolio
delivery.

### 4.3 Data pipeline and control KPIs

**Input row count:** Number of source rows read.

**Output row count:** Number of records written to the cleaned output.

**Duplicate candidate count:** Number of rows flagged by the selected
duplicate rule. Do not delete duplicates without defining what
constitutes a duplicate.

**Required-field missing count:** Count of rows missing required fields.

**Invalid-value count:** Count of records failing documented validation
rules.

**Reconciliation difference:**
`Source control total - Output control total`, using a control total
appropriate to the transformation. Explain when differences are expected
due to filtering or exclusion.

**Pipeline success rate:** Successful completed runs divided by all
attempted runs in the reporting period. For a one-off portfolio
demonstration, show run status and history rather than implying a
meaningful long-term reliability rate.

**Exception resolution rate:** Closed exceptions divided by all
exceptions raised in a specified cohort. State the cohort and cut-off
date.

### 4.4 KPI governance rules

-   Store definitions in a `KPI_Dictionary` worksheet or separate
    documentation file.
-   Use the same definition in Python, Excel and the presentation.
-   Show the reporting period and last refresh timestamp on the
    dashboard.
-   Use N/A for unavailable denominators rather than displaying zero.
-   Preserve raw values and transformation evidence.
-   Separate observed facts, calculated metrics, assumptions and
    recommendations.
-   Do not invent benchmarks. If a threshold is simulated, label it as
    an internal project assumption.

------------------------------------------------------------------------

## 5. Excel Workbook Design

Build `Enterprise_Performance_Command_Center.xlsx` with the following
worksheets.

### 5.1 `ReadMe_Control`

Include:

-   Project purpose and scope.
-   Data source and provenance.
-   Reporting date and reporting period.
-   File version and last refresh timestamp.
-   Instructions to rerun the pipeline.
-   Synthetic data disclaimer.
-   Metric inclusion and exclusion rules.
-   Colour conventions and status definitions.
-   Links to documentation and QA outputs.

### 5.2 `Raw_Transactions`

-   Preserve the downloaded data as received, apart from unavoidable
    import-format handling.
-   Do not overwrite raw data with cleaned values.
-   Record source row count and file name.
-   Keep identifiers as text where appropriate.
-   If the full source is too large for Excel performance, retain the
    complete data in CSV or Parquet and document the subset or query
    feeding the workbook.

### 5.3 `Clean_Transactions`

-   Include parsed dates, derived fields, validity flags and quality
    flags.
-   Keep the treatment of cancellations transparent.
-   Use structured Excel tables.
-   Avoid hard-coded values in formulas where a documented parameter is
    more appropriate.
-   Make each derived field traceable to a documented rule.

### 5.4 `Sales_Pivots`

Create pivot tables or equivalent summary tables for:

-   Monthly sales and growth.
-   Country contribution.
-   Top products by sales value.
-   Top customers by sales value, where customer IDs are available.
-   Invoice and cancellation trends.
-   Data quality findings.

Ensure every pivot or summary table uses the same inclusion rules as the
KPI dictionary.

### 5.5 `Executive_Dashboard`

Recommended components:

**Top KPI cards** - Gross positive sales value. - Month-on-month sales
growth. - Eligible invoice count. - Cancellation rate. - At-risk or
off-track project count. - Overdue action count. - Forecast portfolio
budget variance. - Latest pipeline run status.

**Charts** - Monthly sales trend. - Country contribution. - Top products
or customers. - Project status distribution. - Budget versus forecast
cost. - Open risks by severity. - Overdue actions by workstream.

**Management attention panel** - Three highest-priority issues. -
Decisions required. - Owner role and due date. - Data quality or refresh
warnings.

Avoid overloading the dashboard. Use a clear hierarchy, readable labels,
consistent number formats and visible reporting dates.

### 5.6 `Project_Portfolio`

Include the 10--12 synthetic projects, status, sponsor role, delivery
owner role, budget, actual and forecast cost, progress, baseline and
forecast dates, next milestone and last update.

Use conditional formatting to flag:

-   Forecast end dates later than baseline.
-   Forecast cost above budget.
-   Stale updates.
-   At Risk and Off Track projects.
-   Missing owners or missing next milestone dates.

### 5.7 `Milestones`

Track baseline date, forecast date, actual date, owner role, status and
variance for each milestone. Include a concise exception view for
delayed or overdue milestones.

### 5.8 `Risks_Actions`

Include risk, issue, dependency and action records. Provide filters for
owner, project, priority, due date and status. Highlight high-risk
exposures, overdue actions and records requiring escalation.

### 5.9 `QA_Reconciliation`

Display:

-   Source and output row counts.
-   Duplicate candidate count.
-   Missing required-field counts.
-   Invalid-value counts.
-   Control totals before and after transformations.
-   Expected versus actual exclusions.
-   Reconciliation difference.
-   Pass, Warning or Fail for each check.
-   Links or references to detailed QA logs.

Do not force every reconciliation difference to zero. Explain legitimate
changes due to transformations and exclusions.

### 5.10 `KPI_Dictionary`

Include the KPI name, business purpose, formula, numerator, denominator,
grain, inclusion rules, source fields, refresh frequency, owner role,
threshold if applicable, and known limitations.

### 5.11 Workbook quality requirements

-   Use consistent fonts, alignment, number formats and table styles.
-   Freeze header rows and enable filters on detail sheets.
-   Avoid merged cells in data tables.
-   Avoid hard-coded dashboard metrics that do not update when source
    tables change.
-   Include formulas or transparent output tables rather than
    unexplained manually typed values.
-   Ensure the workbook opens without broken links or formula errors.
-   Test filters, formulas, chart ranges and print layout.
-   If Python produces summary tables, include the generated timestamp
    and pipeline run ID.

------------------------------------------------------------------------

## 6. Python Pipeline and Automation Architecture

The project should demonstrate reliable reporting automation without
becoming an unnecessarily complex software engineering build.

### 6.1 Suggested directory structure

``` text
enterprise-performance-command-center/
├── README.md
├── requirements.txt
├── config/
│   └── project_config.yaml
├── data/
│   ├── raw/
│   ├── interim/
│   └── synthetic/
├── src/
│   ├── ingestTransactions.py
│   ├── cleanTransactions.py
│   ├── validateData.py
│   ├── calculateKpis.py
│   ├── buildProjectPortfolio.py
│   ├── generateReports.py
│   └── runPipeline.py
├── outputs/
│   ├── processed/
│   ├── reports/
│   └── qa/
├── workbook/
│   └── Enterprise_Performance_Command_Center.xlsx
├── presentation/
│   └── Monthly_Business_Performance_Review.pptx
└── docs/
    ├── data_dictionary.md
    ├── kpi_definitions.md
    ├── monthly_reporting_sop.md
    ├── assumptions_and_limitations.md
    └── test_plan.md
```

The example filenames use camelCase for Python scripts. Keep function
names in camelCase if following the same convention throughout the
project.

### 6.2 Pipeline sequence

1.  Load configuration and verify required files exist.
2.  Read the raw transaction source without modifying it.
3.  Validate schema and required columns.
4.  Parse dates and numeric fields.
5.  Add derived fields and data-quality flags.
6.  Generate a validation report.
7.  Calculate transaction KPIs and grouped summary tables.
8.  Load and validate the synthetic project portfolio.
9.  Calculate project, milestone, risk and action KPIs.
10. Reconcile source, transformed and output counts and control totals.
11. Write clean data and reporting tables to `outputs/`.
12. Refresh the workbook tables or clearly document the workbook import
    process.
13. Generate a run log with timestamp, counts, warnings, errors and
    status.
14. Stop or mark the run as failed if a critical validation check fails.
15. Produce an exception report for warnings and failed checks.

### 6.3 Minimum automation controls

Implement:

-   Required-column checks.
-   Date parsing checks.
-   Numeric range checks.
-   Missing-value reporting.
-   Duplicate candidate detection.
-   Explicit treatment of negative quantities and cancellation invoices.
-   Row-count reconciliation.
-   Financial control-total reconciliation with documented exclusions.
-   Safe handling of missing denominators.
-   Output directory creation.
-   Structured logging.
-   Clear error messages.
-   Deterministic transformations where possible.
-   Automated tests for key KPI functions.
-   A non-zero exit status for critical pipeline failures, where
    appropriate.

### 6.4 Integration engineering extension

To reflect business systems and integration engineering, add a
controlled source-to-report interface:

-   Read source data from a documented file or public data endpoint.
-   Validate the payload before processing.
-   Separate ingestion from business logic.
-   Use configuration rather than hard-coded paths and thresholds.
-   Make reruns safe and avoid creating duplicate outputs.
-   Record a run ID and processing timestamp.
-   Preserve failed-run logs and surface actionable error messages.
-   If using an API, protect credentials and never commit secrets.
-   Do not call this a production enterprise integration. Describe it as
    a local portfolio pipeline unless it is genuinely deployed and
    operated in production.

Optional extension: create a mock employee onboarding event workflow
using synthetic employee records and a test notification endpoint. This
is not required for the core JPMorgan project and should only be
attempted after the reporting system is complete.

------------------------------------------------------------------------

## 7. Project Governance Operating Model

### 7.1 Reporting cadence

Simulate a monthly business review supported by weekly project updates.

**Weekly project status update** - Delivery status and progress. -
Milestones completed and upcoming. - Forecast completion date. - Actual
cost and forecast cost. - New or changed risks. - Decisions and
dependencies. - Actions, owners and due dates. - Date of last update.

**Monthly business review** - Business performance summary. - Portfolio
status and movement. - Budget and schedule exceptions. - Top risks and
issues. - Decisions required from leadership. - Actions from the prior
review and closure status. - Data quality and reporting control summary.

### 7.2 Status rules

Create a documented status policy. Example simulation rules:

-   **Green / On Track:** Forecast completion is on or before baseline,
    forecast cost is within budget, and no unresolved critical risk is
    present.
-   **Amber / At Risk:** A material schedule or budget pressure exists,
    a dependency threatens a milestone, or a high risk requires
    mitigation.
-   **Red / Off Track:** A critical milestone is forecast to miss its
    approved date, forecast cost materially exceeds budget, or an
    unresolved severe issue prevents delivery.
-   **Complete:** All agreed deliverables are complete and closure
    evidence is recorded.
-   **Not Started:** Work has not begun and the approved start date has
    not been reached.

These are project-specific rules, not universal standards. Make them
configurable and explain any override. Avoid assigning a status based on
subjective commentary alone.

### 7.3 Decision and action discipline

Every management action should include:

-   A clear action statement.
-   Why the action is required.
-   Evidence supporting it.
-   One accountable owner role.
-   A due date.
-   A status.
-   A definition of completion.
-   Escalation criteria if overdue.

Every requested leadership decision should include the decision
required, options considered, recommendation, implications, deadline and
decision owner role.

------------------------------------------------------------------------

## 8. Fourteen-Day Execution Plan

Plan for approximately 6--8 hours daily. If a day runs over, protect the
analysis, QA and executive narrative before adding optional features.

### Day 1: Define the problem and success criteria

-   Read the official UCI dataset description.
-   Create the project repository and directory structure.
-   Write the problem statement, scope and limitations.
-   Create an initial data dictionary and KPI register.
-   Define which outputs will be delivered.
-   Create a project plan and issue log.

**Exit criteria:** A clear scope, documented source and working
repository.

### Day 2: Acquire and profile the transaction data

-   Download the official dataset.
-   Preserve the raw file.
-   Inspect schema, types, row count, missingness and date range.
-   Profile quantities, prices, cancellation patterns and customer IDs.
-   Document data quality risks.

**Exit criteria:** Reproducible data profile and documented import
procedure.

### Day 3: Build the cleaning and validation layer

-   Parse dates and numeric fields.
-   Standardise text fields.
-   Add derived fields and quality flags.
-   Define cancellation and negative-value treatment.
-   Build missing-value, duplicate and invalid-value checks.
-   Preserve excluded records and record reasons for exclusion.

**Exit criteria:** Cleaned data and a first QA report.

### Day 4: Build transaction KPI calculations

-   Calculate monthly sales, growth, invoice count and average order
    value.
-   Analyse cancellations and net transaction value.
-   Calculate country contribution and top products.
-   Analyse customer concentration where IDs are available.
-   Test calculations against independent spot checks.

**Exit criteria:** KPI tables with documented formulas and tests.

### Day 5: Create the synthetic portfolio

-   Define 10--12 fictional projects across several workstreams.
-   Set baselines, forecast dates, budgets, costs and progress.
-   Create milestones and dependencies.
-   Build realistic at-risk, off-track and completed examples.
-   Add synthetic risks, issues and actions.
-   Validate internal consistency.

**Exit criteria:** Portfolio, milestone and risk/action data with clear
synthetic labels.

### Day 6: Calculate portfolio KPIs

-   Calculate status distribution.
-   Calculate schedule variance and budget variance.
-   Identify overdue milestones and actions.
-   Flag stale updates and missing owners.
-   Define the reporting cut-off date.
-   Test status logic against edge cases.

**Exit criteria:** Reproducible project governance metrics.

### Day 7: Build the automated pipeline

-   Implement ingestion, cleaning, validation and KPI modules.
-   Add configuration for paths and thresholds.
-   Generate output tables and a run log.
-   Add failure handling and readable error messages.
-   Make repeated runs safe.

**Exit criteria:** One documented command runs the pipeline end to end
on local data.

### Day 8: Add reconciliation and exception reporting

-   Reconcile row counts and control totals.
-   Document expected changes due to filtering and transformations.
-   Add critical versus non-critical checks.
-   Produce an exception report.
-   Test deliberately malformed input files.
-   Verify that critical failures are visible.

**Exit criteria:** QA controls catch known errors and explain legitimate
differences.

### Day 9: Build the Excel workbook

-   Create all required worksheets.
-   Load raw, cleaned and summary data.
-   Add the KPI dictionary.
-   Add portfolio, milestone and risk/action tables.
-   Add QA and reconciliation results.
-   Confirm formulas and table ranges.

**Exit criteria:** Complete workbook structure with traceable data.

### Day 10: Build the executive dashboard

-   Create KPI cards and trend charts.
-   Add project status and risk views.
-   Add management attention items.
-   Display reporting period and refresh status.
-   Improve readability and remove redundant visuals.
-   Test workbook filters and recalculation.

**Exit criteria:** Dashboard communicates the main story without
requiring manual exploration of every worksheet.

### Day 11: Analyse findings and formulate recommendations

-   Identify the strongest business trends in the transaction data.
-   Identify the highest-priority portfolio risks.
-   Distinguish observed results from synthetic assumptions.
-   Develop three to five recommendations.
-   Link each recommendation to evidence, an owner role, a deadline and
    a success measure.
-   Note limitations and alternative explanations.

**Exit criteria:** A concise, defensible set of management insights.

### Day 12: Create the executive presentation and memo

-   Build the 10-slide review.
-   Draft the executive decision memo.
-   Ensure the deck and workbook use consistent figures.
-   Make decisions and actions explicit.
-   Remove unsupported claims and invented benchmarks.

**Exit criteria:** A presentation and memo that a manager can understand
quickly.

### Day 13: Test and conduct a simulated review

-   Run the pipeline from a clean environment.
-   Check workbook formulas, charts and reconciliation outputs.
-   Compare all deck figures against the workbook.
-   Ask a reviewer or use a checklist to challenge the assumptions.
-   Test whether each recommendation is actionable.
-   Record issues and fix high-severity defects.

**Exit criteria:** No known critical data, formula or reporting defects.

### Day 14: Finalise the portfolio case study

-   Finalise documentation and setup instructions.
-   Capture clear dashboard and workbook screenshots.
-   Add a concise case study explaining the problem, approach, findings
    and limitations.
-   Describe the project honestly as an independent simulation.
-   Add a list of decisions and improvements that would follow in a real
    organisation.
-   Prepare to explain the pipeline and KPIs in an interview.

**Exit criteria:** A reproducible, polished project with clear evidence
of business judgement, analytical skill and control discipline.

------------------------------------------------------------------------

## 9. Ten-Slide Executive Presentation Outline

### Slide 1: Executive summary

-   Three key findings.
-   Two or three highest-priority risks.
-   Decisions required.
-   Reporting period and data caveat.

### Slide 2: Business performance overview

-   Gross positive sales, growth and invoice volume.
-   Key movement versus the prior period.
-   Important data limitations.

### Slide 3: Revenue drivers and concentration

-   Country, product and customer contributions.
-   Concentration or dependency exposure.
-   Implications for monitoring and follow-up.

### Slide 4: Cancellations and data quality

-   Cancellation trend.
-   Missingness and invalid-value findings.
-   Effect of data treatment on reported metrics.
-   Control status.

### Slide 5: Portfolio health

-   Project status distribution.
-   Progress and delivery outlook.
-   Projects requiring management attention.

### Slide 6: Schedule and budget exceptions

-   Delayed milestones.
-   Forecast completion variance.
-   Forecast cost versus budget.
-   Priority exceptions and their implications.

### Slide 7: Risk and action management

-   Highest-scoring risks.
-   Overdue actions.
-   Dependencies requiring escalation.
-   Named owner roles and deadlines.

### Slide 8: Reporting automation and controls

-   Pipeline stages.
-   Validation and reconciliation controls.
-   Latest run status.
-   Exceptions detected and how failures are handled.

### Slide 9: Recommendations and decisions

For each recommendation show: - Evidence. - Proposed action. - Owner
role. - Due date. - Expected result or measurement. - Decision required.

### Slide 10: Thirty-day action plan and limitations

-   Immediate actions.
-   Next review milestones.
-   Success measures.
-   Data and simulation limitations.
-   Future enhancements.

Do not fabricate findings before analysing the data. The slide outline
defines the structure, not the conclusions.

------------------------------------------------------------------------

## 10. Executive Decision Memo Template

# Executive Decision Memo

**To:** Simulated Business Management Leadership Team\
**From:** Project Analyst\
**Date:** \[Reporting date\]\
**Subject:** Monthly Business Performance and Portfolio Review

### Executive summary

Summarise the most important changes, the portfolio's delivery condition
and the decisions required. State which figures are derived from public
transaction data and which portfolio results are synthetic.

### Key findings

1.  **Business performance:** State the finding, period, metric and
    supporting calculation.
2.  **Portfolio delivery:** State the delivery issue, affected projects
    and forecast implication.
3.  **Risk and controls:** State the largest risk or data quality
    concern and its effect on reporting confidence.

### Decisions required

  ------------------------------------------------------------------------------
  Decision       Recommendation     Decision owner Due date       Consequence of
                                    role                          delay
  -------------- ------------------ -------------- -------------- --------------
  \[Decision\]   \[Evidence-based   \[Role\]       \[Date\]       \[Impact\]
                 option\]                                         

  ------------------------------------------------------------------------------

### Action plan

  Action       Owner role   Due date   Success measure   Status
  ------------ ------------ ---------- ----------------- ------------
  \[Action\]   \[Role\]     \[Date\]   \[Measure\]       \[Status\]

### Risks and limitations

Document the synthetic portfolio, retail dataset's limitations, KPI
assumptions, incomplete data and any caveats affecting interpretation.

------------------------------------------------------------------------

## 11. Quality Assurance and Acceptance Tests

### Data tests

-   Source schema matches expected fields.
-   Date parsing succeeds or produces visible exceptions.
-   Numeric fields are valid under documented rules.
-   Missing required fields are counted.
-   Duplicate candidates are identified using a documented rule.
-   Cancellation and negative quantity records remain traceable.
-   Derived line values can be independently recalculated.
-   Every excluded record has a documented reason or rule.
-   Output row counts reconcile with source rows and documented
    exclusions.

### KPI tests

-   Monthly totals reconcile with underlying records.
-   Growth returns N/A when the comparison period is missing or zero.
-   Average order value uses eligible invoices, not arbitrary row
    counts.
-   Customer concentration excludes missing IDs transparently.
-   Budget variance has the correct sign convention.
-   Schedule variance has the correct sign convention.
-   Overdue actions respect the reporting cut-off date.
-   Project status rules are deterministic and documented.
-   No division by zero creates misleading values.

### Portfolio tests

-   Project IDs are unique.
-   Forecast and baseline dates are logically valid.
-   Completed projects have actual completion evidence.
-   Progress values remain between 0 and 1.
-   Costs and budgets are valid under the simulation assumptions.
-   Risks have probability and impact values where required.
-   Open actions have owners and due dates.
-   Dependencies reference valid projects or documented external teams.

### Reporting tests

-   Dashboard figures match the KPI tables.
-   Presentation figures match the workbook.
-   Reporting date and refresh timestamp are visible.
-   Failed validation checks are not hidden.
-   The workbook opens without broken links or formula errors.
-   All charts have readable titles, units and periods.
-   Recommendations are supported by evidence.
-   Synthetic data is clearly labelled in every relevant artefact.

### Final acceptance checklist

-   [ ] Source provenance documented.
-   [ ] Raw data preserved.
-   [ ] Cleaning and KPI calculations reproducible.
-   [ ] Synthetic portfolio complete and internally consistent.
-   [ ] Workbook complete.
-   [ ] Pipeline and logging work.
-   [ ] Reconciliation and exception reporting work.
-   [ ] Executive dashboard complete.
-   [ ] Ten-slide deck complete.
-   [ ] Decision memo complete.
-   [ ] QA tests passed or outstanding issues disclosed.
-   [ ] Limitations documented.
-   [ ] Project case study ready for portfolio use.

------------------------------------------------------------------------

## 12. How to Present This Project to JPMorgan Chase

### Suggested resume project title

**Enterprise Performance, Portfolio Governance and Reporting
Automation**

### Resume description template

Use only after the project is completed and replace placeholders with
measured results:

-   Built an independent business management command centre combining
    analysis of public retail transaction data with a synthetic 10--12
    project portfolio to demonstrate KPI reporting, delivery governance
    and executive decision support.
-   Developed a Python reporting pipeline with data validation,
    reconciliation, exception reporting and run logging to improve
    repeatability and traceability of management reporting.
-   Designed an Excel dashboard tracking business performance, project
    status, milestone variance, forecast budget variance, risk exposure
    and overdue actions.
-   Produced an executive review deck and decision memo translating
    analytical findings into prioritised recommendations, owner roles
    and due dates.

Do not claim percentage time savings, reduced errors, improved revenue
or other impact unless you measured it using a valid baseline and
recorded the test.

### Interview narrative

Use this sequence:

1.  **Problem:** Explain why fragmented reporting creates management
    blind spots.
2.  **Approach:** Explain how you separated public business data from
    the synthetic project portfolio.
3.  **Analysis:** Explain the KPI definitions and how you validated the
    numbers.
4.  **Controls:** Explain reconciliation, exception handling and
    reporting logs.
5.  **Judgement:** Explain how you prioritised risks and
    recommendations.
6.  **Communication:** Explain how the dashboard and executive deck
    support decisions.
7.  **Limitations:** Acknowledge that the portfolio is simulated and the
    transaction dataset is retail data.
8.  **Next iteration:** Explain how you would integrate approved source
    systems, add access controls and establish an accountable reporting
    cadence in a real organisation.

------------------------------------------------------------------------

## 13. Master Prompt for Codex or Claude

Copy the prompt below into your coding agent after creating the project
folder.

> You are a senior business analyst, management reporting specialist and
> pragmatic Python engineer. Build an end-to-end independent portfolio
> project named **Enterprise Performance, Portfolio Governance and
> Automated Reporting System**.
>
> The project is intended to demonstrate capabilities relevant to a
> Business Management Analyst role. It is not commissioned by JPMorgan
> Chase and must never claim to represent JPMorgan's actual systems,
> data or results.
>
> ### Required outcomes
>
> 1.  Use the public UCI Online Retail dataset from
>     https://archive.ics.uci.edu/dataset/352/online+retail for
>     transaction analysis.
> 2.  Preserve raw data and implement a reproducible Python pipeline for
>     ingestion, cleaning, validation, KPI calculations, reconciliation,
>     exception reporting and run logging.
> 3.  Create a clearly labelled synthetic portfolio of 10--12 projects,
>     with project details, milestones, risks, issues, dependencies and
>     actions.
> 4.  Build an Excel workbook named
>     `Enterprise_Performance_Command_Center.xlsx` with sheets
>     `ReadMe_Control`, `Raw_Transactions`, `Clean_Transactions`,
>     `Sales_Pivots`, `Executive_Dashboard`, `Project_Portfolio`,
>     `Milestones`, `Risks_Actions`, `QA_Reconciliation` and
>     `KPI_Dictionary`.
> 5.  Create a 10-slide presentation named
>     `Monthly_Business_Performance_Review.pptx`.
> 6.  Create an executive decision memo, data dictionary, KPI
>     definitions, monthly reporting SOP, assumptions and limitations
>     document, and test plan.
> 7.  Include reproducible setup and execution instructions.
>
> ### Working method
>
> -   First inspect the existing repository and files. Do not overwrite
>     useful existing work without understanding it.
> -   Create a concise implementation plan and then implement the
>     project in phases.
> -   Prefer simple, readable, maintainable code over unnecessary
>     architecture.
> -   Use Python and pandas for data processing, openpyxl for workbook
>     creation or modification, and python-pptx for presentation
>     generation.
> -   Use camelCase function names consistently.
> -   Keep raw data immutable. Write transformed data and reports to
>     separate output directories.
> -   Do not fabricate analytical results. Run the calculations before
>     writing conclusions.
> -   Clearly label synthetic project data and distinguish it from
>     public transaction data.
> -   Do not invent data sources, benchmarks, savings or business
>     outcomes.
> -   Never embed credentials, API keys or secrets in the repository.
>
> ### Required analysis
>
> Implement documented definitions for gross positive sales,
> cancellation value, net transaction value, monthly sales growth,
> eligible invoice count, average order value, customer concentration,
> country contribution, cancellation rate, project schedule variance,
> budget utilisation, forecast budget variance, on-time delivery,
> overdue actions, high-risk exposure, status freshness, data
> completeness and pipeline run status.
>
> Ensure every KPI definition states its inclusion rules, numerator and
> denominator where applicable, grain, source fields and limitations.
> Handle missing and zero denominators safely.
>
> ### Required controls
>
> Validate required columns, date parsing, numeric fields, missing
> values, duplicate candidates, cancellation treatment, output row
> counts, control totals, portfolio ID uniqueness, valid dates, progress
> ranges, cost and budget assumptions, risk fields and action ownership.
>
> Generate a run log with timestamp, run ID, input and output counts,
> warning and error counts, reconciliation status and run status.
> Critical validation failures must be visible and must not be silently
> ignored. Document legitimate reconciliation differences caused by
> filtering or transformations.
>
> ### Excel requirements
>
> Build a usable command centre, not a collection of disconnected
> tables. Use structured tables, filters, frozen headers, consistent
> number formats, conditional formatting, readable charts and a
> dashboard that shows the reporting period and latest refresh status.
> Ensure dashboard numbers tie to the KPI tables. Avoid unexplained
> hard-coded values and broken links.
>
> ### Presentation requirements
>
> Create these 10 slides: executive summary; business performance
> overview; revenue drivers and concentration; cancellations and data
> quality; portfolio health; schedule and budget exceptions; risk and
> action management; reporting automation and controls; recommendations
> and decisions; 30-day action plan and limitations.
>
> Do not write conclusions until the data is analysed. All
> recommendations must be tied to evidence, an owner role, a due date
> and a success measure. Use simulated values only for the synthetic
> portfolio and label them clearly.
>
> ### Testing and delivery
>
> Add automated tests for critical calculations and validation rules.
> Test missing data, zero denominators, cancellation invoices, negative
> quantities, duplicate candidates, invalid dates, budget overruns and
> overdue actions. Run the full pipeline and fix defects before
> declaring completion.
>
> At the end, provide:
>
> 1.  A concise summary of what was built.
> 2.  The final directory tree.
> 3.  Exact commands to install dependencies and run the pipeline.
> 4.  The location of each deliverable.
> 5.  Test results and known limitations.
> 6.  Any manual steps still required.
>
> Do not claim that the project is complete if any required deliverable
> has not actually been generated and tested.

------------------------------------------------------------------------

## 14. Portfolio README Summary

Use this short description on GitHub or a personal portfolio:

**Enterprise Performance, Portfolio Governance and Automated Reporting
System**

An independent business management simulation combining public retail
transaction analysis, synthetic project portfolio governance, automated
reporting controls and executive decision support. The solution uses
Python for repeatable data processing and validation, Excel for KPI
reporting and portfolio monitoring, and a management review presentation
to communicate findings, risks and decisions. The project demonstrates
analytical discipline, delivery governance, data quality controls and
executive communication. Transaction data is public; project portfolio
data is synthetic.

------------------------------------------------------------------------

## 15. Final Priorities

Build in this order:

1.  **Correct data and KPI definitions.**
2.  **Portfolio governance data that is internally consistent.**
3.  **Automated validation, reconciliation and logging.**
4.  **An Excel dashboard that can be trusted.**
5.  **A concise, evidence-based executive narrative.**
6.  **Polish, screenshots and portfolio presentation.**

Do not spend time on a complex API or iPaaS integration before the core
reporting workflow is reliable. The value of this project is the quality
of the management decisions it supports, the controls behind its numbers
and your ability to explain the trade-offs.
