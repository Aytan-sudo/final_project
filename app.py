import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
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
db = SQL("sqlite:///finance.db")

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
    """Show portfolio of stocks"""
    data = db.execute("SELECT * FROM stocks WHERE username = ?", username())
    values = 0
    for i in data:
        i['name'] = lookup(i['symbol'])['name']
        i['price'] = lookup(i['symbol'])['price']
        values += (i['price'] * i['shares'])

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

    return render_template("index.html", data=data, cash=cash, values=values)

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
        if actual_password != check_password_hash(password_hash_in_db[0]['hash']):
            return apology("wrong actual password", 400)

        # Fianlly update the password
        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(new_password),username())


    #TODO Change cash ?
    

    # User reached route via GET (as by clicking a link or via redirect or backward)
    else:
        return render_template("account.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
        # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        #request data from buy.html
        symbol_to_buy = request.form.get("symbol")
        shares_to_buy = request.form.get("shares")

        #Ensure "symbol" exist and integrity of shares
        if lookup(symbol_to_buy) == None:
            return apology("Invalid Symbol", 400)

        if not shares_to_buy.isdigit():
            return apology("not a number", 400)

        #define variables of the buy
        symbol = lookup(symbol_to_buy)['symbol']
        shares = int(shares_to_buy)
        price = shares * lookup(symbol_to_buy)['price']

        #Check if enough money to buy

        test_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if test_cash:
            cash_available = test_cash[0]['cash']
        else:
            return apology("no user", 400)
        print(symbol, shares, price, cash_available)

        if cash_available < price:
            return apology("Not enough cash",400)

        # add in the transaction table
        db.execute("INSERT INTO transactions (username,type_transaction,date,symbol,shares,price) VALUES (?,?,?,?,?,?)",
        username(), "Buy", datetime.now(), symbol, shares, price)

        # update the cash of the user
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_available - price, session["user_id"])

        # update the stock of the user
        db.execute("INSERT INTO stocks (username, symbol, shares) VALUES (?, ?, ?) ON CONFLICT (username, symbol) DO UPDATE SET shares = shares + ?",
        username(), symbol, shares, shares)

        # return
        flash(f"Buyed {shares} {symbol} for {usd(price)} !")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect or backward)
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT * FROM transactions WHERE username = ?", username())
    return render_template("history.html", history=history)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        quote_to_lookup = request.form.get("symbol")

        if lookup(quote_to_lookup) == None:
            return apology("Don't exist", 400)

        result = (f"A share of {lookup(quote_to_lookup)['name']} ({lookup(quote_to_lookup)['symbol']}) cost {usd(lookup(quote_to_lookup)['price'])}")

        return render_template("quoted.html", result=result)

    # User reached route via GET (as by clicking a link or via redirect or backward)
    else:
        return render_template("quote.html")


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

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        #request data from sell.html
        symbol_to_sell = request.form.get("symbol")
        shares_to_sell = request.form.get("shares")

        #define shares available to sell
        shares_available = db.execute("SELECT shares FROM stocks WHERE username = ? AND symbol = ?", username(), symbol_to_sell)[0]['shares']

        if shares_available < int(shares_to_sell):
            return apology('Not enough stock !', 400)

        #defines variables
        symbol = lookup(symbol_to_sell)['symbol']
        shares = int(shares_to_sell)
        price = shares * lookup(symbol_to_sell)['price']
        cash_available = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']

        # add in the transaction table
        db.execute("INSERT INTO transactions (username,type_transaction,date,symbol,shares,price) VALUES (?,?,?,?,?,?)",
        username(), "Sell", datetime.now(), symbol, shares, price)

        # update the cash of the user
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash_available + price, session["user_id"])

        # update the stock of the user
        db.execute("INSERT INTO stocks (username, symbol, shares) VALUES (?, ?, ?) ON CONFLICT (username, symbol) DO UPDATE SET shares = shares - ?",
        username(), symbol, shares, shares)

        # return
        flash(f"Sold {shares} {symbol} for {usd(price)} !")
        return redirect("/")


        # User reached route via GET (as by clicking a link or via redirect or backward)
    else:
        #Check symbol available and list them as options
        symbol_available = db.execute("SELECT symbol FROM stocks WHERE username = ?",username())

        return render_template("sell.html", symbol_available=symbol_available)
