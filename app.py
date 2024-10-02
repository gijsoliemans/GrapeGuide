#import basic packages
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import os
import math

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config['DEBUG'] = True  # Enable debug mode


# Construct the absolute path to the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'WineDataset.json')

# Read the JSON file into a DataFrame
df = pd.read_json(json_file_path)

# Convert the DataFrame to a list of dictionaries
wines = df.to_dict(orient='records')

# Add an index-based ID to each wine
for index, wine in enumerate(wines):
    wine['id'] = index  # Use lowercase 'id'

country_codes = {
    'USA': 'US',
    'France': 'FR',
    'Italy': 'IT',
    'Spain': 'ES',
    'Germany': 'DE',
    'Australia': 'AU',
    'Argentina': 'AR',
    'Chile': 'CL',
    'South Africa': 'ZA',
    'New Zealand': 'NZ',
    'Portugal': 'PT',
    'Austria': 'AT',
    'Hungary': 'HU',
    'Greece': 'GR',
    'Mexico': 'MX',
    'Israel': 'IL',
    'Brazil': 'BR',
    'Uruguay': 'UY',
    'Turkey': 'TR',
    'Croatia': 'HR',
    'Slovenia': 'SI',
    'Canada': 'CA',
    'Georgia': 'GE',
    'Lebanon': 'LB',
    'Romania': 'RO',
    'Serbia': 'RS',
    'Bulgaria': 'BG',
    'India': 'IN',
    'Taiwan': 'TW',
    'Japan': 'JP',
    'Vietnam': 'VN',
    'Moldova': 'MD',
    'Cyprus': 'CY',
    'Kazakhstan': 'KZ',
    'Tunisia': 'TN',
    'South Korea': 'KR',
    'Costa Rica': 'CR',
    'Thailand': 'TH',
    'Singapore': 'SG',
    'Belgium': 'BE',
    'Netherlands': 'NL',
    'Switzerland': 'CH',
    'Denmark': 'DK',
    'Norway': 'NO',
    'Finland': 'FI',
    'Iceland': 'IS',
    'Ireland': 'IE',
    'Scotland': 'GB', 
    'United Kingdom': 'GB',
    'England': 'GB',
    'Russia': 'RU',
    'Philippines': 'PH',
    'Egypt': 'EG',
    'Armenia': 'AM',
    'Kazakhstan': 'KZ',
    # Add more countries as needed
}


for wine in wines:
    wine['CountryCode'] = country_codes.get(wine['Country'], 'XX')


@app.route('/')
def home():
    return render_template('index.html')

# define the about page
@app.route('/about')
def about():
    return render_template('about.html')

# define the search page
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('search_results', search=search))
    else:
        return render_template('search.html')
    
@app.route('/wines', methods=['GET'], endpoint='wines')
def wine_list():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of wines to display per page
    total_wines = len(wines)
    total_pages = math.ceil(total_wines / per_page)

    # Get the wines for the current page
    start = (page - 1) * per_page
    end = start + per_page
    wines_to_display = wines[start:end]

    # Generate page numbers
    page_numbers = []
    if total_pages <= 5:  # Show all page numbers if there are 5 or fewer
        page_numbers = list(range(1, total_pages + 1))
    else:
        if page < 4:  # If we are on the first 3 pages
            page_numbers = list(range(1, 5)) + ['...'] + [total_pages]
        elif page > total_pages - 3:  # If we are on the last 3 pages
            page_numbers = [1] + ['...'] + list(range(total_pages - 3, total_pages + 1))
        else:  # If we are in the middle
            page_numbers = [1] + ['...'] + list(range(page - 1, page + 2)) + ['...'] + [total_pages]

    return render_template('wines.html', data=wines_to_display, page=page, total_pages=total_pages, page_numbers=page_numbers)


@app.route('/wine/<int:wine_id>')
def wine_detail(wine_id):
    # Logic to fetch the wine detail from wines based on wine_id
    wine = wines[wine_id]  # This assumes wine_id corresponds to the index
    return render_template('wine_detail.html', wine=wine)

if __name__ == "__main__":
    app.run(debug=True)