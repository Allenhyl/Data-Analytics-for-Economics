# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:35:02 2025

@author: Allen
"""

import requests
import pandas as pd

# BEA API Key
API_KEY = "C9CADE2A-C215-42B3-B153-1C7494523FFA"

# BEA API URL
BEA_URL = "https://apps.bea.gov/api/data"

# Parameters for Real GDP (RGDP) in Chained Dollars (Table 1.1.6)
rgdp_params = {
    "UserID": API_KEY,
    "method": "GetData",
    "datasetname": "NIPA",
    "TableName": "T10106",  # Table 1.1.6 for Real GDP (Chained Dollars)
    "Frequency": "A",  # Annual Data
    "Year": "ALL",  # Fetch all available years
    "ResultFormat": "json"
}

# Parameters for GDP Deflator (Table 1.1.9, Line 1: Gross Domestic Product Implicit Price Deflator)
gdp_deflator_params = {
    "UserID": API_KEY,
    "method": "GetData",
    "datasetname": "NIPA",
    "TableName": "T10109",  # Table 1.1.9 for GDP Implicit Price Deflator
    "Frequency": "A",  # Annual Data
    "Year": "ALL",  # Fetch all available years
    "ResultFormat": "json"
}

# Fetch Real GDP Data
rgdp_response = requests.get(BEA_URL, params=rgdp_params)
rgdp_data = rgdp_response.json()

# Fetch GDP Deflator Data
gdp_deflator_response = requests.get(BEA_URL, params=gdp_deflator_params)
gdp_deflator_data = gdp_deflator_response.json()

# Extract RGDP Data
rgdp_records = []
for item in rgdp_data["BEAAPI"]["Results"]["Data"]:
    if item["LineNumber"] == "1":  # Line 1 represents GDP in chained dollars
        rgdp_records.append({
            "Year": int(item["TimePeriod"]),  # Use TimePeriod for Year
            "RGDP": float(item["DataValue"].replace(",", ""))  # Remove commas
        })

df_rgdp = pd.DataFrame(rgdp_records)

# Extract GDP Deflator Data
gdp_deflator_records = []
for item in gdp_deflator_data["BEAAPI"]["Results"]["Data"]:
    if item["LineNumber"] == "1":  # Line 1 represents GDP Deflator
        gdp_deflator_records.append({
            "Year": int(item["TimePeriod"]),  # Use TimePeriod for Year
            "GDP Deflator": float(item["DataValue"].replace(",", ""))  # Remove commas
        })

df_gdp_deflator = pd.DataFrame(gdp_deflator_records)

# Merge the datasets on Year
df_adas = pd.merge(df_rgdp, df_gdp_deflator, on="Year")

# Save to CSV for Tableau
df_adas.to_csv("adas_gdp_deflator.csv", index=False)

df_adas.head()