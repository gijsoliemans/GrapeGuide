#import basic packages
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# Construct the absolute path to the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'WineDataset.json')

# Read the JSON file into a DataFrame
df = pd.read_json(json_file_path)

# Convert the DataFrame to a list of dictionaries
wines = df.to_dict(orient='records')

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
    
@app.route('/wines')
def wines_page():
    return render_template('wines.html', data=wines)

@app.route('/wine/<Title>')
def wine_detail(Title):
    wine = next((wine for wine in wines if wine['Title'] == Title), None)
    if wine is None:
        return "Wine not found", 404
    return render_template('wine_detail.html', wine=wine)

if __name__ == "__main__":
    app.run(debug=True)