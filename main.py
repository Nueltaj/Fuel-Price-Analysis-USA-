"""
Petroleum Data Analysis Pipeline - Main Script

This script orchestrates the complete petroleum data analysis workflow:
1. Fetches raw petroleum data from the EIA API
2. Cleans and processes the data
3. Generates both static (Matplotlib/Seaborn) and interactive (Plotly) visualizations
4. Saves raw and processed data to designated directories

Key Features:
- Modular architecture with separate scripts for data operations
- Environment variable support for API keys
- Automatic directory creation for data storage
- Dual visualization outputs (static PNGs and interactive HTML)

Usage:
- Set EIA_API_KEY in environment variables 
- Run directly: `python main.py`

Outputs:
- Raw data: data/raw/petroleum_raw.csv
- Cleaned data: data/processed/petroleum_clean.csv
- Visualizations displayed (Matplotlib) and saved (Plotly)
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from scripts.fetch_data import fetch_petroleum_data
import os
import matplotlib.pyplot as plt
from scripts.clean_data import clean_petroleum_data
from scripts.visualize_seaborn import (
    set_plot_style,
    plot_scatter,
    plot_price_trend,
    plot_regional_cost,
    plot_fuel_type_comparison,
    plot_us_trend_vs_states
)
from scripts.visualize_plotly import create_all_charts

if __name__ == "__main__":
    set_plot_style()

    # Fetch
    API_KEY = os.getenv("EIA_API_KEY", "eg3hiIakLLsprBiSiTVP4C1Wz0NeLYPLISKYe5ap")
    df = fetch_petroleum_data(API_KEY)

    # Save raw
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/petroleum_raw.csv", index=False)

    # Clean
    df = clean_petroleum_data(df)

    # Save processed
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/petroleum_clean.csv", index=False)

    # Visualize (Seaborn)
    plot_scatter(df)
    plot_price_trend(df)
    plot_regional_cost(df)
    plot_fuel_type_comparison(df)
    plot_us_trend_vs_states(df)

    # Visualize (Plotly)
    create_all_charts(df)

    # to show the charts
    plt.show()
