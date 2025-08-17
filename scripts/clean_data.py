"""
Petroleum Data Cleaning Module

This script performs comprehensive cleaning and preprocessing of petroleum price data from the EIA.
It handles data quality issues, standardizes formats, and prepares the dataset for analysis.

Key Cleaning Operations:
1. Data Type Conversion: Ensures proper datetime and numeric formats
2. Temporal Filtering: Focuses on data from 1990-2025
3. Missing Value Treatment: 
   - Numeric: Median imputation
   - Categorical: Mode imputation
4. Text Standardization: 
   - Trimming whitespace
   - Title case conversion
5. Outlier Removal: Using IQR method (1.5*IQR rule)
6. Value Mapping: 
   - Standardizes region codes to human-readable names
   - Converts product codes to descriptive labels

Input Requirements:
- DataFrame containing raw petroleum data with expected columns:
  - period (date/time)
  - value (numeric)
  - area-name/product-name/process-name (categorical)
  - duoarea/product (for mapping)

Output:
- Cleaned DataFrame with consistent formatting
- CSV file saved to: data/processed/petroleum_clean.csv

Usage:
Import and use the clean_petroleum_data() function:
>>> from clean_data import clean_petroleum_data
>>> cleaned_df = clean_petroleum_data(raw_df)

Error Handling:
- Silent handling of conversion errors (coerce)
- Empty file creation if DataFrame is empty
- Automatic directory creation for outputs

Dependencies:
- pandas, numpy, pathlib, os
"""

# Importing necessary libraries
import os
import pandas as pd
import numpy as np
from pathlib import Path
PLOT_DIR = os.path.join("outputs", "plots")
os.makedirs(PLOT_DIR, exist_ok=True)


# Data cleaning
def clean_petroleum_data(df):
    """
    Cleans and preprocesses raw petroleum price data from EIA API.
    
    Args:
        df (pd.DataFrame): Raw petroleum data containing at minimum:
            - period: Date/time information
            - value: Numeric price values
            - Various categorical columns (area-name, product-name, etc.)
            
    Returns:
        pd.DataFrame: Cleaned dataset with:
            - Proper data types
            - Handled missing values
            - Standardized text formats
            - Removed outliers
            - Mapped categorical values
            
    Side Effects:
        - Creates 'data/cleaned' directory if missing
        - Saves cleaned data to 'data/cleaned/fuel_prices_cleaned.csv'
    """
    # Convert types
    df['period'] = pd.to_datetime(df['period'], errors='coerce')
    df = df[df['period'].dt.year.between(1990, 2025)]
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Fill missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    for col in df.select_dtypes(exclude=[np.number]).columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Format text columns
    for col in ['area-name', 'product-name', 'process-name']:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    # Remove outliers
    Q1, Q3 = df['value'].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    df = df[(df['value'] >= (Q1 - 1.5 * IQR)) & (df['value'] <= (Q3 + 1.5 * IQR))]

    # Mapping
    area_map = {
        'NUS': 'United States',
        'R10': 'PADD 1 (East Coast)',
        'R1X': 'PADD 1A (New England)',
        'R1Y': 'PADD 1B (Central Atlantic)',
        'R20': 'PADD 2 (Midwest)',
        'R30': 'PADD 3 (Gulf Coast)',
        'R40': 'PADD 4 (Rocky Mountain)',
        'R50': 'PADD 5 (West Coast)',
        'R5XCA': 'PADD 5 (Except California)',
        'SCA': 'California',
    }
    product_map = {
        'EPD2D': 'No 2 Diesel',
        'EPD2DXL0': 'Ultra-Low Sulfur Diesel (0–15 ppm)',
        'EPM0': 'Total Gasoline',
        'EPMR': 'Regular Gasoline',
        'EPMP': 'Premium Gasoline',
        'EPM0R': 'Reformulated Motor Gasoline',
    }
    if 'product' in df.columns:
        df['product'] = df['product'].map(product_map).fillna(df['product'])
    if 'duoarea' in df.columns:
        df['duoarea'] = df['duoarea'].map(area_map).fillna("Unknown")

    # Ensure data directory exists
    cleaned_dir = Path("data/processed")
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    # Export cleaned data to CSV
    csv_path = cleaned_dir / "petroleum_clean.csv"
    df.to_csv(csv_path, index=False)
    if not df.empty:
        df.to_csv(csv_path, index=False)
    else:
        csv_path.touch()
    return df


