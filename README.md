# Ethiopia Financial Inclusion Forecasting System

[![Unit Tests](https://github.com/Danielmituku/ethiopia-financial-inclusion-forecast/actions/workflows/unittests.yml/badge.svg)](https://github.com/Danielmituku/ethiopia-financial-inclusion-forecast/actions/workflows/unittests.yml)

🇪🇹 A forecasting system that tracks Ethiopia's digital financial transformation using time series methods, developed for the 10Academy Week 10 Challenge.

## 🎯 Project Objectives

Build a forecasting system that predicts Ethiopia's progress on two core dimensions of financial inclusion:

1. **Access** — Account Ownership Rate (% of adults with financial account or mobile money)
2. **Usage** — Digital Payment Adoption Rate (% of adults making/receiving digital payments)

### Key Questions
- What drives financial inclusion in Ethiopia?
- How do events like product launches, policy changes, and infrastructure investments affect inclusion outcomes?
- How will financial inclusion rates evolve in 2025-2027?

## 📊 Ethiopia's Financial Inclusion Context

| Year | Account Ownership | Change |
|------|------------------|--------|
| 2011 | 14% | — |
| 2014 | 22% | +8pp |
| 2017 | 35% | +13pp |
| 2021 | 46% | +11pp |
| 2024 | 49% | +3pp |

### Key 2024 Indicators
- Mobile money account ownership: 9.45%
- Digital payment adoption: ~35%
- Account for wage receipt: ~15%

## 🏗️ Project Structure

```
ethiopia-fi-forecast/
├── .github/workflows/
│   └── unittests.yml              # CI/CD pipeline
├── data/
│   ├── raw/                       # Starter dataset
│   │   ├── ethiopia_fi_unified_data.csv
│   │   └── reference_codes.csv
│   └── processed/                 # Analysis-ready data
│       ├── ethiopia_fi_enriched.csv
│       ├── event_indicator_matrix.csv
│       └── forecast_results.csv
├── notebooks/                     # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_impact_modeling.ipynb
│   └── 04_forecasting.ipynb
├── src/                           # Source code modules
│   ├── data_loader.py
│   ├── visualization.py
│   ├── forecasting.py
│   └── generate_report.py         # PDF report generator
├── scripts/
│   └── run_analysis.py            # Full pipeline runner
├── dashboard/
│   └── app.py                     # Streamlit dashboard
├── tests/                         # Unit tests
├── models/                        # Saved model artifacts
├── reports/
│   ├── figures/                   # Generated visualizations
│   ├── final_report.html          # HTML report
│   └── final_report.pdf           # PDF report
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Danielmituku/ethiopia-financial-inclusion-forecast.git
cd ethiopia-financial-inclusion-forecast

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard

```bash
streamlit run dashboard/app.py
```

### Running Notebooks

```bash
jupyter notebook notebooks/
```

### Running Tests

```bash
pytest tests/ -v
```

### Generating the Final Report

The project includes a PDF report generator using WeasyPrint:

```bash
# Generate the final PDF report
python src/generate_report.py

# Or run the full analysis pipeline (notebooks + report)
python scripts/run_analysis.py
```

Reports are saved to:
- `reports/final_report.html` - HTML version
- `reports/final_report.pdf` - PDF version (print-ready)

## 📁 Data Schema

The unified dataset uses a single schema where `record_type` determines interpretation:

| record_type | Description |
|-------------|-------------|
| observation | Measured values (Findex surveys, operator reports, infrastructure) |
| event | Policies, product launches, market entries, milestones |
| impact_link | Modeled relationships between events and indicators |
| target | Official policy goals (e.g., NFIS-II targets) |

## 📋 Tasks

- [x] **Task 1**: Data Exploration and Enrichment
- [x] **Task 2**: Exploratory Data Analysis
- [x] **Task 3**: Event Impact Modeling
- [x] **Task 4**: Forecasting Access and Usage
- [x] **Task 5**: Dashboard Development
- [x] **Task 6**: PDF Report Generation

## 📚 Key References

- [Global Findex Database](https://www.worldbank.org/globalfindex)
- [National Bank of Ethiopia](https://nbe.gov.et)
- [Forecasting: Principles and Practice](https://otexts.com/fpp3/)
- [Streamlit Documentation](https://docs.streamlit.io)

## 👥 Author

**Daniel Mituku** - [GitHub](https://github.com/Danielmituku)

## 📄 License

This project is developed for educational purposes as part of the 10 Academy Week 10 challenge.
