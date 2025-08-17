"""
EIA Petroleum Data Fetcher

This module handles the extraction of petroleum price data from the U.S. Energy Information Administration (EIA) API.
It retrieves annual fuel price data for various petroleum products across different U.S. regions from 2000-2024.

Key Features:
- Configurable API request parameters for different petroleum products and regions
- Automatic data validation and error handling
- Local caching of raw data in CSV format
- Directory structure management

API Endpoint:
https://api.eia.gov/v2/petroleum/pri/gnd/data/

Parameters:
- Products: Diesel (No 2, Ultra-Low Sulfur) and Gasoline (Total, Regular, Premium, Reformulated)
- Regions: National (NUS) and PADD regions (1-5, California)
- Timeframe: 2000-2024 (annual frequency)

Usage:
>>> from fetch_data import fetch_petroleum_data
>>> api_key = "your_eia_api_key"
>>> petroleum_data = fetch_petroleum_data(api_key)

Output:
- Returns: Pandas DataFrame containing raw API response data
- Saves: Raw data CSV at 'data/raw/petroleum_raw.csv'

Error Handling:
- Raises RuntimeError for failed API requests (non-200 status codes)
- Creates empty file if response contains no data

Dependencies:
- requests (API communication)
- pandas (data handling)
- pathlib, os (file system operations)
"""

# Importing necessary libraries
import os
import requests
import pandas as pd
from pathlib import Path
PLOT_DIR = os.path.join("outputs", "plots")
os.makedirs(PLOT_DIR, exist_ok=True)


# Data Fetching
def fetch_petroleum_data(api_key):
    """
    Fetch petroleum price data from EIA API.
    
    Args:
        api_key (str): EIA API authentication key
        
    Returns:
        pd.DataFrame: Contains petroleum price data with columns:
            - period (str): Year of record
            - value (float): Price value
            - product (str): Fuel product code
            - duoarea (str): Region code
            - process (str): Always 'PTE' (Price to End User)
            
    Raises:
        RuntimeError: If API request fails (non-200 status code)
    """
    url = "https://api.eia.gov/v2/petroleum/pri/gnd/data/"

    params = {
        "api_key": api_key,
        "frequency": "annual",
        "data[0]": "value",
        "facets[product][]": ["EPD2D", "EPD2DXL0", "EPM0", "EPM0R", "EPMP", "EPMR"],
        "facets[duoarea][]": [
            "NUS",
            "R10",
            "R1X",
            "R1Y",
            "R20",
            "R30",
            "R40",
            "R50",
            "R5XCA",
            "SCA",
        ],
        "facets[process][]": ["PTE"],
        "start": "2000",
        "end": "2024",
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": "0",
        "length": "5000",
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"API request failed: {response.status_code}")

    data = response.json().get("response", {}).get("data", [])
    df = pd.DataFrame(data)
    # Ensure data directory exists
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Export raw data to CSV
    csv_path = raw_dir / "petroleum_raw.csv"
    df.to_csv(csv_path, index=False)
    if not df.empty:
        df.to_csv(csv_path, index=False)
    else:
        csv_path.touch()

    return df if data else pd.DataFrame()
