from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime
import os
import random
import time
from functools import wraps

db = SQL("sqlite:///database.db")

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

    categories = ["Cars", "Yachts", "Hotels", "Watches"]
    randam = random.sample(categories,2)
    random_category = randam[0]
    random_category_1 = randam[1]
    url = random_category + ".jpg"
    url1 = random_category_1 + ".jpg"

    return random_category, random_category_1, url, url1

def names():

    account = db.execute("SELECT * FROM users WHERE id= :id", id=session["user_id"])
    name = account[0]["username"]
    return name

def grinder0(): #if category == "Cars":

    random.seed(datetime.today().microsecond)

    url = db.execute("SELECT cars FROM pictures")
    randomm = random.sample(url,2)
    print(randomm)
    url_choice = randomm[0]["cars"]
    url_choice_2 = randomm[1]["cars"]
    print(url_choice, url_choice_2)

    if url_choice == None:
        return grinder0()
    elif url_choice_2 == None:
        return grinder0()

    else:
        if request.method == "POST":
            if request.form.get("Foto1") == "Ja":
                link= request.form.get("link1")
                db.execute("UPDATE likes SET amount = amount + 1 WHERE link = :link", link = link)
            elif request.form.get("Foto2") == "Ja":
                link= request.form.get("link2")
                db.execute("UPDATE likes SET amount = amount + 1 WHERE link = :link", link = link)

            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, category = "cars")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, category = "cars")

def grinder1(): #if cat == "Yachts":

    random.seed(datetime.today().microsecond)

    url = db.execute("SELECT yachts FROM pictures")
    send_url=(random.choice(url))
    url_choice=send_url["yachts"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["yachts"]

    if url_choice == None:
        return grinder2()
    elif url_choice_2 == None:
        return grinder2()
    elif url_choice == url_choice_2:
        return grinder2()

    else:
        if request.method == "POST":
            if request.form.get("Foto3") == "Ja":
                link = request.form.get("link1")
                db.execute("UPDATE likes SET amount = amount + 1 WHERE link = :link", link = link)
            elif request.form.get("Foto4") == "Ja":
                link = request.form.get("link2")
                db.execute("UPDATE likes SET amount = amount + 1 WHERE link = :link", link = link)

            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, category = "yachts")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, category = "yachts")

def grinder2(): #if category == "Hotels":

    random.seed(datetime.today().microsecond)

    url = db.execute("SELECT hotels FROM pictures")
    print(url)
    send_url=(random.choice(url))
    url_choice=send_url["hotels"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["hotels"]

    if url_choice == None:
        return grinder1()
    elif url_choice_2 == None:
        return grinder1()
    elif url_choice == url_choice_2:
        return grinder1()

    else:
        if request.method == "POST":
            if request.form.get("Foto5") == "Ja":
                link= request.form.get("link1")
                db.execute("UPDATE likes SET amount = amount + 1 WHERE link = :link", link = link)
            elif request.form.get("Foto6") == "Ja":
                link= request.form.get("link2")
                db.execute("UPDATE likes SET amount = amount + 1 WHERE link = :link", link = link)

            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, category = "hotels")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, category = "hotels")

def grinder3(): #if cat == "Watches":

    random.seed(datetime.today().microsecond)

    url = db.execute("SELECT watches FROM pictures")
    send_url=(random.choice(url))
    url_choice=send_url["watches"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["watches"]
    if url_choice == None:
        return grinder3()
    elif url_choice_2 == None:
        return grinder3()
    elif url_choice == url_choice_2:
        return grinder3()

    else:
        if request.method == "POST":
            if request.form.get("Foto7") == "Ja":
                link= request.form.get("link1")
                db.execute("UPDATE likes SET amount = amount + 1 WHERE link = :link", link = link)
            elif request.form.get("Foto8") == "Ja":
                link= request.form.get("link2")
                db.execute("UPDATE likes SET amount = amount + 1 WHERE link = :link", link = link)

            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, category = "watches")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, category = "watches")

def draw_table():

    ranking = db.execute("SELECT users.username as user, SUM(amount) as amount FROM users, likes WHERE users.id = likes.id GROUP BY likes.id")

    data = {}
    for i in ranking:
        key = i.get("user")
        value = i.get("amount")
        data.update({key:value})

    data = dict(sorted(data.items(), key = lambda x:x[1], reverse=True)[0:10])

    return render_template("top.html", data=data)

def upload0():

    if request.method == "POST":

        check = request.form.get('select')

        if check == "Cars":
            target = os.path.join(os.getcwd(), 'static/Cars/')
            target_url = 'static/Cars'

        elif check == "Yachts":
            target = os.path.join(os.getcwd(), 'static/Yachts/')
            target_url = 'static/Yachts'

        elif check == "Hotels":
            target = os.path.join(os.getcwd(), 'static/Hotels/')
            target_url = 'static/Hotels'

        elif check == "Watches":
            target = os.path.join(os.getcwd(), 'static/Watches/')
            target_url = 'static/Watches'

        if not os.path.isdir(target):
            os.mkdir(target)
            if check == "Cars":
                db.execute("ALTER TABLE pictures ADD cars text")
            elif check == "Yachts":
                db.execute("ALTER TABLE pictures ADD yachts text")
            elif check == "Hotels":
                db.execute("ALTER TABLE pictures ADD hotels text")
            elif check == "Watches":
                db.execute("ALTER TABLE pictures ADD watches text")

        for file in request.files.getlist("file"):

            user = str(session["user_id"])

            filename = user + "-" + str(file.filename)

            destination = "/".join ([target,filename])

            file.save(destination)

            tot_dest= "/".join([target_url,filename])

            if check =="Cars":

                db.execute("UPDATE pictures SET cars = :cars WHERE id = :id", id=session["user_id"], cars = tot_dest)
                db.execute("INSERT INTO likes (id, link, amount, category) VALUES (:id, :link, :amount, :category)",
                            id = session["user_id"], link = tot_dest, amount = 0, category = "cars")

            elif check =="Yachts":

                db.execute("UPDATE pictures SET yachts = :yachts WHERE id = :id", id=session["user_id"], yachts = tot_dest)
                db.execute("INSERT INTO likes (id, link, amount, category) VALUES (:id, :link, :amount, :category)",
                            id = session["user_id"], link = tot_dest, amount = 0, category = "yachts")

            elif check =="Hotels":

                db.execute("UPDATE pictures SET hotels = :hotels WHERE id = :id", id=session["user_id"], hotels = tot_dest)
                db.execute("INSERT INTO likes (id, link, amount, category) VALUES (:id, :link, :amount, :category)",
                id = session["user_id"], link = tot_dest, amount = 0, category = "hotels")

            else:
                db.execute("UPDATE pictures SET watches = :watches WHERE id = :id", id=session["user_id"], watches = tot_dest)
                db.execute("INSERT INTO likes (id, link, amount, category) VALUES (:id, :link, :amount, :category)",
                id = session["user_id"], link = tot_dest, amount = 0, category = "watches")

        return redirect(url_for("index"))

    else:

        return render_template("upload.html")