import pandas as pd
import os
import random
import string
import re
from src.country_codes import country_codes

# Construct the absolute path to the CSV file
file_path = os.path.join(os.path.dirname(__file__), 'WineDataset.csv')

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

df = df.dropna(subset=['Title', 'Description', 'Price','Capacity', 'Grape', 
                       'Closure','Country', 'Unit', 'Characteristics',
                       'Type', 'ABV', 'Region', 'Style', 'Vintage'])

df = df.drop(columns=['Per bottle / case / each'])

def clean_title(title):
    pattern = re.compile(r'\d{4}')
    split_text = pattern.split(title, 1)
    return split_text[0] 

def clean_price(price):
    # remove the pound sign and remove "per bottle"
    clean_price_gbp = float(price.replace('£', '').replace(' per bottle', '').strip())
    return clean_price_gbp

def clean_capacity(capacity):
    if 'CL' in capacity:
        return float(capacity.replace('CL', ''))
    elif 'ML' in capacity:
        return float(capacity.replace('ML', '')) / 10
    elif 'LTR' in capacity:
        return float(capacity.replace('LTR', '')) * 100

def clean_ABV(abv):
    # remove the ABV and the % sign
    return float(abv.replace('ABV ', '').replace('%', '').strip())

def clean_vintage(year: str) -> int:
    if len(year) < 4:
        return np.nan
    if len(year) > 4:
        return int(year.split('/')[0])
    else:
        return int(year)

def add_id(row):
    # create a unique ID of 8 random characters
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# apply al cleaning funcitons to the DataFrame
df['Title'] = df['Title'].apply(clean_title)
df['Capacity'] = df['Capacity'].apply(clean_capacity)
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