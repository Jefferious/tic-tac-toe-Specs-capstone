from flask import (Flask, render_template, request, flash, session, redirect, g)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.before_request
def before_request():
    g.current_user = None
    if "user_email" in session:
        g.current_user = crud.get_user_by_email(session["user_email"])

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    wins = 0
    losses = 0
    draws = 0
    
    existing_user = crud.get_user_by_email(email)
    if existing_user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password, wins, losses, draws)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/homepage")

@app.route("/update", methods=["GET", "POST"])
def update_user():
    """Update user stats."""
    if request.method == "POST":
        # Assuming you have form fields named "wins", "losses", and "draws"
        wins = request.form.get("wins")
        losses = request.form.get("losses")
        draws = request.form.get("draws")

        # Update the user's stats in the database
        crud.update_user_stats(g.current_user.user_id, wins, losses, draws)

        flash("Stats updated successfully!")

    return render_template("update.html", current_user=g.current_user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/homepage")

@app.route('/scores')
def scores():
    # Assuming you have a user object stored in 'current_user'
    user_wins = crud.get_user_wins(g.current_user.user_id)
    user_losses = crud.get_user_losses(g.current_user.user_id)
    user_draws = crud.get_user_draws(g.current_user.user_id)

    return render_template('scores.html', current_user=g.current_user, user_wins=user_wins, user_losses=user_losses, user_draws=user_draws)

@app.route("/homepage")
def homepage():
    

    return render_template("homepage.html", homepage=homepage)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)