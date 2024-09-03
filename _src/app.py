#import basic packages
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))

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
def wines():
    # Example product data
    product = {
        'name': 'Chateau Margaux',
        'year': 2015,
        'description': 'A full-bodied red wine with rich flavors of blackberry and plum.',
        'price': '$250',
        'image_url': 'https://example.com/chateau_margaux.jpg'
    }
    return render_template('wines.html', product=product)

if __name__ == "__main__":
    app.run(debug=True)