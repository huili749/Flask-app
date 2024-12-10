The entire file is linked here: https://drive.google.com/drive/folders/1IIyCo3ZQphGMxFMKFUjzGm1uDsYNLvcc?usp=sharing

/*Color Palette Manager*/

https://www.youtube.com/watch?v=IToYRdqUCoI

Color Palette Manager is a web application designed to help users generate and manage a personal library of color palettes. It offers features for creating color palettes, saving them into customizable categories, and downloading palettes for use. Users can edit the colors of generated palettes and manage their library by renaming categories, deleting categories, or removing individual palettes. The application is built with Python (Flask) on the backend and HTML, CSS, and JavaScript for the frontend.

/*Table of Contents*/
    1. Features
    2. System Requirements
    3. Installation
    4. Configuration
    5. Usage
        --Generating Palettes
        --Managing Categories
    6. Project Structure
    7. Notes
    8. Contact

/*Features*/
    Generate color palettes from uploaded images.
    Save palettes to customizable categories.
    Color palette adjustment customly and download.
    Organize categories and palettes with a clean, responsive UI.
    User authentication for secure access.

/*System Requirements*/
    Python 3.10 or higher
    SQLite 3
    Flask 2.x
    Compatible browser (e.g., Chrome, Firefox)

/*Installation*/
    1. Unzip the Project
        Download and unzip the project ZIP file.
        Open the folder in VS Code:
            code <path_to_unzipped_folder>
    2. Set Up a Virtual Environment
        Open the integrated terminal in VS Code (Ctrl + ~ or View > Terminal).
        Run the following commands:
            python -m venv venv
        Activate the virtual environment:
            source venv/bin/activate # For Linux/macOS
            venv\Scripts\activate # For Windows
        You should now see (venv) at the beginning of the terminal prompt.

    3. Install Dependencies
        With the virtual environment active, run:
            pip install -r requirements.txt
    4. Initialize the Database
        Ensure the library.db file is removed if you need to reinitialize the database:
            rm library.db  # For Linux/macOS
            del library.db  # For Windows
        Run the following commands in the VS Code terminal:
            flask shell
            >>> from app import db
            >>> db.create_all()
            >>> exit()

/*Configuration*/
    1. Environment Variables:
        In the root folder of your project, create a .env file with the following contents:
            FLASK_APP=app.py
            FLASK_ENV=development
            SECRET_KEY=your_secret_key_here
        This ensures Flask runs in development mode with proper configuration.
    2. Run the Application:
        In the terminal, start the Flask development server:
            flask run
        Open a browser and navigate to http://127.0.0.1:5000 to use the application.

/*Notes*/
    1. Ensure VS Code uses the Python interpreter from the venv environment
    2. Database Schema:
        users: Stores user login credentials.
        categories: Contains category metadata.
        palettes: Links palettes to their categories and stores image paths.
    3. Verify that the static/uploads/ directory exists for saving images. If it doesn’t, create it manually:
        mkdir static/uploads
    4. Error Handling: The application provides feedback for common errors, such as duplicate categories or invalid inputs.

/*Contact*/
    If you encounter issues or have questions, feel free to reach out to:
        Name: Hui Li
        Email: hui_li@gsd.harvard.edu