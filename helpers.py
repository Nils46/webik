from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime
import os
import random
import time
from flask import redirect, render_template, request, session
from functools import wraps
from werkzeug.utils import secure_filename

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

    random.seed(datetime.today().microsecond)

    url = db.execute("SELECT pic FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic"]
    if url_choice == None:
        return grinder0()
    elif url_choice_2 == None:
        return grinder0()
    elif url_choice == url_choice_2:
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

    #random.seed(datetime.today().microsecond)
    url = db.execute("SELECT pic1 FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic1"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic1"]
    if url_choice == None:
        return grinder1()
    elif url_choice_2 == None:
        return grinder1()
    elif url_choice == url_choice_2:
        return grinder1()

    else:
        if request.method == "POST":
            if request.form.get("Foto3") == "Ja":
                link= request.form.get("link1")
                like = 1
                db.execute("UPDATE userbio SET like1 = like1 + :like WHERE pic1 = :pic", pic=link, like=like)
            elif request.form.get("Foto4") == "Ja":
                link= request.form.get("link2")
                like = 1
                db.execute("UPDATE userbio SET like1 = like1 + :like WHERE pic1 = :pic", pic=link, like=like)


            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item2")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item2")


def grinder2(): #if cat == "Hotels":

    #random.seed(datetime.today().microsecond)

    url = db.execute("SELECT pic2 FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic2"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic2"]
    if url_choice == None:
        return grinder2()
    elif url_choice_2 == None:
        return grinder2()
    elif url_choice == url_choice_2:
        return grinder2()

    else:
        if request.method == "POST":
            if request.form.get("Foto5") == "Ja":
                link= request.form.get("link1")
                like = 1
                db.execute("UPDATE userbio SET like2 = like2 + :like WHERE pic2 = :pic", pic=link, like=like)
            elif request.form.get("Foto6") == "Ja":
                link= request.form.get("link2")
                like = 1
                db.execute("UPDATE userbio SET like2 = like2 + :like WHERE pic2 = :pic", pic=link, like=like)


            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item3")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item3")


def grinder3(): #if cat == "Hotels":

    #random.seed(datetime.today().microsecond)

    url = db.execute("SELECT pic3 FROM userbio")
    send_url=(random.choice(url))
    url_choice=send_url["pic3"]
    send_url_2=(random.choice(url))
    url_choice_2=send_url_2["pic3"]
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
                like = 1
                db.execute("UPDATE userbio SET like3 = like3 + :like WHERE pic3 = :pic", pic=link, like=like)
            elif request.form.get("Foto8") == "Ja":
                link= request.form.get("link2")
                like = 1
                db.execute("UPDATE userbio SET like3 = like3 + :like WHERE pic3 = :pic", pic=link, like=like)

            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item4")
        else:
            return render_template("grinder.html", url_choice=url_choice, url_choice_2=url_choice_2, cat="item4")

def draw_table():
    userlist=list()
    valuelist=list()
    tot=0
    tempo = db.execute("SELECT id FROM userbio")
    temp =db.execute("SELECT username,tot FROM users")
    for x in temp:
        userlist.append(x["username"])
    for x in tempo:
        tot=0
        user=(x["id"])
        temp_like = db.execute("SELECT like FROM userbio WHERE id= :id", id=user)
        temp_like1 = db.execute("SELECT like1 FROM userbio WHERE id= :id", id=user)
        temp_like2 = db.execute("SELECT like2 FROM userbio WHERE id= :id", id=user)
        temp_like3 = db.execute("SELECT like3 FROM userbio WHERE id= :id", id=user)
        for y in temp_like:
            like=0
            like=(y["like"])
        for y in temp_like1:
            like1=0
            like1=(y)["like1"]
        tot=tot+like1
        for y in temp_like2:
            like2=0
            like2=(y)["like2"]
        tot=tot+like2
        for y in temp_like3:
            like3=0
            like3=(y)["like3"]
        tot=[like, like1, like2, like3]
        tot =(sum(tot))
        valuelist.append(tot)
    data = dict(zip(userlist,valuelist))

    data = sorted(data.items(), key = lambda x:x[1], reverse=True)
    data=dict(data)


    return render_template("top.html", data=data)

def upload0():



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
            if check == "Cars":
                db.execute("ALTER TABLE userbio ADD pic text")
                db.execute("ALTER TABLE userbio ADD like INT DEFAULT 0")
            elif check == "Yachts":
                db.execute("ALTER TABLE userbio ADD pic1 text")
                db.execute("ALTER TABLE userbio ADD like1 INT DEFAULT 0")
            elif check == "Hotels":
                db.execute("ALTER TABLE userbio ADD pic2 text")
                db.execute("ALTER TABLE userbio ADD like2 INT DEFAULT 0")
            elif check == "Watches":
                db.execute("ALTER TABLE userbio ADD pic3 text")
                db.execute("ALTER TABLE userbio ADD like3 INT DEFAULT 0")

        for file in request.files.getlist("file"):
            user = str(session["user_id"])
            print(file)
            filename = user + "-" + str((secure_filename(file.filename)))
            print(filename)
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


        return redirect(url_for("index"))

    else:
        print("rendering")
        return render_template("upload.html")
