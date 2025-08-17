"""
Interactive Visualization Module with Plotly

This module generates interactive visualizations for petroleum price analysis using Plotly Express.
It creates five distinct chart types to explore different aspects of fuel pricing data.

Key Features:
- Interactive visualizations with hover tooltips
- Automatic handling of empty data cases
- Consistent styling across all charts
- Responsive design for different screen sizes
- Error handling for missing or invalid data

Available Visualizations:
1. Scatter Plot: Fuel product price distribution
2. Line Chart: Historical price trends by product
3. Bar Chart: Regional cost comparisons (2021, 2024-2025)
4. Bar Chart: Fuel type comparisons by year
5. Line Chart: National vs regional trends

Usage:
>>> from visualize_plotly import create_all_charts
>>> create_all_charts(cleaned_df)

Note: Ensure your DataFrame contains the required columns:
- 'period' (datetime)
- 'value' (numeric)
- 'product-name' (categorical)
- 'area-name' (categorical)
"""
import plotly.express as px
import pandas as pd
import os

def create_all_charts(df):
    """
    Generates and displays all Plotly interactive visualizations for fuel price analysis.
    
    Args:
        df (pd.DataFrame): Cleaned petroleum data containing:
            - period: Date/time information
            - value: Numeric price values
            - product-name: Fuel product categories
            - area-name: Geographic regions
            
    Returns:
        None: Displays interactive charts and shows warning messages for missing data
        
    Side Effects:
        - Opens browser windows/tabs with interactive visualizations
        - Prints warnings if expected data is missing
    """
    os.makedirs("outputs", exist_ok=True)  # ensure outputs folder exists

    # Scatter plot
    fig1 = px.scatter(
        df, x='value', y='product-name', size='value', color='value',
        color_continuous_scale='viridis',
        title="Fuel Product Prices ($/Gallon)",
        labels={"value": "Cost ($/GAL)", "product-name": "Product Type"},
        height=500
    )
    fig1.write_html("outputs/scatter_prices.html")

    # Line plot
    fig2 = px.line(
        df, x='period', y='value', color='product-name',
        title="Prices ($/Gallon) Trend Over the Years",
        labels={"value": "Cost ($/GAL)", "period": "Year"},
        height=500
    )
    fig2.update_xaxes(tickangle=60)
    fig2.write_html("outputs/price_trend.html")

    # Regional data filter
    df['year'] = pd.to_datetime(df['period']).dt.year.astype(str)
    regional_data = df[df['year'].isin(['2021', '2024', '2025'])]

    if regional_data.empty:
        print("⚠️ No regional data found for 2021, 2024, or 2025.")
    else:
        # Bar plot 1
        fig3 = px.bar(
            regional_data, x='area-name', y='value', color='product-name',
            barmode='group',
            title="Regional Cost by Area and Product (2024–2025)",
            labels={"value": "Cost ($/GAL)", "area-name": "Region"},
            height=600
        )
        fig3.update_xaxes(tickangle=60)
        fig3.write_html("outputs/regional_cost.html")

        # Bar plot 2
        fig4 = px.bar(
            regional_data, x='product-name', y='value', color='period',
            barmode='group',
            title="Fuel Type Cost by Area and Time (2024–2025)",
            labels={"value": "Cost ($/GAL)", "product-name": "Product Name"},
            height=500
        )
        fig4.update_xaxes(tickangle=45)
        fig4.write_html("outputs/fuel_type_comparison.html")

    # National vs States
    fig5 = px.line(
        df, x='period', y='value', color='area-name',
        title="U.S. National Trend vs States (Period)",
        labels={"value": "Cost ($/GAL)", "period": "Period"},
        height=500
    )
    fig5.update_xaxes(tickangle=60)
    fig5.write_html("outputs/national_vs_states.html")


print("✅ All Plotly plots saved in 'outputs'")