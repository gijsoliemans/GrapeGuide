from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import os
import math
import datetime

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config['DEBUG'] = True  # Enable debug mode

json_file_path = os.path.join(os.path.dirname(__file__), 'WineDataset_Complete.json')

df = pd.read_json(json_file_path)

wines = df.to_dict(orient='records')

for index, wine in enumerate(wines):
    wine['id'] = index  

def get_unique_values(data, key):
    unique_values = set()  
    for wine in data:
        values = wine.get(key)
        if values:
            if isinstance(values, list):  
                unique_values.update(values)
            else:
                unique_values.add(values)  
    return sorted(unique_values)

@app.route('/')
def home():
    # Seed of the random 3 wines (based on datetime)
    np.random.seed(int(datetime.datetime.now().strftime('%Y%m%d')))
    random_wines = np.random.choice(wines, 3, replace=False)
    random_wines = [{'id': wine['id'], 'Title': wine['Title'], 'Image': wine['image_source'] } for wine in random_wines]
    print(random_wines)
    return render_template('index.html', random_wines=random_wines)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/wines', methods=['GET'], endpoint='wines')
def wine_list():
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
    unique_vintages = [year for year in unique_vintages if '/' not in year]
    unique_secondary_grapes = sorted({grape.strip() for varieties in unique_secondary_grapes for grape in varieties.split(', ')})
    unique_characteristics = sorted({characteristic.strip() for characteristics in unique_characteristics for characteristic in characteristics.split(', ')})

    price_min = request.args.get('price_min', 0, type=float)  
    price_max = request.args.get('price_max', 1000, type=float) 
    abv_min = request.args.get('abv_min', 0, type=float)  
    abv_max = request.args.get('abv_max', 100, type=float)  

    # Filter the wines based on selected filters
    filtered_wines = wines
    pairing_filter = request.args.get('pairing')  

    if pairing_filter:  
        filtered_wines = [wine for wine in wines if pairing_filter in wine.get('best_pairing', [])]

    for key, value in filters.items():  # Key for example country, grape. Value for example France, Chardonnay.
        if value:
            values = [v.strip() for v in value.split(',')]
            # If filtering on 'Secondary Grape Varieties' or 'Characteristics' or 'Style' (which are lists)
            if key in ['Secondary Grape Varieties', 'Characteristics', 'Style']:
                filtered_wines = [
                    wine for wine in filtered_wines
                    if any(v in (wine.get(key) if isinstance(wine.get(key), list) else [wine.get(key)]) for v in values)
                ]
            # For standard single-value fields like 'Country', 'Region', 'Grape', etc.
            else:
                filtered_wines = [
                    wine for wine in filtered_wines
                    if str(wine.get(key, '')).strip() == value  # Standard exact match for non-list fields
                ]

    # Apply filters (price, ABV)
    filtered_wines = [wine for wine in filtered_wines if price_min <= wine.get('Price') <= price_max]
    filtered_wines = [wine for wine in filtered_wines if abv_min <= wine.get('ABV') <= abv_max]

    # If search bar is not empty:
    if search:
        search_lower = search.lower()
        filtered_wines = [
            wine for wine in filtered_wines
            if search_lower in wine.get('Title', '').lower()
            or search_lower == wine.get('Country', '').lower()
            or search_lower == wine.get('Region', '').lower()
            or search_lower == wine.get('Grape', '').lower()
            or search_lower == wine.get('Type', '').lower()
            or search_lower == wine.get('Closure', '').lower()
            or any(search_lower in style.lower() for style in wine.get('Style', []))  
            or any(search_lower in char.lower() for char in wine.get('Characteristics', [])) 
            or any(search_lower in topic.lower() for topic in wine.get('Topics', []))
        ]

    # Now sort the wines
    if sort == 'ascending' or sort == 'descending':
        # Sort by Price
        filtered_wines.sort(key=lambda x: x['Price'], reverse=(sort == 'descending'))
    elif sort == 'a-z' or sort == 'z-a':
        # Sort by Name
        filtered_wines.sort(key=lambda x: x['Title'], reverse=(sort == 'z-a'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12 
    total_wines = len(filtered_wines)
    total_pages = math.ceil(total_wines / per_page)

    # Get the wines for the current page
    start = (page - 1) * per_page
    end = start + per_page
    wines_to_display = filtered_wines[start:end]

    # Generate page numbers
    page_numbers = []
    if total_pages <= 5:  
        page_numbers = list(range(1, total_pages + 1))
    else:
        if page < 4: 
            page_numbers = list(range(1, 5)) + ['...'] + [total_pages]
        elif page > total_pages - 3:  
            page_numbers = [1] + ['...'] + list(range(total_pages - 3, total_pages + 1))
        else:  
            page_numbers = [1] + ['...'] + list(range(page - 1, page + 2)) + ['...'] + [total_pages]

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
    wine = wines[wine_id]  
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