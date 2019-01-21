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
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    print("in upload")

    if request.method == "POST":

        check = request.form.get('select')
        print(check)

        if check == "auto":
            target = os.path.join(os.getcwd(), 'static/Image1/')
            target_url = 'static/Image1'

        else:
            target = os.path.join(os.getcwd(), 'static/Image2/')
            target_url = 'static/Image2'
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "/".join ([target,filename])
            print(destination)
            file.save(destination)
            tot_dest= "/".join([target_url,filename])
            if check =="auto":
                db.execute("UPDATE userbio SET pic=:pic WHERE id=:id",id=session["user_id"], pic=tot_dest)
            else:
                db.execute("UPDATE userbio SET pic1=:pic1 WHERE id=:id",id=session["user_id"], pic1=tot_dest)
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


        username = db.execute("SELECT username FROM users WHERE id= :id", id=session["user_id"])
        name= username[0]["username"]

        return render_template("index.html", name=name)

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

@app.route("/top", methods=["GET", "POST"])
@login_required
def top():
    return render_template("top.html")


@app.route("/userbio", methods=["GET", "POST"])
def userbio():


    username = db.execute("SELECT username FROM users WHERE id= :id", id=session["user_id"])
    name= username[0]["username"]

    if request.method == "POST":
        db.execute("INSERT INTO userbio (id, bio) VALUES (:id, :bio)",id=session["user_id"], bio=request.form.get("Text1"));

        return render_template("index.html", name=name)
    else:
        return render_template("userbio.html", name=name)

@app.route("/grinder")
@login_required
def grinder():
    url = db.execute("SELECT pic FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic"]
    #if url_choice == url_choice_2:
        #return grinder()
    #else:
        #return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2)

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
    bio = db.execute("SELECT * FROM userbio WHERE id= :id", id=session["user_id"])
    userbio = bio[0]["bio"]
    username = profile[0]["username"]

    # redirect user to login form
    return render_template("profile.html", username = username, userbio = userbio)

@app.route("/settings")
def settings():

    return render_template("settings.html")
