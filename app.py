import os
import time
import json

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, url_for, request, session, g, jsonify, abort
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from colorthief import ColorThief

from helpers import login_required, save_palette_image

# Configure application
app = Flask(__name__)

app.secret_key = '071ca08c98ef594f297a4304808d9c453893cd7459f6295a4d3a111ed66baa3b'

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Upload directory settle down
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configure the database connection
db = SQL("sqlite:///library.db")

# Check the filename extention
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    """Home page with buttons to start journey."""
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

            categories = db.execute("SELECT name FROM categories")

            # Render the template with the image and color palette
            response = render_template('generate.html', colors=hex_colors, filename=filename, categories=categories)
            
            return response
    categories = db.execute("SELECT name FROM categories")
    return render_template('generate.html', categories=categories)

@app.route('/save_palette', methods=['POST'])
@login_required
def save_palette():
    """Generate palette image, save it, and link it to a category."""
    # Retrieve form data
    category_name = request.form.get('category')
    new_category_name = request.form.get('new_category', "").strip()
    colors_raw = request.form.get('colors')

    # Validate colors
    if not colors_raw:
        flash("No colors provided!")
        return redirect(url_for('generate'))
    
    try:
        colors = json.loads(colors_raw)
        print(f"Parsed Colors: {colors}")
    except json.JSONDecodeError:
        print("Error: Invalid colors format!")
        flash("Invalid colors format!")
        return redirect(url_for('generate'))

    # Handle category: create or retrieve ID
    if new_category_name:
        # Check if the category exists
        existing_category = db.execute("SELECT id FROM categories WHERE name = ?", new_category_name)
        if not existing_category:
            # Try to insert a new category
            try:
                db.execute("INSERT INTO categories (name) VALUES (?)", new_category_name)
                db.commit()  # Ensure the submission
                print(f"Inserted new category: {new_category_name}")
            except Exception as e:
                print(f"Error inserting new category: {e}")
            # Fetch the ID for the new item
            category = db.execute("SELECT id FROM categories WHERE name = ?", new_category_name)
            if category:
                category_id = category[0]["id"]
                print(f"New category ID: {category_id}")
            else:
                print("Failed to retrieve newly inserted category.")
        else:
            # If exists
            category_id = existing_category[0]["id"]
            print(f"Using existing category: {new_category_name}")

    elif category_name:
        category = db.execute("SELECT id FROM categories WHERE name = ?", category_name)
        if not category:
            flash("Invalid category selected!")
            return redirect(url_for('generate'))
        category_id = category[0]["id"]
    else:
        flash("No category provided!")
        return redirect(url_for('generate'))

    # Generate palette image and save it
    palette_filename = f"palette_{int(time.time())}.png"
    palette_path = os.path.join(app.config['UPLOAD_FOLDER'], 'palettes', palette_filename)
    save_palette_image(colors, palette_path)

    # Save palette details in the database
    relative_path = os.path.join('uploads', 'palettes', palette_filename)  # Relative path for database
    db.execute(
        "INSERT INTO palettes (image_path, category_id, colors) VALUES (?, ?, ?)",
        relative_path,
        category_id,
        str(colors)
    )

    flash("Palette saved to library!")
    return redirect(url_for('library'))

@app.route('/library')
@login_required
def library():
    """Library page showing all categories."""
    sort_by = request.args.get('sort', 'name_asc')  # Default to A-Z sorting

    if sort_by == 'name_asc':
        order_by = "c.name ASC"
    elif sort_by == 'name_desc':
        order_by = "c.name DESC"
    elif sort_by == 'recent':
        order_by = "MAX(p.timestamp) DESC"
    else:
        order_by = "c.name ASC"  # Fallback to A-Z sorting

    categories = db.execute(f"""
        SELECT c.id, c.name, COUNT(p.id) AS palette_count,
               MAX(p.timestamp) AS latest_palette
        FROM categories c
        LEFT JOIN palettes p ON c.id = p.category_id
        GROUP BY c.id, c.name
        ORDER BY {order_by}
    """)

    for category in categories:
        category['palettes'] = db.execute("SELECT * FROM palettes WHERE category_id = ? LIMIT 4", category['id'])

    return render_template('library.html', categories=categories)

@app.route('/library/<category_name>')
@login_required
def category_page(category_name):
    """Display palettes for a specific category."""
    # Fetch the category details
    category = db.execute("SELECT * FROM categories WHERE name = ?", category_name)
    if not category:
        flash("Category not found!")
        return redirect(url_for('library'))

    category_id = category[0]["id"]

    # Fetch palettes for this category
    palettes = db.execute("SELECT * FROM palettes WHERE category_id = ?", category_id)

    return render_template('category.html', category_name=category_name, palettes=palettes)

