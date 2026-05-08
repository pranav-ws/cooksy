# Cooksy

#### Cooksy: https://pranav-ws.github.io/cooksy/
alt link: https://cooksy-c0c0.onrender.com

#### Description:
The idea for Cooksy was born out of a universal, everyday frustration: staring into a refrigerator full of mismatched ingredients and having no idea what to cook. Traditional recipe websites require users to figure out what they want to eat first, often leading to a frustrating realization that they are missing key components. Cooksy flips this paradigm entirely. It operates as a "reverse recipe engine," allowing users to input the ingredients they already have on hand and instantly generating a curated list of meals they can prepare right now. Not only does this solve the daily dilemma of "what's for dinner," but it also actively encourages users to reduce their food waste and save money.

Cooksy is a full-stack web application built using Python and the Flask framework for the backend, SQLite for the relational database, and HTML, CSS, JavaScript, and Bootstrap 5 for the frontend user interface.

At its core, the application relies on seamless integration with the Spoonacular REST API. When a user submits a list of ingredients via the homepage form, the Flask backend captures this data and constructs a dynamic HTTP GET request using Python's requests library. This query is sent to Spoonacular's findByIngredients endpoint, which returns a comprehensive JSON payload. The backend then parses this JSON, extracting vital information such as the recipe ID, title, and high-resolution image URLs, and passes this data to the frontend using Jinja templating.

To ensure user privacy and personalized experiences, Cooksy features a robust authentication system adapted from the CS50 framework. Users can securely register for an account, with their passwords hashed via werkzeug.security before being stored in the database. Session management ensures that users remain logged in across different pages and protects specific routes (like the search and favorites pages) from being accessed by unauthorized visitors using a custom @login_required decorator.

The project is structured into several key files and directories, each handling a specific layer of the application's logic:

app.py: This serves as the central nervous system of the application. It handles all backend routing, manages the user session, executes database queries via the CS50 SQL library, and manages the external API calls. Crucially, the Spoonacular API key is secured using environment variables and the python-dotenv library, ensuring that sensitive credentials are never hardcoded into the source code.

pantry.db: The SQLite database consists of two primary tables. The users table stores user credentials, while the favorites table acts as a relational ledger, linking specific user_ids to the recipe_id, title, and image_url of the meals they have chosen to save.

helpers.py: This file contains utility functions, primarily the apology function to render user-friendly error pages, and the login_required wrapper to secure routes.

templates/: This directory contains the HTML files, which utilize Jinja syntax for dynamic rendering.

layout.html acts as the master template, containing the navigation bar, Bootstrap CDN links, and the JavaScript required for the persistent Dark Mode.

index.html serves as the landing page, featuring a visually striking hero section with a semi-transparent dark overlay to ensure text readability, alongside a custom search bar.

results.html uses Jinja for loops to dynamically generate a responsive Bootstrap grid of recipe cards based on the API response. Each card includes a hidden HTML form that allows the user to save the recipe via a POST request.

favorites.html pulls data directly from the SQLite database to display the user's saved recipes, providing external links to view the full cooking instructions.

One of the most significant design decisions in this project was the implementation of the user interface. I utilized Bootstrap 5 to ensure the application is entirely mobile-responsive, automatically adapting the recipe card grids from a single column on phones to three columns on desktop monitors.

Furthermore, I implemented a custom, persistent Dark Mode toggle to elevate the user experience. Rather than storing the user's theme preference in the backend database—which would require a server request and cause a brief "flash" of bright light upon page load—I opted to handle the theme state entirely on the client side using JavaScript and the browser's localStorage API. When the user clicks the theme toggle in the navigation bar, JavaScript dynamically swaps the data-bs-theme attribute on the root HTML element and updates the button's icon, instantly transitioning the site's color palette. Because this preference is saved to localStorage, the browser automatically checks and applies the correct theme the millisecond a new page loads, resulting in a buttery-smooth, native-feeling application.

Looking forward, future iterations of Cooksy could include advanced filtering options, allowing users to exclude specific allergens or specify dietary preferences (such as vegan or gluten-free) before pinging the API. Additionally, a feature to automatically generate a missing ingredients grocery list for saved recipes would further enhance the application's utility.

Building Cooksy was an incredibly rewarding challenge that brought together all the core concepts of CS50: memory management (via sessions), algorithms (parsing complex JSON arrays), data structures (relational database schemas), and web design. It successfully transforms raw data from the internet into a beautiful, highly functional tool that solves a real-world problem.
