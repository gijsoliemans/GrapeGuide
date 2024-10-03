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

# Function to extract unique values out the json for the filters on wines.html
def get_unique_values(data, key):
    return sorted(set([wine.get(key) for wine in data if wine.get(key)]))

@app.route('/wines', methods=['GET'], endpoint='wines')
def wine_list():
    # GET filters
    filters = {
        'Country': request.args.get('country'),
        'Region': request.args.get('region'),
        'Grape': request.args.get('grape'),
        'Type': request.args.get('type'),
        'Style': request.args.get('style'),
        'Vintage': request.args.get('vintage'),
        'Closure': request.args.get('closure'),
        'Capacity': request.args.get('capacity'),
        'Secondary Grape Varieties': request.args.get('secondary_grape_varieties'),
        'Unit': request.args.get('unit'),
        'Characteristics': request.args.get('characteristics'),
        'Per bottle/case/each': request.args.get('per_bottle_case_each'),
        'Appellation': request.args.get('appellation')
    }

    # Get unique filter options using get_unique_values function
    unique_countries = get_unique_values(wines, 'Country')
    unique_regions = get_unique_values(wines, 'Region')
    unique_grapes = get_unique_values(wines, 'Grape')
    unique_types = get_unique_values(wines, 'Type')
    unique_styles = get_unique_values(wines, 'Style')
    unique_vintages = get_unique_values(wines, 'Vintage')
    unique_closures = get_unique_values(wines, 'Closure')
    unique_capacities = get_unique_values(wines, 'Capacity')
    unique_secondary_grapes = get_unique_values(wines, 'Secondary Grape Varieties')
    unique_units = get_unique_values(wines, 'Unit')
    unique_characteristics = get_unique_values(wines, 'Characteristics')
    unique_per_bottle_case_each = get_unique_values(wines, 'Per bottle / case / each')
    unique_appellations = get_unique_values(wines, 'Appellations')

    # Additional filters with slidebars
    price_min = request.args.get('price_min', 0, type=float)
    price_max = request.args.get('price_max', 1000, type=float)
    abv_min = request.args.get('abv_min', 0, type=float)
    abv_max = request.args.get('abv_max', 100, type=float)

    # Filter the wines dynamically
    filtered_wines = wines
    for key, value in filters.items(): # Key for example country, grape. Value for example France, Chardonnay.
        if value:
            filtered_wines = [wine for wine in filtered_wines if str(wine.get(key)) == value]

    # Apply slidebar filters (price, ABV)
    filtered_wines = [wine for wine in filtered_wines if price_min <= wine.get('Price') <= price_max]
    filtered_wines = [wine for wine in filtered_wines if abv_min <= wine.get('ABV') <= abv_max]

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of wines to display per page
    total_wines = len(filtered_wines)
    total_pages = math.ceil(total_wines / per_page)

    # Get the wines for the current page
    start = (page - 1) * per_page
    end = start + per_page
    wines_to_display = filtered_wines[start:end]

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

    # Pass the data to the template, including unique filters
    return render_template(
        'wines.html',
        filters=filters,
        data=wines_to_display,
        page_numbers=page_numbers,
        unique_countries=unique_countries,
        unique_regions=unique_regions,
        unique_grapes=unique_grapes,
        unique_types=unique_types,
        unique_styles=unique_styles,
        unique_vintages=unique_vintages,
        unique_closures=unique_closures,
        unique_capacities=unique_capacities,
        unique_secondary_grapes=unique_secondary_grapes,
        unique_units=unique_units,
        unique_characteristics=unique_characteristics,
        unique_per_bottle_case_each=unique_per_bottle_case_each,
        unique_appellations=unique_appellations
    )

@app.route('/wine/<int:wine_id>')
def wine_detail(wine_id):
    # Logic to fetch the wine detail from wines based on wine_id
    wine = wines[wine_id]  # This assumes wine_id corresponds to the index
    return render_template('wine_detail.html', wine=wine)

if __name__ == "__main__":
    app.run(debug=True)