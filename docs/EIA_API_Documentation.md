# 🛢️ EIA Petroleum API Documentation

**API Provider:** U.S. Energy Information Administration (EIA)  
**Base URL:** `https://api.eia.gov/v2/`  
**Documentation:** [Official EIA API Guide](https://www.eia.gov/opendata/documentation.php)  
**Project:** Petroleum Market Intelligence Analysis  

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Petroleum Price Endpoint](#petroleum-price-endpoint)
4. [Request Parameters](#request-parameters)
5. [Response Structure](#response-structure)
6. [Code Examples](#code-examples)
7. [Data Dictionary](#data-dictionary)
8. [Rate Limits & Best Practices](#rate-limits--best-practices)
9. [Troubleshooting](#troubleshooting)

---

## 🔍 Overview

The EIA API provides access to comprehensive energy data including petroleum prices, production, consumption, and inventory data. This documentation focuses on the **Petroleum Prices endpoint** used for fuel market analysis.

### Key Features:
- ✅ Real-time and historical petroleum price data
- ✅ Multiple product types (gasoline, diesel, jet fuel)
- ✅ Regional breakdowns (PADD regions, states)
- ✅ Various frequencies (annual, monthly, weekly, daily)
- ✅ JSON response format
- ✅ Free access with API key registration

---

## 🔐 Authentication

### API Key Registration
1. Visit: [EIA API Registration](https://www.eia.gov/opendata/register.php)
2. Provide email and basic information
3. Receive API key via email
4. Include key in all requests as `api_key` parameter

### Authentication Method
```
GET https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key=YOUR_API_KEY
```

**Security Note:** Keep your API key secure and never commit it to public repositories.

---

## ⛽ Petroleum Price Endpoint

### Primary Endpoint
```
GET https://api.eia.gov/v2/petroleum/pri/gnd/data/
```

### Endpoint Purpose
Retrieves petroleum product price data for various fuels across different geographic regions and time periods.

### Data Coverage
- **Time Range:** 2000 - Present
- **Update Frequency:** Weekly (typically Mondays)
- **Geographic Coverage:** National, PADD regions, selected states
- **Product Coverage:** Gasoline, diesel, heating oil, jet fuel

---

## 🎛️ Request Parameters

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `api_key` | string | Your EIA API authentication key | `your_api_key_here` |

### Core Parameters

| Parameter | Type | Description | Options |
|-----------|------|-------------|---------|
| `frequency` | string | Data frequency | `annual`, `monthly`, `weekly`, `daily` |
| `data[0]` | string | Data series to retrieve | `value` (price data) |
| `start` | string | Start date | `2000` (for annual), `2000-01` (monthly) |
| `end` | string | End date | `2024` (for annual), `2024-12` (monthly) |
| `sort[0][column]` | string | Sort column | `period`, `area-name`, `product-name` |
| `sort[0][direction]` | string | Sort direction | `asc`, `desc` |
| `offset` | integer | Record offset for pagination | `0`, `100`, `500` |
| `length` | integer | Number of records to return | `5000` (max) |

### Filter Parameters (Facets)

#### Product Facets (`facets[product][]`)
| Code | Product Description |
|------|-------------------|
| `EPD2D` | No 2 Diesel |
| `EPD2DXL0` | No 2 Diesel Low Sulfur (0-15 ppm) |
| `EPM0` | Regular Gasoline |
| `EPM0R` | Premium Gasoline |
| `EPMP` | Reformulated Motor Gasoline |
| `EPMR` | Total Gasoline |

#### Geographic Facets (`facets[duoarea][]`)
| Code | Region Description |
|------|-------------------|
| `NUS` | United States |
| `R10` | PADD 1 (East Coast) |
| `R1X` | PADD 1A (New England) |
| `R1Y` | PADD 1B (Central Atlantic) |
| `R20` | PADD 2 (Midwest) |
| `R30` | PADD 3 (Gulf Coast) |
| `R40` | PADD 4 (Rocky Mountains) |
| `R50` | PADD 5 (West Coast) |
| `R5XCA` | PADD 5 Except California |
| `SCA` | California |

#### Process Facets (`facets[process][]`)
| Code | Process Description |
|------|-------------------|
| `PTE` | Petroleum Total Energy |

---

## 📊 Response Structure

### Successful Response Format
```json
{
  "response": {
    "data": [
      {
        "period": "2024",
        "area-name": "United States",
        "product-name": "Regular Gasoline",
        "process-name": "Petroleum Total Energy",
        "duoarea": "NUS",
        "product": "EPM0",
        "process": "PTE",
        "value": 3.52,
        "units": "dollars per gallon"
      }
    ],
    "total": 1250,
    "dateFormat": "YYYY",
    "frequency": "annual"
  },
  "request": {
    "command": "data",
    "params": {
      "frequency": "annual",
      "data": ["value"],
      "facets": {...},
      "start": "2000",
      "end": "2024"
    }
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `period` | string | Time period (year, month, date) |
| `area-name` | string | Geographic region name |
| `product-name` | string | Fuel product name |
| `value` | number | Price in dollars per gallon |
| `units` | string | Unit of measurement |
| `duoarea` | string | Geographic area code |
| `product` | string | Product code |

---

## 💻 Code Examples

### Basic Python Request
```python
import requests
import pandas as pd

def fetch_petroleum_data(api_key):
    url = "https://api.eia.gov/v2/petroleum/pri/gnd/data/"
    
    params = {
        "api_key": api_key,
        "frequency": "annual",
        "data[0]": "value",
        "facets[product][]": ["EPM0", "EPM0R", "EPMP"],  # Regular, Premium, Reformulated
        "facets[duoarea][]": ["NUS", "SCA", "R30"],      # US, California, Gulf Coast
        "facets[process][]": ["PTE"],
        "start": "2000",
        "end": "2024",
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": "0",
        "length": "5000"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['response']['data'])
        return df
    else:
        raise Exception(f"API request failed: {response.status_code}")
```

### JavaScript/Fetch Example
```javascript
async function fetchPetroleumData(apiKey) {
    const baseUrl = 'https://api.eia.gov/v2/petroleum/pri/gnd/data/';
    
    const params = new URLSearchParams({
        'api_key': apiKey,
        'frequency': 'annual',
        'data[0]': 'value',
        'start': '2000',
        'end': '2024',
        'length': '5000'
    });
    
    // Add array parameters
    ['EPM0', 'EPM0R', 'EPMP'].forEach(product => {
        params.append('facets[product][]', product);
    });
    
    const response = await fetch(`${baseUrl}?${params}`);
    const data = await response.json();
    
    return data.response.data;
}
```

### cURL Example
```bash
curl -X GET "https://api.eia.gov/v2/petroleum/pri/gnd/data/" \
  -G \
  --data-urlencode "api_key=YOUR_API_KEY" \
  --data-urlencode "frequency=annual" \
  --data-urlencode "data[0]=value" \
  --data-urlencode "facets[product][]=EPM0" \
  --data-urlencode "facets[duoarea][]=NUS" \
  --data-urlencode "start=2000" \
  --data-urlencode "end=2024"
```

---

## 📖 Data Dictionary

### Product Codes & Descriptions
| Code | Full Product Name | Market Segment |
|------|------------------|----------------|
| `EPM0` | Regular Gasoline | Consumer - Mass Market |
| `EPM0R` | Premium Gasoline | Consumer - Premium |
| `EPMP` | Reformulated Motor Gasoline | Consumer - Environmental |
| `EPMR` | Total Gasoline | Consumer - Aggregate |
| `EPD2D` | No 2 Diesel | Commercial - Standard |
| `EPD2DXL0` | No 2 Diesel Low Sulfur (0-15 ppm) | Commercial - Environmental |

### Geographic Regions (PADD System)
| PADD | Region Name | States Included | Market Characteristics |
|------|-------------|-----------------|----------------------|
| 1 | East Coast | CT, DE, FL, GA, ME, MD, MA, NH, NJ, NY, NC, PA, RI, SC, VT, VA, WV, DC | Import-dependent, high prices |
| 1A | New England | CT, ME, MA, NH, RI, VT | Heating oil demand, seasonal variation |
| 1B | Central Atlantic | DE, MD, NJ, NY, PA, DC | High population density, complex logistics |
| 2 | Midwest | IL, IN, IA, KS, KY, MI, MN, MO, NE, ND, OH, OK, SD, TN, WI | Agricultural demand, transportation hub |
| 3 | Gulf Coast | AL, AR, LA, MS, NM, TX | Refining center, lowest prices |
| 4 | Rocky Mountains | CO, ID, MT, UT, WY | Isolated market, limited refining |
| 5 | West Coast | AK, AZ, CA, HI, NV, OR, WA | Environmental regulations, CA dominance |

### Units of Measurement
- **Price Data:** Dollars per gallon (USD/gal)
- **Time Format:** YYYY (annual), YYYY-MM (monthly), YYYY-MM-DD (daily)
- **Precision:** Typically 2-3 decimal places for price data

---

## ⚡ Rate Limits & Best Practices

### Rate Limits
- **Request Limit:** No official limit, but recommended max 1000 requests/hour
- **Data Limit:** 5000 records per request maximum
- **Concurrent Requests:** Limit to 5 simultaneous requests

### Best Practices

#### 1. Efficient Data Retrieval
```python
# Good: Request specific data
params = {
    "facets[product][]": ["EPM0", "EPM0R"],  # Only needed products
    "facets[duoarea][]": ["NUS", "SCA"],     # Only needed regions
    "start": "2020",                         # Recent data only
    "end": "2024"
}

# Avoid: Requesting all available data
```

#### 2. Error Handling
```python
def safe_api_call(url, params, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
```

#### 3. Data Caching
```python
import os
from pathlib import Path

def cache_data(df, filename="petroleum_data.csv"):
    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache_dir / filename, index=False)
```

### API Etiquette
- ✅ Cache frequently used data
- ✅ Use appropriate date ranges
- ✅ Handle errors gracefully
- ✅ Include delays between bulk requests
- ❌ Don't hammer the API with rapid requests
- ❌ Don't request more data than needed

---

## 🔧 Troubleshooting

### Common Error Codes

| Code | Error Type | Description | Solution |
|------|------------|-------------|----------|
| `400` | Bad Request | Invalid parameters or syntax | Check parameter names and values |
| `403` | Forbidden | Invalid or missing API key | Verify API key is correct and active |
| `404` | Not Found | Invalid endpoint or data not available | Check endpoint URL and date ranges |
| `429` | Too Many Requests | Rate limit exceeded | Implement delays, reduce request frequency |
| `500` | Internal Server Error | EIA server issues | Wait and retry, check EIA status page |

### Common Issues & Solutions

#### Issue: Empty Response Data
```python
# Problem: No data returned
response = {"response": {"data": []}}

# Solutions:
# 1. Check date range is valid
# 2. Verify product/region codes exist
# 3. Confirm data is available for time period
```

#### Issue: Parameter Formatting
```python
# Wrong: Single parameter for multiple values
"facets[product]": ["EPM0", "EPM0R"]

# Correct: Array parameter format  
"facets[product][]": ["EPM0", "EPM0R"]
```

#### Issue: Large Dataset Handling
```python
def paginated_request(params, max_records=5000):
    all_data = []
    offset = 0
    
    while True:
        params['offset'] = offset
        params['length'] = max_records
        
        response = make_request(params)
        data = response['response']['data']
        
        if not data:
            break
            
        all_data.extend(data)
        offset += max_records
    
    return all_data
```

### Debugging Tips
1. **Test with minimal parameters first**
2. **Use browser/Postman to verify requests manually**
3. **Check EIA website for service status**
4. **Validate date formats and ranges**
5. **Confirm product/region codes in EIA documentation**

---

## 📞 Support & Resources

### Official Resources
- **EIA API Documentation:** [https://www.eia.gov/opendata/documentation.php](https://www.eia.gov/opendata/documentation.php)
- **Data Browser:** [https://www.eia.gov/opendata/browser/](https://www.eia.gov/opendata/browser/)
- **Registration:** [https://www.eia.gov/opendata/register.php](https://www.eia.gov/opendata/register.php)

### Community Resources
- **Stack Overflow:** `eia-api` tag
- **GitHub Examples:** Search for "EIA API Python"
- **Data Science Communities:** Reddit r/datasets, Kaggle forums

### Contact Information
- **EIA Support:** [https://www.eia.gov/about/contact/](https://www.eia.gov/about/contact/)
- **Technical Issues:** infoctr@eia.gov

---

**Documentation Maintained By:** Omotaje Emmanuel Oluwaferanmi  
**Last Updated:** August 16, 2025  
**Version:** 1.0  

*This documentation is based on practical implementation experience and official EIA API resources. Always refer to the official EIA documentation for the most current information.*