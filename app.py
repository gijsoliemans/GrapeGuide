#import basic packages
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import os
from data.data import wines  

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

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

@app.route('/wine/<name>')
def wine_detail(name):
    wine = next((wine for wine in wines if wine['name'] == name), None)
    if wine is None:
        return "Wine not found", 404
    return render_template('wine_detail.html', wine=wine)

if __name__ == "__main__":
    app.run(debug=True)

    