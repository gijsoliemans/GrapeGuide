import pandas as pd
import os
import random
import string
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
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

def convert_to_list(text):
    if pd.isna(text):
        return None  
    items = [item.strip() for item in text.split(',')]
    return items if items else None  

# Special function to split Style based on the '&' separator
def convert_style_to_list(text):
    if pd.isna(text):
        return None  # Return None if the value is NaN
    items = [item.strip() for item in text.split('&')]
    return items if items else None 

# apply al cleaning funcitons to the DataFrame
df['Title'] = df['Title'].apply(clean_title)
df['Capacity'] = df['Capacity'].apply(clean_capacity)
df['Price'] = df['Price'].apply(clean_price)
df['ABV'] = df['ABV'].apply(clean_ABV)

df['Secondary Grape Varieties'] = df['Secondary Grape Varieties'].apply(convert_to_list)
df['Characteristics'] = df['Characteristics'].apply(convert_to_list)
df['Style'] = df['Style'].apply(convert_style_to_list)

# Create a column with country codes with the imported country codes
df['CountryCode'] = df['Country'].map(country_codes)

# create a CountVectorizer object
count_vectorizer = CountVectorizer(stop_words='english')

# fit and transform the data
count_data = count_vectorizer.fit_transform(df['Description'])

# create a LatentDirichletAllocation object
lda = LatentDirichletAllocation(n_components=5, random_state=0)

# fit the data
lda.fit(count_data)

# get the topics
def get_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names_out()
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topic = [words[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics.append(topic)
    return topics

# Example usage
topics = get_topics(lda, count_vectorizer, 10)

# Add the topics to the DataFrame
df['Topics'] = lda.transform(count_data).argmax(axis=1)
df['Topics'] = df['Topics'].apply(lambda x: topics[x])

# Construct the absolute path to save the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'WineDataset.json')

# Save the modified dataset with classification scores to a JSON file
df.to_json(json_file_path, orient='records', indent=4)

# Verify if the file is saved
if os.path.exists(json_file_path):
    print(f"File saved successfully at {json_file_path}")
else:
    print("Failed to save the file.")