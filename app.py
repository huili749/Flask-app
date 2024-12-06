import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from colorthief import ColorThief

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

app.secret_key = '071ca08c98ef594f297a4304808d9c453893cd7459f6295a4d3a111ed66baa3b'

# Upload directory settle down
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Check the filename extention
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    """Home page with buttons for Generate and Library."""
    print("Home route is being accessed!") 
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate page: upload image and extract the main color"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('File not found')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Get the number of colors from the form (default to 5)
            color_count = int(request.form.get('color-count', 5))

            # Extract the main color
            color_thief = ColorThief(filepath)
            palette = color_thief.get_palette(color_count=color_count)
            hex_colors = ['#{:02x}{:02x}{:02x}'.format(*color) for color in palette]

            # Render the template with the image and color palette
            response = render_template('generate.html', colors=hex_colors, filename=filename)
            
            return response

    return render_template('generate.html')

@app.route('/library')
def library():
    """Home page with buttons for Generate and Library."""
    return render_template('library.html')

@app.route('/history')
def create():
    """Home page with buttons for Generate and Library."""
    return render_template('history.html')

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