@app.route('/save_category', methods=["POST"])
@login_required
def save_category():
    """Save a new category or link an existing one."""
    data = request.get_json()

    selected_category = data.get("category", "").strip()
    new_category = data.get("new_category", "").strip()

    if not selected_category and not new_category:
        return jsonify({"error": "No category provided!"}), 400

    if new_category:
        # Check if the category already exists
        existing = db.execute("SELECT * FROM categories WHERE name = ?", new_category)
        if existing:
            return jsonify({"error": "Category already exists!"}), 400
        # Create the new category
        db.execute("INSERT INTO categories (name) VALUES (?)", new_category)
        return jsonify({"message": f"New category '{new_category}' created!"}), 200

    return jsonify({"message": f"Category '{selected_category}' linked!"}), 200

@app.route('/update_category/<int:category_id>', methods=["POST"])
@login_required
def update_category(category_id):
    """Update the name of a category."""
    new_name = request.json.get("name", "").strip()
    if not new_name:
        return jsonify({"success": False, "error": "Name cannot be empty"}), 400

    # Check if the category exists
    category = db.execute("SELECT * FROM categories WHERE id = ?", category_id)
    if not category:
        return jsonify({"success": False, "error": "Category not found"}), 404

    # Update the category name
    db.execute("UPDATE categories SET name = ? WHERE id = ?", new_name, category_id)
    return jsonify({"success": True})

@app.route('/delete_category/<int:category_id>', methods=["DELETE"])
@login_required
def delete_category(category_id):
    """Delete a category and all its related palettes."""
    # Check if the category exists
    category = db.execute("SELECT * FROM categories WHERE id = ?", category_id)
    if not category:
        return jsonify({"error": "Category not found!"}), 404

    # Delete all palettes related to this category
    db.execute("DELETE FROM palettes WHERE category_id = ?", category_id)

    # Delete the category itself
    db.execute("DELETE FROM categories WHERE id = ?", category_id)

    return jsonify({"success": True, "message": "Category and related palettes deleted successfully!"}), 200

@app.route('/palette/<int:palette_id>')
@login_required
def get_palette(palette_id):
    """Fetch palette details by ID."""
    palette = db.execute("SELECT * FROM palettes WHERE id = ?", palette_id)
    if not palette:
        return {"error": "Palette not found"}, 404
    return {
        "id": palette[0]["id"],
        "image_path": url_for('static', filename=palette[0]["image_path"]),
        "colors": palette[0]["colors"]
    }

@app.route('/delete_palette/<int:palette_id>', methods=["DELETE"])
@login_required
def delete_palette(palette_id):
    """Delete a palette by ID."""
    palette = db.execute("SELECT * FROM palettes WHERE id = ?", palette_id)
    if not palette:
        return {"error": "Palette not found"}, 404

    # Remove the file from the filesystem
    palette_path = os.path.join('static', palette[0]['image_path'])
    if os.path.exists(palette_path):
        os.remove(palette_path)

    # Remove the palette from the database
    db.execute("DELETE FROM palettes WHERE id = ?", palette_id)
    return {"success": True}, 200

@app.before_request
def load_logged_in_user():
    g.username = session.get("user_name")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Fetch user data
        user = db.execute("SELECT * FROM users WHERE email = ?", email)
        if not user or not check_password_hash(user[0]['password'], password):
            flash("Invalid email or password!")
            return redirect(url_for('login'))

        # Set session data
        session["user_id"] = user[0]["id"]
        session["user_name"] = user[0]["name"]
        flash("Logged in successfully!")
        return redirect(url_for('library'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up a new user."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        existing_user = db.execute("SELECT * FROM users WHERE email = ?", email)
        if existing_user:
            flash("User with this email already exists!")
            return redirect(url_for('signup'))
        
        # Hash the password and save the user
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", name, email, hashed_password)

        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    """Log out the current user."""
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
    """Allow users to change their password."""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Fetch the current user's data
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Validate current password
        if not check_password_hash(user[0]['password'], current_password):
            flash("Current password is incorrect!")
            return redirect(url_for('change_password'))

        # Check if the new passwords match
        if new_password != confirm_password:
            flash("New passwords do not match!")
            return redirect(url_for('change_password'))

        # Update the password in the database
        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET password = ? WHERE id = ?", hashed_password, session["user_id"])

        flash("Password updated successfully!")
        return redirect(url_for('library'))

    return render_template('change_password.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)