import os
import requests
from cs50 import SQL
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology # Re-use these from Finance!

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pantry.db")

# Load the .env file first!
load_dotenv()

# Now safely get the key
API_KEY = os.environ.get("SPOONACULAR_API_KEY")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Main Search Page"""
    if request.method == "POST":
        # 1. Get ingredients from the HTML form
        ingredients = request.form.get("ingredients")
        
        # 2. Check if user actually typed something
        if not ingredients:
            return apology("Must provide ingredients", 400)
            
        # 3. Make the API request to Spoonacular 
        url = "https://api.spoonacular.com/recipes/findByIngredients"
        params = {
            "ingredients": ingredients, 
            "number": 9,               
            "apiKey": API_KEY
        }
        
        response = requests.get(url, params=params)
        
        # 4. Parse the JSON response 
        if response.status_code == 200:
            recipes = response.json()
            # 5. Pass the data to your results page
            return render_template("results.html", recipes=recipes)
        else:
            return apology("Could not fetch recipes", 500)
            
    else:
        # Just show the search bar
        return render_template("index.html")

@app.route("/save", methods=["POST"])
@login_required
def save_recipe():
    """Save a recipe to user's favorites"""
    if not session.get("user_id"):
        return redirect("/login")
    # 1. Get recipe ID, title, and image URL from the form submission
    recipe_id = request.form.get("recipe_id")
    title = request.form.get("title")
    image_url = request.form.get("image_url")
    # 2. INSERT into your favorites table linking it to session["user_id"]
    db.execute("INSERT INTO favorites (user_id, recipe_id, recipe_title, image_url) VALUES (?, ?, ?, ?)", session["user_id"], recipe_id, title, image_url)
    flash("Recipe Saved!")
    return redirect("/favorites")

@app.route("/favorites")
@login_required
def favorites():
    """Show saved recipes"""
    if not session.get("user_id"):
        return redirect("/login")
    # 1. Query the database for all recipes saved by session["user_id"]
    query = db.execute("SELECT * FROM favorites WHERE user_id = ?", session["user_id"])
    # 2. Pass that data to the template
    return render_template("favorites.html", recipes=query)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        # 1. Forget any user_id
        session.clear()

        # 2. Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # 3. Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # 4. Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # 5. Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # 6. Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # 7. Redirect user to home page
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # 1. Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # 2. Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # 3. Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # 4. Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # 5. Hash the password
        hash = generate_password_hash(request.form.get("password"))

        # 6. Attempt to insert the new user into the database
        try:
            new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)
        except:
            return apology("username already taken", 400)

        # 7. Remember which user has logged in
        session["user_id"] = new_user_id

        # 8. Redirect user to home page
        return redirect("/")
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)