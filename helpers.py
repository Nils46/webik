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
    
    #random.seed(datetime.today().day)
    #print(datetime.today().day)
    #number = random.randint(0,24)
    #print(number)
    
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
def grinder0(): #if cat == "Hotels":

    url = db.execute("SELECT pic FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic"]
    if url_choice == url_choice_2:
        return grinder0()

    else:
        if request.method == "POST":
            if request.form.get("Foto1") == "Ja":
                link= request.form.get("link1")
                like = 1
                db.execute("UPDATE userbio SET like = like + :like WHERE pic = :pic", pic=link, like=like)
            elif request.form.get("Foto2") == "Ja":
                link= request.form.get("link2")
                like = 1
                db.execute("UPDATE userbio SET like = like + :like WHERE pic = :pic", pic=link, like=like)


            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item1")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item1")

def grinder1(): #if cat == "Hotels":

    url = db.execute("SELECT pic1 FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic1"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic1"]
    if url_choice == url_choice_2:
        return grinder1()

    else:
        if request.method == "POST":
            if request.form.get("Foto3") == "Ja":
                link= request.form.get("link1")
                like = 1
                db.execute("UPDATE userbio SET like = like + :like WHERE pic1 = :pic", pic=link, like=like)
            elif request.form.get("Foto4") == "Ja":
                link= request.form.get("link2")
                like = 1
                db.execute("UPDATE userbio SET like = like + :like WHERE pic1 = :pic", pic=link, like=like)


            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item2")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item2")


def grinder2(): #if cat == "Hotels":

    url = db.execute("SELECT pic2 FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic2"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic2"]
    if url_choice == url_choice_2:
        return grinder2()

    else:
        if request.method == "POST":
            if request.form.get("Foto5") == "Ja":
                link= request.form.get("link1")
                like = 1
                db.execute("UPDATE userbio SET like = like + :like WHERE pic2 = :pic", pic=link, like=like)
            elif request.form.get("Foto6") == "Ja":
                link= request.form.get("link2")
                like = 1
                db.execute("UPDATE userbio SET like = like + :like WHERE pic2 = :pic", pic=link, like=like)


            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item3")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item3")


def grinder3(): #if cat == "Hotels":

    url = db.execute("SELECT pic3 FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic3"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic3"]
    if url_choice == url_choice_2:
        return grinder3()

    else:
        if request.method == "POST":
            if request.form.get("Foto7") == "Ja":
                link= request.form.get("link1")
                like = 1
                db.execute("UPDATE userbio SET like = like + :like WHERE pic3 = :pic", pic=link, like=like)
            elif request.form.get("Foto8") == "Ja":
                link= request.form.get("link2")
                like = 1
                db.execute("UPDATE userbio SET like = like + :like WHERE pic3 = :pic", pic=link, like=like)


            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item4")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item4")
