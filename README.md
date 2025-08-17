# Petroleum Data Dashboard

## Overview
This project fetches, cleans, and visualizes petroleum production and consumption data.  
It uses Python scripts to retrieve raw datasets, process them, and generate interactive visualizations using Plotly.

## Features
- **Data Fetching** — Downloads petroleum data from source APIs or CSV files.
- **Data Cleaning** — Handles missing values, standardizes formats, and prepares datasets for analysis.
- **Visualization** — Creates interactive dashboards using Plotly.
- **Modular Structure** — Easy to extend with additional scripts.

## Project Structure
Fuel_Price_Analysis_USA/
├── main.py # Main entry point for running the project
├── requirements.txt # Python dependencies
├── scripts/ # Core processing scripts
├── data/ # Raw and processed datasets
├── outputs/ # Generated charts and reports
└── docs/ # Documentation


## Installation
1. **Clone the Repository**
   ```bash
   git clone <your-repo-url> Fuel_Price_Analysis_USA
   cd Fuel_Price_Analysis_USA

2. **Set Up a Virtual Environment**
python3 -m venv FPAUA_env
source FPAUA_env/bin/activate

3. **Install Dependencies**
pip install -r requirements.txt



## Usage 
1. **Run the Main Script**
python3 main.py
2. **Run Individual Scripts**
python3-m scripts.fetch_data
python3 -m scripts.clean_data
python3 -m scripts.visualize_plotly

## Data
- Raw Data is stored in `data/raw/`

- Processed Data is stored in data`/processed/`

## Outputs

- Generated charts are stored in `outputs/charts/`

- Reports are stored in `outputs/reports/`
## Requirements

- Python 3.10+
- Install dependencies 

pip install -r requirements.txt

**Included Libraries:**
pandas — Data handling

numpy — Numerical operations

requests — API data fetching

matplotlib — Basic visualizations

seaborn — Statistical plotting

plotly — Interactive visualizations

python-dotenv — Environment variable management

## License

This project is licensed under the MIT License.