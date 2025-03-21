# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:12:54 2025

@author: Allen
"""
import pandas as pd
import pycountry_convert as pc

def get_continent(country_name):
    """
    Given a country name, return the corresponding continent name.
    If the country cannot be converted, return "Unknown".
    """
    try:
        # Convert country name to its alpha-2 country code
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        # Get the continent code from the country code
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        # Convert continent code to continent name (e.g., 'Europe', 'Asia')
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except Exception:
        return "Unknown"

# Replace 'world_happiness.csv' with your CSV file path
input_csv = "World Happiness Report.csv"
df = pd.read_csv(input_csv)

# Create a new 'Continent' column by applying the get_continent function to each country name
df["Continent"] = df["Country"].apply(get_continent)

# Save the updated DataFrame to a new CSV file
output_csv = "world_happiness_with_continent.csv"
df.to_csv(output_csv, index=False)

print(f"Successfully created '{output_csv}' with the Continent column.")
