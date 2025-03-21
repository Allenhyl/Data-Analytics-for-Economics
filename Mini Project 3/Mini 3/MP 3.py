# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 19:00:20 2025

Mini Project 3 code, Hu Yinglun
"""
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the webpage content
url = 'https://starbucksmenuprices.com/'
response = requests.get(url)
if response.status_code == 200:
    print("Successfully fetched the webpage!")
else:
    print(f"Failed to fetch webpage. Status code: {response.status_code}")

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Find all <ul> elements
sections = soup.find_all('ul')

# Step 4: Extract links
country_links = []
for section in sections:
    links = section.find_all('a')
    for link in links:
        country_name = link.text.strip()
        country_url = link.get('href')
        country_links.append({'Country': country_name, 'URL': country_url})

# Step 5: Convert to DataFrame
df = pd.DataFrame(country_links)
print(df.head())  # Display the first 5 rows

# Step 6: Save to CSV
df.to_csv('starbucks_country_links.csv', index=False)
print("Saved country links to starbucks_country_links.csv")


# Step 1: Load the Links
links_file = 'starbucks_country_links.csv'  # File containing country links
country_links = pd.read_csv(links_file)  # Read the CSV file into a DataFrame

# Step 2: Filter Valid Links
valid_links = country_links[~country_links['URL'].str.contains('#', na=False)]  # Remove invalid URLs containing '#'

# Check if there are any valid links
if valid_links.empty:
    print("No valid links found in the file.")
    exit()

# Step 3: Loop Over All Valid Links
for index, row in valid_links.iterrows():
    country_url = row['URL']  # Extract the URL
    country_name = row['Country'].lower().replace(' ', '-')  # Format the country name for the file name

    print(f"Fetching data for {country_name} from {country_url}...")

    # Step 4: Fetch the Webpage Content
    response = requests.get(country_url)
    if response.status_code == 200:
        print(f"Successfully fetched the page: {country_url}")
    else:
        print(f"Failed to fetch webpage for {country_name}. Status code: {response.status_code}")
        continue  # Skip this country if the webpage request fails

    # Step 5: Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 6: Locate "h2" Section Containing Starbucks Prices
    starbucks_prices_heading = soup.find('h2')  # Locate the "h2" section heading
    if starbucks_prices_heading:
        starbucks_prices_table = starbucks_prices_heading.find_parent('table')  # Find the parent table containing the data
    else:
        print(f"'Hot Coffee' section not found for {country_name}. Skipping...")
        continue  # Skip to the next country if no relevant section is found
    # Step 7: Extract Data
    starbucks_prices_data = []  # List to store extracted data
    if starbucks_prices_table:
        rows = starbucks_prices_table.find_all('tr', class_='item')  # Find all rows with class "item"
        for row in rows:
            cols = row.find_all('td')  # Find all columns in the row
            cols = [col.string.strip() if col.string else '' for col in cols]  # Clean the text and handle missing values
            if cols:  # Skip empty rows
                starbucks_prices_data.append(cols)

    # Step 8: Save Data
    if starbucks_prices_data:
        df_starbucks_prices = pd.DataFrame(starbucks_prices_data, columns=['Item', 'Price'])  # Create a DataFrame
        output_file = f'starbucks_prices_{country_name}.csv'  # Generate file name with country name
        df_starbucks_prices.to_csv(output_file, index=False)  # Save to CSV
        print(f"Saved 'Starbucks Prices' prices to {output_file}")
    else:
        print(f"No 'Starbucks Prices Data' found for {country_name}. Skipping...")

# Step 1: Define the folder path containing the CSV files
folder_path = './'  # Adjust to the directory where the files are stored

# Step 2: Initialize a list to store latte prices data
worldwide_latte_prices = []

# Step 3: Loop through files in the folder
for file_name in os.listdir(folder_path):
    # Check if the file matches the pattern "starbucks_prices_[country].csv"
    if file_name.startswith('starbucks_prices_') and file_name.endswith('.csv'):
        # Extract the country name from the file name
        country_name = file_name.replace('starbucks_prices_', '').replace('.csv', '').capitalize()
        
        # Load the CSV file into a DataFrame
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)
        
        # Step 4: Search for a row containing 'Latte'
        for _, row in df.iterrows():
            if 'latte' in row['Item'].lower():  # Case-insensitive search for "latte"
                latte_price = row['Price']
                # Append the country name and latte price to the list
                worldwide_latte_prices.append({'Country': country_name, 'Latte Price': latte_price})
                break  # Stop after finding the first matching "latte"

# Step 5: Save the consolidated data to a new CSV file
output_file = 'worldwide_latte_prices.csv'
df_worldwide = pd.DataFrame(worldwide_latte_prices)
df_worldwide.to_csv(output_file, index=False)

print(f"Worldwide latte prices saved to {output_file}")
print(df_worldwide)
import pycountry

# Step 1: Load Data
file_path = "worldwide_latte_prices.csv"  # Change this to your actual file name
df = pd.read_csv(file_path)

# Step 2: Function to Standardize Country Names
def standardize_country_name(country):
    try:
        # Convert country name to lowercase and remove leading/trailing spaces
        country = country.strip().lower()
        
        # Handle common non-standard names manually
        country_corrections = {
            "czech-republic": "Czech Republic",
            "south-africa": "South Africa",
            "united-states": "United States",
            "united-kingdom": "United Kingdom",
            "méxico": "Mexico",
            "brasil": "Brazil",
            "italy": "Italy",
            "hungary": "Hungary",
            "finland": "Finland",
            "colombia": "Colombia",
            "canada": "Canada",
            "poland": "Poland",
            "australia": "Australia",
            "chile": "Chile"
        }

        # Check for manual corrections first
        if country in country_corrections:
            return country_corrections[country]

        # Use pycountry to get standard country names
        country_obj = pycountry.countries.lookup(country)
        return country_obj.name  # Return the official English name

    except LookupError:
        return country  # If no match is found, return the original name
# Step 3: Apply the function to the "Country" column
df["Country"] = df["Country"].apply(standardize_country_name)

# Step 4: Remove Duplicates (if any)
df = df.drop_duplicates()

# Step 5: Save the cleaned file
output_file = "latte_prices_standardized.csv"
df.to_csv(output_file, index=False)

print(f"✅ Standardized country names saved to {output_file}")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Load country data
csv_file = 'latte_prices_standardized.csv'
countries = pd.read_csv(csv_file)

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed

# Country to currency mapping
country_to_currency = {
    "Brazil": "BRL",
    "Canada": "CAD",
    "United Kingdom": "GBP",
    "Japan": "JPY",
    "Mexico": "MXN",
    "India": "INR"
}

# Function to get exchange rate from DuckDuckGo
def get_exchange_rate_from_duckduckgo(country_name):
    try:
        # Convert country name to currency code if available
        currency_code = country_to_currency.get(country_name, country_name)

        # Open DuckDuckGo
        driver.get("https://duckduckgo.com/")

        # Locate and enter search query in search box
        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(f"1 USD to {currency_code} exchange rate")
        search_box.send_keys(Keys.RETURN)

        # Wait for results to load
        try:
            rate_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'1 USD =')]"))
            )
            exchange_rate = rate_element.text.split('=')[1].strip()
            return exchange_rate
        except:
            print(f"No exchange rate found for {country_name}")
            return None

    except Exception as e:
        print(f"Error fetching exchange rate for {country_name}: {e}")
        return None

# Loop through each country and fetch exchange rates
exchange_rates = []
for _, row in countries.iterrows():
    country_name = row['Country']
    print(f"Fetching exchange rate for {country_name}...")
    rate = get_exchange_rate_from_duckduckgo(country_name)
    exchange_rates.append({'Country': country_name, 'Exchange Rate': rate})

# Save results to CSV
df_exchange_rates = pd.DataFrame(exchange_rates)
output_file = 'exchange_rates_duckduckgo.csv'
df_exchange_rates.to_csv(output_file, index=False)
print(f"Exchange rates saved to {output_file}")

# Close Selenium WebDriver
driver.quit()
