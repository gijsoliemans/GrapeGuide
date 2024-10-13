#import basic packages
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import os
import math
import datetime

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config['DEBUG'] = True  # Enable debug mode

# Construct the absolute path to the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'WineDataset_with_Dishes_with_Images.json')

# Read the JSON file into a DataFrame
df = pd.read_json(json_file_path)

# Convert the DataFrame to a list of dictionaries
wines = df.to_dict(orient='records')

# Add an index-based ID to each wine
for index, wine in enumerate(wines):
    wine['id'] = index  # Use lowercase 'id'

# Function to extract unique values out the json for the filters on wines.html
def get_unique_values(data, key):
    return sorted(set([wine.get(key) for wine in data if wine.get(key)]))

@app.route('/')
def home():
    # Seed of the random 3 wines (based on datetime)
    np.random.seed(int(datetime.datetime.now().strftime('%Y%m%d')))
    # Randomly choose 3 wines from the dataset 
    random_wines = np.random.choice(wines, 3, replace=False)
    random_wines = [{'id': wine['id'], 'Title': wine['Title'], 'Image': wine['image_source'] } for wine in random_wines]
    print(random_wines)
    return render_template('index.html', random_wines=random_wines)

# define the about page
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/wines', methods=['GET'], endpoint='wines')
def wine_list():

    # GET filters
    sort = request.args.get('sort')
    search = request.args.get('search')
    lead = request.args.get('lead')
    this_page = request.args.get('page', 1, type=int)

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

    # Get unique filter options using the get_unique_values function
    unique_countries = get_unique_values(wines, 'Country')
    unique_regions = get_unique_values(wines, 'Region')
    unique_grapes = get_unique_values(wines, 'Grape')
    unique_types = get_unique_values(wines, 'Type')
    unique_styles = get_unique_values(wines, 'Style')
    unique_closures = get_unique_values(wines, 'Closure')
    unique_capacities = get_unique_values(wines, 'Capacity')
    unique_secondary_grapes = get_unique_values(wines, 'Secondary Grape Varieties')
    unique_vintages = get_unique_values(wines, 'Vintage')
    unique_units = get_unique_values(wines, 'Unit')
    unique_characteristics = get_unique_values(wines, 'Characteristics')
    unique_per_bottle_case_each = get_unique_values(wines, 'Per bottle / case / each')
    unique_appellations = get_unique_values(wines, 'Appellations')

    # Split styles for wines that have multiple styles separated by ' & '
    unique_styles = sorted({style.strip() for styles in unique_styles for style in styles.split(' & ')})

    # Remove vintages that contain double years (e.g., '2020/2021')
    unique_vintages = [year for year in unique_vintages if '/' not in year]

    # Split wine filters for wines with multiple filters separated by ', '
    unique_secondary_grapes = sorted({grape.strip() for varieties in unique_secondary_grapes for grape in varieties.split(', ')})
    unique_characteristics = sorted({characteristic.strip() for characteristics in unique_characteristics for characteristic in characteristics.split(', ')})

    # Additional filters (sliders that are nice to have for the future)
    price_min = request.args.get('price_min', 0, type=float)  # Minimum price filter
    price_max = request.args.get('price_max', 1000, type=float)  # Maximum price filter
    abv_min = request.args.get('abv_min', 0, type=float)  # Minimum ABV filter
    abv_max = request.args.get('abv_max', 100, type=float)  # Maximum ABV filter

    # Filter the wines based on selected filters
    filtered_wines = wines

    pairing_filter = request.args.get('pairing')  # Get the selected pairing from the query parameters

    if pairing_filter:  # If a pairing is selected
        filtered_wines = [
            wine for wine in wines 
            if pairing_filter in wine.get('best_pairing', [])
        ]

    for key, value in filters.items(): # Key for example country, grape. Value for example France, Chardonnay.
        if value:
            # Split the input value separated by ', '
            if key in ['Secondary Grape Varieties', 'Characteristics']:
                values = [v.strip() for v in value.split(',')]
                filtered_wines = [
                    wine for wine in filtered_wines
                    if any(v.strip() in str(wine.get(key)).split(', ') for v in values)
                ]
            elif key == 'Style':
                # Split the input value separated by ' & '
                values = [v.strip() for v in value.split(' & ')]
                filtered_wines = [
                    wine for wine in filtered_wines
                    if any(v.strip() in str(wine.get(key)).split(' & ') for v in values)
                ]
            else:
                # Standard filtering for single values
                filtered_wines = [
                    wine for wine in filtered_wines
                    if str(wine.get(key)).strip() == value
                ]

    # Apply slidebar filters (price, ABV)
    filtered_wines = [wine for wine in filtered_wines if price_min <= wine.get('Price') <= price_max]
    filtered_wines = [wine for wine in filtered_wines if abv_min <= wine.get('ABV') <= abv_max]

    # If search bar is not empty:
    if search:
        filtered_wines = [wine for wine in filtered_wines if search.lower() in wine.get('Title').lower() or search.lower() == wine.get('Country').lower() 
                          or search.lower() in wine.get('Style').lower() or search.lower() == wine.get('Characteristics').lower()
                          or search.lower() == wine.get('Region').lower() or search.lower() == wine.get('Grape').lower()
                          or search.lower() == wine.get('Type').lower() or search.lower() == wine.get('Closure').lower()] 

    # Now sort the wines
    if sort == 'ascending' or sort == 'descending':
        # Sort by Price
        filtered_wines.sort(key=lambda x: x['Price'], reverse=(sort == 'descending'))
    elif sort == 'a-z' or sort == 'z-a':
        # Sort by Name
        filtered_wines.sort(key=lambda x: x['Title'], reverse=(sort == 'z-a'))


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

    # Pass all the data needed to build the webpage
    return render_template(
        'wines.html',
        path=request.path,
        sort=sort,
        search=search,
        filters=filters,
        data=wines_to_display,
        page_numbers=page_numbers,
        this_page=this_page,
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
        unique_appellations=unique_appellations,
        lead=lead
    )

@app.route('/wine/<int:wine_id>')
def wine_detail(wine_id):
    # Logic to fetch the wine detail from wines based on wine_id
    wine = wines[wine_id]  # This assumes wine_id corresponds to the index
    return render_template('wine_detail.html', wine=wine)

@app.route('/guide')
def guide():
    unique_countries = get_unique_values(wines, 'Country')
    unique_regions = get_unique_values(wines, 'Region')
    unique_grapes = get_unique_values(wines, 'Grape')
    unique_types = get_unique_values(wines, 'Type')
    unique_styles = get_unique_values(wines, 'Style')
    unique_closures = get_unique_values(wines, 'Closure')
    unique_capacities = get_unique_values(wines, 'Capacity')
    unique_secondary_grapes = get_unique_values(wines, 'Secondary Grape Varieties')
    unique_vintages = get_unique_values(wines, 'Vintage')
    unique_units = get_unique_values(wines, 'Unit')
    unique_characteristics = get_unique_values(wines, 'Characteristics')
    unique_per_bottle_case_each = get_unique_values(wines, 'Per bottle / case / each')
    unique_appellations = get_unique_values(wines, 'Appellations')
    
    return render_template(
        'guide.html',
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

if __name__ == "__main__":
    app.run(debug=True)