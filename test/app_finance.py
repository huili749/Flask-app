import os

from cs50 import SQL
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

    # Get the user's ID from the session
    user_id = session["user_id"]

    # Query for the user's stock holdings
    holdings = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    # Query for the user's current cash balance
    cash_query = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    if len(cash_query) == 0:
        return apology("User not found", 404)
    user_cash = cash_query[0]["cash"]

    # Prepare a list to store portfolio information
    portfolio = []
    total_stocks_value = 0

    # Loop through each stock in holdings
    for stock in holdings:
        # Use lookup to get the current price of the stock
        stock_data = lookup(stock["symbol"])
        if not stock_data:
            return apology("Invalid stock symbol")

        # Calculate the total value of the holding
        total_value = stock["total_shares"] * stock_data["price"]
        total_stocks_value += total_value

        # Append the stock's details to the portfolio
        portfolio.append({
            "symbol": stock["symbol"],
            "name": stock_data["name"],
            "shares": stock["total_shares"],
            "price": usd(stock_data["price"]),
            "total": usd(total_value)
        })

    # Calculate the grand total (cash + stocks' value)
    grand_total = total_stocks_value + user_cash

    # Render the index.html template with portfolio and cash information
    return render_template("index.html", portfolio=portfolio, cash=usd(user_cash), total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Get form data
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Vlidate symbol
        if not symbol:
            return apology("Missing symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid stock symbol", 400)

        # Validate shares
        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("shares must be a positive integer", 400)

        # Get user's current cash
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        # Calculate total price
        total_price = stock["price"] * shares

        # Check if user can afford the shares
        if user_cash < total_price:
            return apology("cannot afford", 400)

        # Update user's cash and record the transaction
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_price, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?, datetime('now'))",
            user_id, stock["symbol"], shares, stock["price"], "buy"
        )

        # Redirect to home
        return redirect("/")

    # Render the buy form
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get the user's ID from the session
    user_id = session["user_id"]

    # Query all transactions for the user
    transactions = db.execute("""
        SELECT symbol, shares, price, transaction_type, timestamp
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, user_id)

    # Render the history.html template
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "POST":
        # Get the stock symble from the form
        symbol = request.form.get("symbol")

        # Validate input
        if not symbol:
            return apology("Invalid symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("invalid stock symbol", 400)

        # Format the stock price using usd
        stock["price"] = usd(stock["price"])

        # Render the quoted.html template with stock data
        return render_template("quoted.html", stock=stock)

    # Render the quote.html template for GET requests
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get user inputs from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Insert the user into the database
        try:
            hash_password = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password)
        except ValueError:
            return apology("Username already exists", 400)

        # Validate form input
        if not username:
            return apology("Username cannot be blank", 400)
        if not password:
            return apology("Password cannot be blank", 400)
        if password != confirmation:
            return apology("Passwords do not match", 400)

        # Redirect to login or another page after successful registration
        flash("Registered successfully!")
        return redirect("/login")

    else:
        # Render the registration form
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Get the stock symbol and shares from the form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate symbol
        if not symbol:
            return apology("Missing stock", 400)

        # Validate shares
        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("shares must be a positive integer", 400)

        # Query user's holdings for the selected stock
        user_id = session["user_id"]
        holdings = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", user_id, symbol)

        if not holdings or holdings[0]["total_shares"] < shares:
            return apology("not enough shares", 400)

        # Get current stock price
        stock = lookup(symbol)
        if not stock:
            return apology("invalid stock symbol", 400)

        # Calculate the sale value
        sale_value = shares * stock["price"]

        # Update transactions table (negative shares indicate a sale)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?, datetime('now'))",
            user_id, symbol, -shares, stock["price"], "sell"
        )

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, user_id)

        # Redirect to home
        return redirect("/")

    else:
        # Query the user's owned stocks for the dropdown menu
        user_id = session["user_id"]
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)

        # Render the sell form
        return render_template("sell.html", stocks=stocks)


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change password"""
    if request.method == "POST":
        # Get form inputs
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Validate inputs
        if not current_password or not new_password or not confirmation:
            return apology("All fields are required", 400)

        if new_password != confirmation:
            return apology("New passwords do not match", 400)

        # Get user's current hashed password from the database
        user_id = session["user_id"]
        rows = db.execute("SELECT hash FROM users WHERE id = ?", user_id)

        # Check if the current password matches the stored password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], current_password):
            return apology("Invalid current password", 400)

        # Update password in the database
        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_password, user_id)

        # Flash success message and redirect
        flash("Password updated successfully!")
        return redirect("/")
    else:
        # Render the change password form
        return render_template("change_password.html")
