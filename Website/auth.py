from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash



# hashing functions are functions that have no inverse, use for beefing up password security. sha256 is a hasing algorithm. There are others if you have another preference.
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if check_password_hash(user.password, password):
                flash("Login Success 🙏🏽", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again", category="error")
        else:flash("Email not in database, have you signed up?", category="error")



    return render_template("login.html", user=current_user)




@auth.route("/logout")
@login_required # This decorator assures that you cannot logout without being logged in.
def logout():
    logout_user()
    return redirect(url_for("auth.login"))




@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email is already registered", category="error")

        elif len(email) < 4 :
            flash("Email must be greater than 3 characters", category="error")

        elif len(username) < 2 :
            flash("First name must be greater than 1 character", category="error")

        elif password1 != password2:
            flash("Passwords don't match", category="error")

        elif len(password1) < 7:
            flash("Password must be at least 8 characters", category="error")

        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("sign-up.html", user=current_user)
