from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import datetime, timedelta
import pytz  # Import pytz for timezone support
import verify_creds_confi
import create_creds_confi


app = Flask(__name__)
app.secret_key = "some_random_string"



def register_data_validation(username, password): 
    """
    Function responsible for validating the 
    user registration data.

        Conditions: 
        username => should be non empty-string and not 
                    be present in the existing user list
        password => should have more than 5 characters
                    (password security not main focus)

    Args:
        username (str): username field input str from user
        password (str): password field input str from user

    Returns:
        Boolean: True or False value defining if both 
                 conditions were met or not 
    """
    
    username_ok = False 
    password_ok = False
    
    if not verify_creds_confi.verify_user_existance(username) and username != "":
        username_ok = True
    if len(password) > 5: 
        password_ok = True 
    
    return username_ok and password_ok


# enforce session expiration after a certain timedelta, (explicit handling) 
@app.before_request
def make_session_permanent():
    session.permanent = True   # activate permanent session
    app.permanent_session_lifetime = timedelta(minutes=5)   # set the timedelta to 5 mins


@app.route("/")
def redirecter():
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login(): 
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        if verify_creds_confi.verify_user_login(user, pw):  # check creds (username & password)
            session["user"] = user
            session["login_time"] = datetime.now(pytz.utc)  # set the login_time of user upon logging in
            flash("Login successful.", category="info")
            return redirect(url_for("home"))
        else:
            flash("Wrong login credentials.", category="error")
            return redirect(url_for("login"))
    else:
        if session.get("user"):  
            return redirect(url_for("home"))  
        else:
            return render_template("login.html")


@app.route("/home")
def home():
    user = session.get("user")
    login_time = session.get("login_time")    # get the login time of user
    if user and login_time and (datetime.now(pytz.utc) - login_time < timedelta(minutes=5)):  # Make datetime.now() timezone-aware and track if the 5 minutes expired
        return render_template("home.html", logged_user=user)    # if time < timedelta, keep user logged in
    else:                                                        # if time < timedelta, delete session data and redirect to login
        session.pop("user", None)
        session.pop("login_time", None)
        return redirect(url_for("login"))


@app.route("/profile")
def profile():
    user = session.get("user")
    if user:
        return render_template("profile.html", logged_user=user)
    else: 
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out.", category="info")
    session.pop("user", None)
    session.pop("login_time", None)
    return redirect(url_for("login"))


@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        new_user = request.form["new_username"]
        new_pw = request.form["new_password"]
        if register_data_validation(new_user, new_pw):   # registration creds validation
            create_creds_confi.save_to_config(new_user, create_creds_confi.encrypt_pw(new_pw))   # create new creds
            flash("Registration successful!", category="info")
            return redirect(url_for("login"))
        else:
            flash("Username existent or password is shorter than 5 characters!", category="error")
            return redirect(url_for("register"))
    else:   # request.method == "GET":
        return render_template("register.html")



if __name__ == "__main__": 
    app.run(debug=True)
