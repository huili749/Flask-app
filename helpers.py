import os

from flask import session, redirect, url_for, flash
from functools import wraps
from PIL import Image, ImageDraw

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def save_palette_image(colors, path):
    """Generate a palette image and save it to the specified path."""
    # Image dimensions
    block_width = 200  # Width of each color block
    block_height = 200  # Height of the image
    image_width = block_width * len(colors)
    image_height = block_height

    # Create a new image
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    # Draw each color as a block
    for i, color in enumerate(colors):
        x0 = i * block_width
        x1 = x0 + block_width
        draw.rectangle([x0, 0, x1, block_height], fill=color)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save the image
    image.save(path)

