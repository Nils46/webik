from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import os
import random
import urllib,json
from urllib import request
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
    cat = categorieconverter(cats[0])
    cat1 = categorieconverter(cats[1])

    if session.get("user_id") is None:
        return render_template("index.html", cats = cats)

    else:
        account = db.execute("SELECT * FROM users WHERE id= :id", id=session["user_id"])
        firstname = account[0]["firstname"]
        print(firstname)
        return render_template("index.html", firstname = firstname, cats = cats, cat = cat, cat1 = cat1)

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    return upload0()

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("You muust provide your username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("You must provide your password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("Invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # redirect user to home page

        return redirect(url_for("index"))

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
            return apology("You must provide a username")

        # check if password was given
        elif not password:
            return apology("You must provide a password")
        elif not confirmation:
            return apology("You must provide a password once more")
        elif password != confirmation:
            return apology("Passwords did not match")
        elif not first_name:
            return apology("You must provide your first name")
        elif not surname:
            return apology("You must provide your surname")


        hash = pwd_context.hash(password)
        entry = db.execute("INSERT INTO users (username,hash, firstname, surname) VALUES(:username, :hash, :first_name, :surname)",
                           username=request.form.get("username"), hash=hash, first_name=request.form.get("first_name"), surname=request.form.get("surname"))

        session["user_id"] = entry

        db.execute("INSERT INTO pictures (id) VALUES (:id)", id=session["user_id"])

        return redirect(url_for("userbio"))

    else:
        return render_template("register.html")

@app.route("/top", methods=["GET", "POST"])
@login_required
def top():
    return draw_table()

@app.route("/cats", methods=["GET", "POST"])
@login_required
def cats():
    return render_template("cats.html")

@app.route("/userbio", methods=["GET", "POST"])
def userbio():

    cats = categories()

    username = db.execute("SELECT firstname FROM users WHERE id= :id", id=session["user_id"])
    name = username[0]["firstname"]

    if request.method == "POST":

        username = db.execute("SELECT firstname FROM users WHERE id= :id", id=session["user_id"])
        name = username[0]["firstname"]

        db.execute("INSERT INTO userbio (id, bio) VALUES (:id, :bio)",id=session["user_id"], bio=request.form.get("Text1"));

        target = os.path.join(os.getcwd(), 'static/GIPHY/')
        target_url = 'static/GIPHY'

        for file in request.files.getlist("GIPHY"):

            user = str(session["user_id"])

            filename = user + "-" + str(file.filename)

            destination = "/".join([target,filename])
            file.save(destination)

            tot_dest= "/".join([target_url,filename])

            db.execute("UPDATE userbio SET profilepicture = :tot_dest WHERE id = :id", id=session["user_id"], tot_dest = tot_dest)

        return redirect(url_for("index"))

    else:
        return render_template("userbio.html", name=name)

@app.route("/cars", methods=["GET", "POST" ])
@login_required
def cars():
    return grinder0()

@app.route("/yachts", methods=["GET", "POST" ])
@login_required
def yachts():
    return grinder1()

@app.route("/hotels", methods=["GET", "POST" ])
@login_required
def hotels():
    return grinder2()

@app.route("/watches", methods=["GET", "POST" ])
@login_required
def watches():
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

    profilepic = db.execute("SELECT profilepicture FROM userbio WHERE id=:id", id=session["user_id"])
    profilepicture = profilepic[0]["profilepicture"]
    pictures = db.execute("SELECT * FROM pictures WHERE id= :id", id=session["user_id"])
    bio = db.execute("SELECT bio FROM userbio WHERE id= :id", id=session["user_id"])
    userbio = bio[0]["bio"]

    account = db.execute("SELECT * FROM users WHERE id= :id", id=session["user_id"])
    firstname = account[0]["firstname"]
    surname = account[0]["surname"]
    username = account[0]["username"]

    # redirect user to login form
    return render_template("profile.html", userbio = userbio, pictures = pictures, profilepicture = profilepicture,
                            firstname = firstname, surname = surname, username = username)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    if request.method == "POST":

        # change password
        if request.form.get("old_password"):

            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")

            rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id = session["user_id"])

            if len(rows) != 1 or not pwd_context.verify(request.form.get("old_password"), rows[0]['hash']):
                return apology("Old password invalid")

            hash = pwd_context.hash(new_password)

            result = db.execute("UPDATE users SET hash = :hash", hash = hash)

            # return index
            return redirect(url_for("profile"))

        # change username
        elif request.form.get("new_username"):

            new_username = request.form.get("new_username")

            result = db.execute("UPDATE users SET username = :new_username WHERE id = :user_id", user_id = session["user_id"], new_username = new_username)

            if not result:
                return apology("Something went wrong")

            # return index
            return redirect(url_for("profile"))

        # change bio
        elif request.form.get("new_bio"):

            new_bio = request.form.get("new_bio")

            result = db.execute("UPDATE userbio SET bio = :new_bio WHERE id = :user_id", user_id = session["user_id"], new_bio = new_bio)

            if not result:
                return apology("Something went wrong")

            # return index
            return redirect(url_for("profile"))

    else:
        return render_template("settings.html")

@app.route("/follow", methods=["GET", "POST"])
@login_required
def follow():

    id_following = request.form.get("follow")
    print(id_following)

    check = db.execute("SELECT idfollowing FROM following WHERE id=:id", id=session["user_id"])

    for c in check:
        if c["idfollowing"] == id_following:
            continue
        else:
            return apology("already following")

    name_following1= db.execute("SELECT username FROM users WHERE id=:id", id=id_following)
    print(name_following1)
    name_following = name_following1[0]["username"]

    db.execute("INSERT INTO following (id, idfollowing, name_following) VALUES (:id, :id_following, :name_following)", id=session["user_id"], id_following = id_following, name_following=name_following)

    return redirect(url_for("following"))

@app.route("/following", methods=["GET", "POST"])
@login_required
def following():

    following1 = db.execute("SELECT * FROM following WHERE id=:id", id=session["user_id"])

    name = db.execute ("SELECT firstname, surname FROM users WHERE id = :id", id=session["user_id"])

    following=[]

    for f in following1:
        following.append(f["idfollowing"])

    return render_template("following.html", following=following, name=name)


@app.route("/user_profile", methods=["GET", "POST"])
@login_required
def user_profile():

    link = request.form.get("follow")

    user = db.execute("SELECT id FROM likes WHERE link = :link", link = link)

    if not user:
        user = db.execute("SELECT id FROM likes WHERE id = :link", link = link)
        user_id = user[0]["id"]
    else:
        user_id = user[0]["id"]

    pictures = db.execute("SELECT * FROM pictures WHERE id = :user", user = user_id)

    biography = db.execute("SELECT bio, profilepicture FROM userbio WHERE id = :user", user = user_id)
    bio = biography[0]["bio"]
    profilepicture = biography[0]["profilepicture"]

    names = db.execute("SELECT * FROM users WHERE id = :user", user = user_id)
    username = names[0]["username"]
    firstname = names[0]["firstname"]
    surname = names[0]["surname"]

    following = db.execute("SELECT id, idfollowing FROM following WHERE id = :user_id GROUP BY id", user_id = session["user_id"])
    following1 = []

    for i in following:
        value = i.get("idfollowing")
        following1.append(value)

    return render_template("user_profile.html", bio = bio, username = username, firstname = firstname, surname = surname,
                            user_id = user_id, pictures = pictures, following1 = following1, profilepicture = profilepicture)


@app.route("/unfollow", methods=["GET", "POST"])
@login_required
def unfollow():
    if request.method == "POST":
        name=request.form.get("unfollow")
        db.execute("DELETE FROM following WHERE idfollowing = :name", name=name)

        return redirect(url_for("following"))