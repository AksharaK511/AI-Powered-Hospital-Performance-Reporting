# AI-Powered Hospital Performance & Reporting Automation
**1. Project Overview**
An end-to-end healthcare analytics project that automates hospital performance monitoring, anomaly detection, AI-powered reporting, and interactive analysis.

The project uses publicly available CMS hospital data to identify facilities with unusually high emergency department excess minutes, classify anomalies by severity and operational priority, generate validated insights using Google Gemini, and present the results through an interactive Tableau dashboard.

The goal is to demonstrate how data analytics, AI, and business intelligence can be combined to reduce manual reporting effort and help healthcare operations teams identify facilities requiring further review.

**2. Business Problem**

Healthcare organizations monitor large volumes of hospital performance data to identify operational issues and facilities that may require additional review. Manually reviewing these records can be time-consuming and make it difficult to quickly identify the highest-priority facilities.

This project focuses on Emergency Department performance data and uses excess minutes as an indicator for identifying potential performance anomalies.

The solution automates the process of identifying anomalous facilities, assigning operational priority levels, generating AI-assisted insights, and presenting the results through a business intelligence dashboard.

**3. Objectives**

* Analyze hospital performance data from the CMS public dataset.
* Identify facilities with unusually high Emergency Department excess minutes.
* Classify anomalies into severity and operational priority levels.
* Generate executive-level insights from validated analytical results.
* Use Gemini AI to answer natural-language questions about the anomaly data.
* Prevent unsupported AI conclusions by restricting responses to the supplied data.
* Validate AI-generated numerical results against trusted Python calculations.
* Provide an interactive Tableau dashboard for operational analysis.
* Reduce the manual effort required to review and summarize hospital performance data.

**4. Data Source**

The project uses publicly available hospital performance data from the **Centers for Medicare & Medicaid Services (CMS)**.

The dataset contains hospital-level quality and performance measures across multiple conditions and reporting categories. The analysis focuses on Emergency Department performance measures relevant to identifying excess wait-time anomalies.

### Dataset Processing

* Loaded the CMS dataset into Python using pandas.
* Converted facility identifiers to a consistent string format.
* Examined missing values and relevant reporting fields.
* Filtered the dataset to Emergency Department measures.
* Converted performance scores into numeric values for analysis.
* Calculated excess minutes for each applicable facility.
* Identified facilities exceeding the defined performance threshold.

**5. Technology Stack**

### Data Analysis

* Python
* Pandas
* NumPy
* JSON

### AI & Automation

* Google Gemini API
* Google GenAI Python SDK
* Structured AI responses
* AI response validation
* Conversational AI chatbot

### Data Visualization

* Tableau Public
* Interactive KPI dashboard
* Geographic visualization
* Priority and severity analysis

### Data Source

* Centers for Medicare & Medicaid Services (CMS)
* Public CMS hospital performance dataset

### Output

* Hospital anomaly CSV report
* AI-generated executive report in JSON format
* Interactive AI chatbot
* Tableau Public dashboard

**6. Project Workflow**

The project follows an end-to-end analytics and AI reporting workflow:

CMS Hospital Performance Data
            ↓
      Data Ingestion
            ↓
    Data Cleaning & Preparation
            ↓
    Emergency Department Analysis
            ↓
      Anomaly Detection
            ↓
 Severity & Priority Classification
            ↓
    Hospital Anomaly Report
            ↓
      Trusted Statistics
            ↓
       Gemini AI Analysis
            ↓
      AI Response Validation
            ↓
    ┌───────────────────────┐
    │                       │
    ▼                       ▼
AI Executive Report     AI Chatbot
    │                       │
    └───────────┬───────────┘
                ↓
        Tableau Dashboard

### Workflow Description

1. **Data Ingestion**
   Public CMS hospital performance data is loaded and prepared using Python and pandas.

2. **Data Preparation**
   Facility identifiers, performance scores, missing values, and relevant reporting fields are examined and prepared for analysis.

3. **Anomaly Detection**
   Emergency Department performance data is analyzed to identify facilities with unusually high excess minutes.

4. **Severity & Priority Classification**
   Detected anomalies are categorized by severity and mapped to operational priority levels.

5. **Hospital Anomaly Report**
   The identified anomalies are saved as a structured CSV report containing facility details, performance metrics, severity, priority, and recommended actions.

6. **Trusted Statistics**
   Python calculates key metrics such as total anomalies, priority counts, maximum excess minutes, and average excess minutes.

7. **Gemini AI Analysis**
   The trusted analytical results and hospital-level anomaly report are provided to Gemini to generate an executive summary, key findings, recommended actions, and data limitations.

