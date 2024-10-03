import pandas as pd
import os
import random
import string
from src.country_codes import country_codes

# Construct the absolute path to the CSV file
file_path = os.path.join(os.path.dirname(__file__), 'WineDataset.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

df = df.dropna(subset=['Title', 'Description', 'Price','Capacity', 'Grape', 
                       'Closure','Country', 'Unit', 'Characteristics', 'Per bottle / case / each', 
                       'Type', 'ABV', 'Region', 'Style', 'Vintage'])

def clean_title(title):
    # split on the comma and take the first part
    return title.split(',')[0]

def clean_price(price):
    # remove the pound sign and remove "per bottle"
    return float(price.replace('£', '').replace(' per bottle', '').strip())

def clean_ABV(abv):
    # remove the ABV and the % sign
    return float(abv.replace('ABV ', '').replace('%', '').strip())

def add_id(row):
    # create a unique ID of 8 random characters
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# apply al cleaning funcitons to the DataFrame
df['Title'] = df['Title'].apply(clean_title)
df['Price'] = df['Price'].apply(clean_price)
df['ABV'] = df['ABV'].apply(clean_ABV)
df['ID'] = df.apply(add_id, axis=1)

# Create a column with country codes with the imported country codes
df['CountryCode'] = df['Country'].map(country_codes)

# Construct the absolute path to save the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'WineDataset.json')

# Save the modified dataset with classification scores to a JSON file
df.to_json(json_file_path, orient='records')

# Verify if the file is saved
if os.path.exists(json_file_path):
    print(f"File saved successfully at {json_file_path}")
else:
    print("Failed to save the file.")