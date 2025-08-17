"""
Seaborn Visualization Module for Petroleum Data

This module provides a suite of visualization functions for petroleum price analysis,
creating publication-quality plots using Seaborn and Matplotlib. All plots are 
automatically saved to the outputs/plots directory with date-stamped filenames.

Key Features:
- Consistent styling across all visualizations
- Automatic directory creation for outputs
- Date-stamped output filenames
- Five distinct plot types for different analytical perspectives
- Tight layout management for professional presentation

Available Visualizations:
1. Scatter plot: Fuel product price distribution
2. Line chart: Price trends over time
3. Bar chart: Regional cost comparisons
4. Bar chart: Fuel type cost comparisons
5. Line chart: National vs state trends

Usage:
>>> from visualize_seaborn import set_plot_style, plot_scatter, plot_price_trend
>>> set_plot_style()  # Initialize styling
>>> plot_scatter(cleaned_df)  # Generate scatter plot
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date

# Ensure outputs folder exists
PLOT_DIR = os.path.join("outputs", "plots")
os.makedirs(PLOT_DIR, exist_ok=True)


# visualization
def set_plot_style():
    """
    Configures the base styling for all plots in the module.
    
    Applies:
    - Whitegrid theme
    - DejaVu Serif font family
    - Consistent font sizing (titles 14pt, labels 12pt, ticks 10pt)
    """
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "axes.titlesize": 14,
            "axes.labelsize": 12,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        }
    )


def plot_scatter(df):
    """
    Creates a scatter plot of fuel product prices.
    
    Args:
        df (pd.DataFrame): Cleaned petroleum data containing:
            - value: Price values
            - product-name: Fuel product categories
            
    Outputs:
        Saves scatter plot to: outputs/plots/Fuel_Product_Prices_YYYY-MM-DD.png
    """
    plt.figure(figsize=(14, 7))
    sns.scatterplot(
        x="value",
        y="product-name",
        data=df,
        size="value",
        hue="value",
        sizes=(50, 200),
        palette="viridis",
        alpha=0.7,
    )
    plt.title("Fuel Product Prices ($/Gallon)", pad=20)
    plt.xlabel("Cost ($/GAL)")
    plt.ylabel("Product Type")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    today_str = date.today().strftime("%Y-%m-%d")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, f"Fuel_Product_Prices_{today_str}.png"),dpi=300,bbox_inches="tight")


def plot_price_trend(df):
    """
    Creates a line plot showing price trends over time by product.
    
    Args:
        df (pd.DataFrame): Must contain:
            - period: Datetime values
            - value: Price values
            - product-name: Fuel categories
            
    Outputs:
        Saves line plot to: outputs/plots/Prices_Trend_Over_the_Years_YYYY-MM-DD.png
    """
    plt.figure(figsize=(14, 7))
    sns.lineplot(x="period", y="value", data=df, hue="product-name", palette="husl")
    plt.xticks(rotation=60)
    plt.title("Prices ($/Gallon) Trend Over the Years", pad=20)
    plt.xlabel("Year")
    plt.ylabel("Cost ($/GAL)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    today_str = date.today().strftime("%Y-%m-%d")
    plt.tight_layout()
    plt.savefig(
        os.path.join(PLOT_DIR, f"Prices_Prices_Trend_Over_the_Years_{today_str}.png"),dpi=300,bbox_inches="tight"
    )
    


def plot_regional_cost(df):
    """
    Creates a bar plot comparing regional costs by product (2024-2025).
    
    Args:
        df (pd.DataFrame): Must contain:
            - period: Filtered to 2024-2025
            - area-name: Region categories
            - product-name: Fuel types
            - value: Price values
            
    Outputs:
        Saves bar plot to: outputs/plots/Regional_Cost_by_Area_and_Product_YYYY-MM-DD.png
    """
    data_2024_25 = df[df["period"].dt.year.isin([2024, 2025])]
    plt.figure(figsize=(14, 7))
    sns.barplot(data=data_2024_25, x="area-name", y="value", hue="product-name")
    plt.xticks(rotation=60)
    plt.title("Regional Cost by Area and Product (2024–2025)", pad=20)
    plt.ylabel("Cost ($/GAL)")
    plt.xlabel("Region")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    today_str = date.today().strftime("%Y-%m-%d")
    plt.tight_layout()
    plt.savefig(
        os.path.join(PLOT_DIR, f"Regional_Cost_by_Area_and_Product_{today_str}.png"),dpi=300,bbox_inches="tight"
    )
    


def plot_fuel_type_comparison(df):
    """
    Generate and save a static bar chart comparing fuel prices by product type (2024-2025).
    
    Creates a grouped bar chart showing cost comparisons between different fuel products
    for years 2024 and 2025, with prices grouped by product type and differentiated by year.

    Args:
        df (pd.DataFrame): Cleaned petroleum data containing:
            - period (datetime): Must include 2024 and 2025 data
            - value (numeric): Price values
            - product-name (str): Fuel product categories
            
    Outputs:
        Saves PNG file to: outputs/plots/Fuel_Type_Cost_Comparison_YYYY-MM-DD.png
        
    Example:
        >>> plot_fuel_type_comparison(cleaned_data)
    """
    data_2024_25 = df[df["period"].dt.year.isin([2024, 2025])]
    plt.figure(figsize=(14, 7))
    sns.barplot(data=data_2024_25, x="product-name", y="value", hue="period")
    plt.xticks(rotation=45)
    plt.title("Fuel type Cost by Area and Time (2024–2025)", pad=20)
    plt.ylabel("Cost ($/GAL)")
    plt.xlabel("Product Name")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    today_str = date.today().strftime("%Y-%m-%d")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, f"Fuel_Type_Cost_Comparison_{today_str}.png"),dpi=300,bbox_inches="tight")
    

def plot_us_trend_vs_states(df):
    """
    Generate and save a static line chart comparing national vs state-level fuel price trends.
    
    Creates a multi-line plot showing fuel price trends over time, comparing the
    national average against individual state/regional trends. Uses a qualitative
    color palette to distinguish between regions.

    Args:
        df (pd.DataFrame): Cleaned petroleum data containing:
            - period (datetime): Time series data
            - value (numeric): Price values
            - area-name (str): Region/state identifiers
            
    Outputs:
        Saves PNG file to: outputs/plots/U_S_National_Trend_vs_States_YYYY-MM-DD.png
        
    Example:
        >>> plot_us_trend_vs_states(cleaned_data)
    """
    plt.figure(figsize=(14, 7))
    sns.lineplot(x="period", y="value", data=df, hue="area-name", palette="tab20")
    plt.xticks(rotation=60)
    plt.title("U.S. National Trend vs States", pad=20)
    plt.ylabel("Cost ($/GAL)")
    plt.xlabel("Year")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    today_str = date.today().strftime("%Y-%m-%d")
    plt.tight_layout()
    plt.savefig(
        os.path.join(PLOT_DIR, f"U_S__National_Trend_vs_States_{today_str}.png"),dpi=300,bbox_inches="tight"
    )
    

print(f"✅ All Seaborn plots saved in '{PLOT_DIR}'")
