from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
import os

from helpers import *

# configure application
app = Flask(__name__)

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
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():

    print("in upload")

    if request.method == "POST":

        print("POST!")
        target = os.path.join(os.getcwd(), 'Image1/')

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "/".join ([target,filename])
            print(destination)
            file.save(destination)

        return render_template("index.html")

    else:
        print("rendering")
        return render_template("upload.html")


@app.route("/upload2", methods=["GET", "POST"])
def upload2():

    print("in upload")

    if request.method == "POST":

        print("POST!")
        target = os.path.join(os.getcwd(), 'Image2/')

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "/".join ([target,filename])
            print(destination)
            file.save(destination)

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

        hash = pwd_context.hash(password)
        entry = db.execute("Insert INTO users (username,hash) VALUES(:username, :hash)",
                           username=request.form.get("username"), hash=hash)
        if not entry:
            return apology("Username already exists")

        session["user_id"] = entry

        return redirect(url_for("userbio"))

    else:
        return render_template("register.html")

<<<<<<< HEAD
@app.route("/settings")
def settings():
=======
@app.route("/top", methods=["GET", "POST"])
def top():
    return render_template("top.html")


@app.route("/userbio", methods=["GET", "POST"])
def userbio():
>>>>>>> 9731eeb21c09642ea25488b063423c39ccf5d6be

    if request.method == "POST":

        old_password = request.form.get("old-password")
        new_password = request.form.get("new-password")

        if not old_password:
            return None

        elif not new_password:
            return None

        if len(rows) != 1 or not pwd_context.verify(request.form.get('password'), rows[0]['hash']):
            return None

<<<<<<< HEAD
        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session['user_id'])

        hash = pwd_context.encrypt(new_password)

        result = db.execute("UPDATE users SET hash=:hash", hash=hash)

        if not result:
            return None

    else:
        return render_template("settings.html")

@app.route("/top")
def top():
    return render_template("Top10.html")
=======
    username = db.execute("SELECT username FROM users WHERE id= :id", id=session["user_id"])
    name= username[0]["username"]

    if request.method == "POST":
        db.execute("INSERT INTO userbio (id, bio) VALUES (:id, :bio)",id=session["user_id"], bio=request.form.get("Text1"));

        return redirect(url_for("index"))
    else:
        return render_template("userbio.html", name=name)
>>>>>>> 9731eeb21c09642ea25488b063423c39ccf5d6be
