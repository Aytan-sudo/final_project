import os
import core_maze
import io
import base64

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

@login_required
def username():
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']
    return username

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """To define"""

    return render_template("index.html")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Managing Account"""
    # User reached route via POST (as by submitting a form via POST)

    if request.method == "POST":
        actual_password = request.form.get("actual_password")
        new_password = request.form.get("new_password")
        new_password_repeat = request.form.get("new_password_repeat")

        # Ensure username was submitted
        if not request.form.get("actual_password"):
            return apology("must provide actual password", 403)

        # Ensure password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide password", 403)

        # Ensure confirmation password was equal
        if new_password != new_password_repeat:
            return apology("retype your password", 400)

        # Extract the real password
        password_hash_in_db = db.execute("SELECT hash FROM users WHERE username IS ?", username())

        # Ensure actual password is correct
        if not check_password_hash(password_hash_in_db[0]['hash'], actual_password):
            return apology("wrong actual password", 400)

        # Fianlly update the password
        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(new_password),username())

    

    # User reached route via GET (as by clicking a link or via redirect or backward)
    else:
        return render_template("account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
        # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username_to_register = request.form.get("username")
        password_to_register = request.form.get("password")
        confirmation_password_to_register = request.form.get("confirmation")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation of password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Check database for username
        if db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
            return apology("username already exist", 400)

        #check confirmation password
        elif confirmation_password_to_register != request.form.get("password"):
            return apology("wrong password confirmation", 400)

        else:
            #insert username et hash(password) in the db
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username_to_register, generate_password_hash(password_to_register))
            return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect or backward)
    else:
        return render_template("register.html")


def encode_maze(col_value, lines_value, algo):
    """Maze encoding, function call by maze() in @app.route (/maze)"""

    maze = core_maze.Grid(col = int(col_value), lines = int(lines_value), algo= algo).create_png()
        
    img_io = io.BytesIO()
    maze.save(img_io, 'PNG')
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return img_base64  #encoding in text (base 64)


@app.route("/maze", methods=["GET", "POST"])
def maze():
    # default values for the first loading (i.e. GET)
    default_slider_value = 20
    default_algo = "ab"
    
    # For a POST request (i.e. by sliders or radio buttons)
    if request.method == "POST":
        col_value = request.form.get('colValue')
        lines_value = request.form.get('linesValue')
        algo = request.form.get('algo')

        img_base64 = encode_maze(col_value, lines_value, algo)
        return img_base64  #AJAX answer for a POST request

    # For a GET request, display the page with the default value
    img_base64 = encode_maze(col_value=default_slider_value, lines_value=default_slider_value, algo=default_algo)
    return render_template('maze.html', img_data=img_base64)