8. **AI Response Validation**
   AI-generated numerical values are compared against the trusted Python calculations to ensure the reported metrics match the source analysis.

9. **Interactive AI Chatbot**
   Users can ask free-text questions about the hospital anomaly report. The chatbot is instructed not to invent causes or information that is not supported by the provided data.

10. **Tableau Dashboard**
    The analyzed data is visualized through an interactive Tableau dashboard containing KPIs, priority distribution, top facilities by excess minutes, and a state-level map.

**7. Anomaly Detection**

The anomaly detection process was performed using Python and pandas before any AI-generated analysis was introduced.

### Emergency Department Analysis

The CMS dataset was filtered to identify Emergency Department performance measures. Performance scores were converted into numeric values and analyzed to identify facilities with elevated excess minutes.

A performance threshold was established to identify facilities requiring further operational review.

Facilities exceeding the threshold were classified as anomalies and assigned severity categories based on the magnitude of their excess minutes.

### Severity Classification

Detected facilities were categorized into the following severity levels:

* **Normal** — No anomaly detected
* **Low** — Lower-level anomaly
* **Moderate** — Moderate anomaly
* **High** — High-severity anomaly
* **Severe** — Highest-severity anomaly

The resulting analysis identified:

| Severity | Facilities |
| -------- | ---------: |
| Normal   |      4,592 |
| Low      |         22 |
| Moderate |         17 |
| High     |         16 |
| Severe   |         11 |

### Operational Priority

Severity categories were mapped to operational priority levels:

| Severity | Priority |
| -------- | -------- |
| Severe   | Critical |
| High     | High     |
| Moderate | Medium   |
| Low      | Low      |

This resulted in **66 anomalous facilities**:

| Priority | Facilities |
| -------- | ---------: |
| Critical |         11 |
| High     |         16 |
| Medium   |         17 |
| Low      |         22 |

### Anomaly Report

The final anomaly report contains:

* Facility ID
* Facility name
* State
* Performance score
* Excess minutes
* Severity category
* Priority level
* Recommended operational action

The report was exported as:

`hospital_ed_anomaly_report.csv`

This structured report serves as the trusted analytical source for the subsequent AI reporting and Tableau visualization stages.

**8. AI-Powered Reporting**

Google Gemini is integrated into the project to automate the interpretation and communication of hospital anomaly results.

The AI layer does not perform the underlying anomaly calculations. Instead, trusted statistics and the hospital-level anomaly report generated by Python are provided to Gemini as controlled inputs.

### AI-Generated Executive Report

Gemini generates a structured executive report containing:

* Executive summary
* Key findings
* Recommended actions
* Data limitations

The AI response is generated using a structured response schema to ensure the expected fields and data types are returned consistently.

### AI Guardrails

The system prompt instructs Gemini to:

* Use only the data supplied to the model.
* Avoid inventing facts.
* Avoid inferring causes that are not supported by the data.
* Clearly state when the available data cannot answer a question.
* Focus responses on anomalies, severity, priority, excess minutes, facility details, and recommended actions.

For example, when asked why a facility experienced excess minutes, the chatbot correctly identifies that the cause cannot be determined from the supplied report rather than generating an unsupported explanation.

### AI Response Validation

AI-generated numerical results are validated against trusted Python calculations before the report is accepted.

The validation checks:

* Total anomaly count
* Critical cases
* High cases
* Medium cases
* Low cases
* Maximum excess minutes
* Average excess minutes
* Required response fields

The report is accepted only when the required fields are present and the AI-generated numerical values match the trusted Python statistics.

This approach provides a controlled workflow where:

Python calculates → Gemini interprets → Python validates

**9. Interactive AI Chatbot**

The project includes an interactive Gemini-powered chatbot that allows users to ask free-text questions about the hospital anomaly report.

The chatbot maintains conversation history, allowing users to ask follow-up questions without resending the entire dataset with every question.

### Example Questions

Users can ask questions such as:

* How many critical hospitals are in the report?
* Which hospital has the highest excess minutes?
* How many critical hospitals are located in Texas?
* What recommended action is associated with a critical priority?
* What are the limitations of the report?

### Data-Bound Responses

The chatbot is designed to remain within the boundaries of the supplied data.

For example, when asked:

> "Why is MANATI MEDICAL CENTER DR OTERO LOPEZ experiencing a 123.875-minute excess?"

the chatbot responds that the cause cannot be determined from the available report rather than assuming a cause.

This prevents unsupported conclusions and demonstrates how LLM-based analytics can be combined with controlled data access and explicit response guardrails.

