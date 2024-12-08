import os
import shutil

from flask import Blueprint, current_app, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from validator_collection import checkers

from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Query Database
        user = User.query.filter_by(email=email).first()
        if user:
            # Check password hashes
            if check_password_hash(user.password, password):
                # Create a session
                login_user(user, remember=True)
                # Flashing login message
                flash("Logged in successfully.", category="success")
                return redirect(url_for("views.home")) # Finds url to home-function
            else:
                flash("Incorrect credentials.", category="error")
        else:
            flash("Account not found.", category="error")


    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required #  unless logged in no access
def logout():
    # Ending users session
    logout_user()
    flash("Logout successful.", category="success")
    return redirect(url_for("auth.login"))

@auth.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        terms_checkbox = request.form.get("terms_checkbox")  # Get the checkbox value

        user = User.query.filter_by(email=email).first()

        # Check if the checkbox is checked
        if not terms_checkbox:
            flash("You must agree to the Terms of Service and Privacy Policy.", category="error")
            return redirect(url_for("auth.sign_up"))

        # Check credentials
        if user:
            flash("Email is already signed up.", category="error")
        elif len(email) <= 0:
            flash("Email must be greater than 0 characters.", category="error")
        elif not checkers.is_email(email):
            flash("Invalid Email Adress.", category="error")
        elif len(user_name) <= 3:
            flash("Username must be greater than 3 characters.", category="error")

        # Check passwords
        elif password1 != password2:
            flash("Passwords do not match.", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters.", category="error")

        # Create a new User
        else:
            new_user = User(email=email, user_name=user_name, password=generate_password_hash(password1))

            # Add User to Database
            db.session.add(new_user)
            db.session.commit()

            # Create a session right after signing up
            login_user(new_user, remember=True)

            # Create the user-specific directories
            user_dir = os.path.join(current_app.root_path, "filesystem", str(new_user.id))
            img_dir = os.path.join(user_dir, "img")
            text_dir = os.path.join(user_dir, "text")

            # Create the directories if they don't exist
            os.makedirs(user_dir, exist_ok=True)
            os.makedirs(img_dir, exist_ok=True)
            os.makedirs(text_dir, exist_ok=True)

            # Flash a success message
            flash("Account created.", category="success")

            # Redirect to the Home Page
            return redirect(url_for("views.home")) # Finds url to home-function

    return render_template("sign_up.html", user=current_user)

@auth.route("/user_settings", methods=["GET", "POST"])
@login_required
def user_settings():
    # User Deletion
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check Username and Email Adress
        if user_name != current_user.user_name:
            flash("Unexpected Username", category="error")
        elif email != current_user.email:
            flash("Unexpected Email Adress", category="error")
        # Check passwords
        elif password1 != password2:
            flash("Passwords do not match.", category="error")
        elif not check_password_hash(current_user.password, password1):
            flash("Incorrect Password.", category="error")
        else:
            user_dir = os.path.join(current_app.root_path, "filesystem", str(current_user.id))
            if os.path.exists(user_dir):
                shutil.rmtree(user_dir)
            db.session.delete(current_user)
            db.session.commit()
            # session.clear()
            logout_user()
            flash("Your account has been deleted.", category="success")
            return redirect(url_for("auth.login"))

    return render_template("user_settings.html", user=current_user)
