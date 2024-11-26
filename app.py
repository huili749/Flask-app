import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

app.secret_key = '071ca08c98ef594f297a4304808d9c453893cd7459f6295a4d3a111ed66baa3b'

# Routes
@app.route('/')
def index():
    """Home page with buttons for Generate and Library."""
    print("Home route is being accessed!") 
    return render_template('index.html')

@app.route('/home')
def home():
    """Home page with buttons for Generate and Library."""
    return render_template('home.html')

@app.route('/generate')
def generate():
    """Home page with buttons for Generate and Library."""
    return "This is the Generate page!"

@app.route('/explore')
def explore():
    """Home page with buttons for Generate and Library."""
    return render_template('explore.html')

@app.route('/library')
def library():
    """Home page with buttons for Generate and Library."""
    return render_template('library.html')

@app.route('/create')
def create():
    """Home page with buttons for Generate and Library."""
    return render_template('create.html')

@app.route('/login')
def login():
    """Home page with buttons for Generate and Library."""
    return render_template('login.html')

@app.route('/signup')
def signup():
    """Home page with buttons for Generate and Library."""
    return render_template('signup.html')

@app.route('/logout')
def logout():
    """Home page with buttons for Generate and Library."""
    return render_template('logout.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