**10. Tableau Dashboard**

The analyzed hospital anomaly data is visualized through an interactive Tableau dashboard designed to help users quickly identify high-priority facilities and understand the distribution of anomalies.

Dashboard Features-
Total Anomalies KPI
Level wise Anomalies
State-Level Hospital Anomaly Map
Average Excess Minutes KPI
Maximum Excess Minutes KPI
Top 10 Hospitals by Excess Minutes
Detailed Level View

Interactive filtering by state and priority

Link to the Dashboard - https://public.tableau.com/app/profile/akshara6899/viz/HospitalAnomaliesDashboard/KPIDashboard

## Key Results

The completed analysis produced the following results:

### Hospital Anomaly Detection

* Identified **66 hospitals** with Emergency Department performance anomalies.
* Classified anomalies into four operational priority levels:

  * **11 Critical**
  * **16 High**
  * **17 Medium**
  * **22 Low**
* The highest observed excess time was **123.88 minutes**.
* The average excess time across anomalous facilities was **30.89 minutes**.

### Highest-Priority Finding

The hospital with the highest excess minutes was:

* **MANATI MEDICAL CENTER DR OTERO LOPEZ**
* Facility ID: **400114**
* State: **Puerto Rico**
* Excess minutes: **123.875**
* Severity: **Severe**
* Priority: **Critical**

### AI Reporting Results

The AI reporting layer successfully:

* Generated a structured executive summary from trusted analytical results.
* Produced key findings and recommended operational actions.
* Included data limitations to prevent unsupported conclusions.
* Passed validation against the trusted Python-calculated metrics.
* Supported natural-language questions through the interactive chatbot.

### Overall Outcome

The project demonstrates an end-to-end approach for transforming raw healthcare performance data into:

**Analyzed Data → Prioritized Anomalies → Validated AI Insights → Interactive Business Intelligence**

This provides a reusable framework for combining traditional data analytics, AI-assisted reporting, and business intelligence visualization in a healthcare analytics workflow.

## How to Run

### 1. Clone the Repository

Clone the repository to your local machine and navigate to the project directory.

### 2. Install Required Python Libraries

Install the required Python packages:

```bash
pip install pandas numpy google-genai
```

### 3. Run the Data Pipeline

Run the scripts in the following order:

#### Step 1 — Retrieve the CMS Data

```bash
python "API & DF Creation.py"
```

This retrieves the hospital performance data from the CMS public API and creates the initial dataset.

#### Step 2 — Clean and Analyze the Data

```bash
python "Data Cleaning.py"
```

This prepares the data, performs the Emergency Department analysis, identifies anomalies, assigns severity and priority levels, and generates:

```text
hospital_ed_anomaly_report.csv
```

#### Step 3 — Generate the AI Report and Chatbot

```bash
python "AI_Report & Chatbot.py"
```

This uses Google Gemini to:

* Generate the structured AI executive report.
* Validate AI-generated numerical results against Python calculations.
* Save the validated AI report as `hospital_ai_report.json`.
* Start the interactive AI chatbot.

### 4. Configure the Gemini API Key

The Gemini API requires a valid API key.

For security, store the API key as an environment variable rather than hard-coding it directly in the Python script.

Example:

```bash
export GEMINI_API_KEY="your_api_key"
```

Then configure the Python application to read the key from the environment.

> **Security Note:** Never commit API keys or other credentials to GitHub.

### 5. Tableau Dashboard

The final `hospital_ed_anomaly_report.csv` can be loaded into Tableau to reproduce the dashboard analysis.

The published Tableau dashboard is available through Tableau Public.

## Future Enhancements

Potential enhancements to the project include:

* **Automated Data Refresh**
  Schedule the CMS data pipeline to automatically retrieve and process updated hospital performance data.

* **Expanded Hospital Metrics**
  Incorporate additional CMS quality and operational measures beyond Emergency Department performance.

* **Historical Trend Analysis**
  Track hospital performance over multiple reporting periods to identify recurring or improving performance patterns.

* **Advanced Anomaly Detection**
  Explore statistical or machine learning approaches for detecting unusual hospital performance patterns.

* **Automated Dashboard Refresh**
  Connect the analytical pipeline to a regularly refreshed visualization layer.

* **Enhanced AI Reporting**
  Expand the AI reporting layer to support additional executive questions and comparisons across hospitals, states, and priority levels.

* **Improved Data Governance**
  Add data-quality checks, lineage tracking, and logging to make the pipeline more robust for production environments.

* **Deployment**
  Package the analytics and AI workflow into a deployable application or scheduled reporting service.






