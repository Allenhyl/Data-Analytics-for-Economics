# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:08:03 2025

@author: Allen
"""

import requests
import pandas as pd

# Your Census API Key
api_key = "cf7da88575f52a7d85c4a291d7f1b3dd8f20fdea"

# Census API endpoint for ACS 5-Year Data (2023)
base_url = "https://api.census.gov/data/2023/acs/acs5"

# Variables to fetch
variables = ["B25071_001E"]  # Median Gross Rent as % of Income
fields = ",".join(variables)

# Fetch data for all counties
params = {
    "get": f"{fields},NAME",
    "for": "county:*",
    "key": api_key
}

# Request Data
response = requests.get(base_url, params=params)
data = response.json()

# Convert to DataFrame
columns = ["Median Rent % Income", "County", "State Code", "County Code"]
df = pd.DataFrame(data[1:], columns=columns)

# Convert Rent % Income to numeric
df["Median Rent % Income"] = pd.to_numeric(df["Median Rent % Income"], errors="coerce")

# Merge with state FIPS codes for easier mapping
state_fips_url = "https://www2.census.gov/geo/docs/reference/state.txt"
state_fips = pd.read_csv(state_fips_url, sep="|", usecols=["STATE", "STUSAB"])
state_fips["STATE"] = state_fips["STATE"].astype(str).str.zfill(2)

# Merge Data
df = df.merge(state_fips, left_on="State Code", right_on="STATE", how="left").drop(columns=["STATE"])
df.rename(columns={"STUSAB": "State"}, inplace=True)

# Save to CSV for Tableau
df.to_csv("housing_costs.csv", index=False)

print("Data saved to housing_costs.csv")
