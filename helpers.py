from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime
import os
import random

from flask import redirect, render_template, request, session
from functools import wraps

db = SQL("sqlite:///database.db")

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def categories():

    random.seed(datetime.today().day)
    print(datetime.today().day)
    number = random.randint(0,24)
    print(number)

    categories = ["Cars", "Yachts", "Hotels", "Watches"]
    random_category = random.choice(categories)
    random_category_1 = random.choice(categories)
    url = random_category + ".jpg"
    url1 = random_category_1 + ".jpg"

    return random_category, random_category_1, url, url1

def names():
    account = db.execute("SELECT * FROM users WHERE id= :id", id=session["user_id"])
    name = account[0]["username"]
    return name
