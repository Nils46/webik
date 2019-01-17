from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

app = Flask(__name__)

@app.route("/account", methods=["GET", "POST"])
def account():
    """Change user password"""
    if request.method == 'POST':

        if not request.form.get('password'):
            return apology("must provide old password")

        rows = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session['user_id'])

        if len(rows) != 1 or not pwd_context.verify(request.form.get('password'), rows[0]['hash']):
            return apology("old password invalid")

        # ensure new password was submitted
        if not request.form.get("new-password"):
            return apology("must provide new password")

        if not request.form.get("password-confirm"):
            return apology("must provide password confirmation")

        if request.form.get("new-password") != request.form.get("password-confirm"):
            return apology("passwords must match")

        password = request.form.get("new-password")
        hash = pwd_context.encrypt(password)

        result = db.execute("UPDATE users SET hash=:hash", hash=hash)
        if not result:
            return apology("that didn't work")

        return redirect(url_for("index"))

    else:
        return render_template("account.html")


