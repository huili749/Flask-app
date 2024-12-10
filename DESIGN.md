/*Overview*/
    This project is a web application designed for managing and visualizing categories and palettes. The primary functionality includes creating, editing, and deleting categories, as well as saving palettes under categories. The application is built using Flask, a lightweight Python web framework, and relies on SQLite for the backend database. The front-end employs HTML, CSS, and JavaScript to deliver an interactive and user-friendly experience.
    
    This document provides a technical overview of the project's architecture, implementation details, and design decisions.

/*Architecture*/
    The application is built with the following key components:
        Back-End (Flask)
            Implements routes for managing categories and palettes.
            Provides APIs for saving, editing, and deleting data.
            Uses SQLite as the database to store users, categories, and palettes.
        Front-End
            Combines HTML templates, CSS, and JavaScript.
            Uses the Jinja2 templating engine for dynamically generating HTML content.
            Incorporates modular JavaScript files to handle interactivity and API requests.
        Database (SQLite)
            Contains three main tables:
            users: For authentication and user data.
            categories: To store category metadata.
            palettes: To store palette information (linked to categories).

/*Key Features and Design Decisions*/
    1. User Authentication
        Utilizes Flask-Login for managing user sessions.
        The users table stores hashed passwords for security.
        Authentication ensures that each user has their own categories and palettes, maintaining data isolation and privacy.
    2. Dynamic Category Management
        Categories are displayed dynamically on the Library page.
        Editing and deleting categories is handled via modals and API requests.
        Using modals allows for a seamless user experience without needing page reloads.
        The "Edit Category" functionality supports renaming and deleting categories, improving user control over their data.
    3. Palette Management
        Palettes are associated with categories through a foreign key relationship.
        Saving palettes involves AJAX requests to send palette data to the server.
        Storing palettes in a dedicated table allows for better scalability as users add more data.
        Using JSON payloads for palette data simplifies handling and transferring data between the front-end and back-end.
    4. Palette Generation
        Users can upload an image on the Generate page to generate a palette. The server processes the image to extract dominant colors, which are displayed dynamically on the page.
        The extracted palette can be previewed, saved to a category, or downloaded as an image.
        The use of image processing allows users to generate unique color palettes quickly.
        Dynamically displaying the palette encourages immediate interaction, such as saving or editing the palette.
    5.  Modular Front-End Design
        JavaScript is split into modular files (e.g., library.js, generate.js, category_edit.js).
        Each file corresponds to specific functionalities (e.g., managing the library or handling palette generation).
        Keeping JavaScript modular improves maintainability and avoids potential conflicts between scripts.
    6.  Interactive Background with Dot Grid
        The number of dots, their spacing, and responsiveness to mouse movement are adjustable, allowing flexibility in aesthetic design.
        Enhances static pages like the homepage and login screen with subtle, interactive animations for improved user experience.
    7. Responsive Layout
        CSS Grid and Flexbox are used for layout design, ensuring the application is responsive across different screen sizes.
        Responsiveness is crucial for usability on both desktop and mobile devices.
    8. Database Schema
        The database schema includes the following tables:
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );

            CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE TABLE palettes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            );
        Decision:
            Normalizing the database ensures efficient storage and avoids redundant data.

/*Challenges and Solutions*/
    1. Database Relationships
        Challenge: Handling the cascading deletion of palettes when a category is deleted.
        Solution: Added ON DELETE CASCADE constraints in the database schema and validated in the application logic.
    2. Dynamic UI Updates
        Challenge: Updating the front-end dynamically after actions like saving or deleting without reloading the page.
        Solution: Implemented AJAX requests and JavaScript DOM manipulation to make real-time updates.
    3. Error Handling
        Challenge: Preventing duplicate categories and handling user input errors.
        Solution: Added server-side validation for unique category names and user-friendly error messages.

/*Future Improvements*/
    1. Enhanced Customization During Generation:
        Allow users to specify more advanced options during palette generation, such as:
            Hue: Users can choose a specific color range or theme (e.g., warm, cool, or monochromatic palettes).
            Temperature: Implement color temperature adjustments to generate palettes with warmer or cooler tones.
            Contrast and Saturation: Add sliders for fine-tuning the vibrancy and balance of the generated colors.
        A user-friendly UI with sliders, dropdowns, or presets for easy selection of these parameters.
        Offers greater creative control for users, catering to diverse design needs.
    2. Pagination: Implement pagination for the Library page to handle a large number of categories or palettes efficiently.
    3. Advanced Search: Add a search bar to filter palettes and categories dynamically.
    4. Palette Editing: Extend functionality to allow editing colors within saved palettes.
    5. API Documentation: Create comprehensive documentation for the API endpoints using tools like Swagger.
    6. Expanded Extraction Capabilities:
        Integrate machine learning models (e.g., TensorFlow.js or OpenCV.js) to detect and extract key objects from uploaded images.
        After identifying primary objects, query a design database or API (e.g., Google Lens, Pinterest, or custom datasets) to find items or elements with similar styles, materials, or aesthetics, enables to save to library.
        Elevates the platform from a palette generator to a full-fledged design tool for professionals.
