from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import os
import random

from helpers import *

# configure application
app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.route('/')
@app.route('/index')
def index():

    cats = categories()

    if session.get("user_id") is None:
        return render_template("index.html", cats = cats)
    else:
        name = names()
        return render_template("index.html", cats = cats, name = name)

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        check = request.form.get('select')
        print(check)

        if check == "Cars":
            target = os.path.join(os.getcwd(), 'static/Image1/')
            target_url = 'static/Image1'

        elif check == "Yachts":
            target = os.path.join(os.getcwd(), 'static/Image2/')
            target_url = 'static/Image2'

        elif check == "Hotels":
            target = os.path.join(os.getcwd(), 'static/Image3/')
            target_url = 'static/Image3'

        elif check == "Watches":
            target = os.path.join(os.getcwd(), 'static/Image4/')
            target_url = 'static/Image4'

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "/".join ([target,filename])
            print(destination)
            file.save(destination)
            tot_dest= "/".join([target_url,filename])
            if check =="Cars":
                db.execute("UPDATE userbio SET pic=:pic WHERE id=:id",id=session["user_id"], pic=tot_dest)
            elif check =="Yachts":
                db.execute("UPDATE userbio SET pic1=:pic1 WHERE id=:id",id=session["user_id"], pic1=tot_dest)
            elif check =="Hotels":
                db.execute("UPDATE userbio SET pic2=:pic2 WHERE id=:id",id=session["user_id"], pic2=tot_dest)
            else:
                db.execute("UPDATE userbio SET pic3=:pic3 WHERE id=:id",id=session["user_id"], pic3=tot_dest)
        return render_template("index.html")

    else:
        print("rendering")
        return render_template("upload.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # redirect user to home page

        cats = categories()
        name = names()

        return render_template("index.html", cats=cats, name=name)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    # check if user is submitting via "POST"
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        surname = request.form.get("surname")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # check if username was given
        if not username:
            return apology("must provide username")

        # check if password was given
        elif not password:
            return apology("must provide password")
        elif not confirmation:
            return apology("must provide password once more")
        elif password != confirmation:
            return apology("Passwords didn`t match")
        elif not first_name:
            return apology("must provide first name")
        elif not surname:
            return apology("must provide surname")


        hash = pwd_context.hash(password)
        entry = db.execute("Insert INTO users (username,hash, first_name, surname) VALUES(:username, :hash, :first_name, :surname)",
                           username=request.form.get("username"), hash=hash, first_name=request.form.get("first_name"), surname=request.form.get("surname"))
        if not entry:
            return apology("Username already exists")

        session["user_id"] = entry

        return redirect(url_for("userbio"))

    else:
        return render_template("register.html")

@app.route("/top", methods=["GET", "POST"])
@login_required
def top():
    return render_template("top.html")


@app.route("/userbio", methods=["GET", "POST"])
def userbio():

    cats = categories()
    name = names()

    if request.method == "POST":
        db.execute("INSERT INTO userbio (id, bio) VALUES (:id, :bio)",id=session["user_id"], bio=request.form.get("Text1"));

        return render_template("index.html", cats=cats, name=name)
    else:
        return render_template("userbio.html", name=name)

@app.route("/grinder_car", methods=["GET", "POST" ])
@login_required
def grinder_car():
    return grinder0()

@app.route("/grinder_yacht", methods=["GET", "POST" ])
@login_required
def grinder_yacht():
    return grinder1()

@app.route("/grinder_hotel", methods=["GET", "POST" ])
@login_required
def grinder_hotel():
    return grinder2()

@app.route("/grinder_watch", methods=["GET", "POST" ])
@login_required
def grinder_watch():
    return grinder3()
@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("index"))

@app.route("/profile")
@login_required
def profile():

    profile = db.execute("SELECT * FROM users WHERE id= :id", id=session["user_id"])
    pictures = db.execute("SELECT * FROM userbio WHERE id= :id", id=session["user_id"])
    bio = db.execute("SELECT * FROM userbio WHERE id= :id", id=session["user_id"])
    userbio = bio[0]["bio"]
    username = profile[0]["username"]

    # redirect user to login form
    return render_template("profile.html", username = username, userbio = userbio, pictures = pictures)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")

        if not old_password:
            return apology("Fill in all fields")
        elif not new_password:
            return apology("Fill in all fields")

        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id = session["user_id"])

        if len(rows) != 1 or not pwd_context.verify(request.form.get("old_password"), rows[0]['hash']):
            return apology("Old password invalid")

        hash = pwd_context.hash(new_password)

        result = db.execute("UPDATE users SET hash = :hash", hash = hash)

        if not result:
            return apology("Something went wrong")

        cats = categories()
        name = names()

        return render_template("index.html", cats=cats, name=name)

    else:
        return render_template("settings.html")
