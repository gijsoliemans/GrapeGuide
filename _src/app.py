#import basic packages
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np



# create a basic flask app
app = Flask(__name__)

# define the home page
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
    
    

