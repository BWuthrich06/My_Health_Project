"""Server for Health Condition app"""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template("homepage.html")




@app.route('/users')
def new_user():
    """Create new user."""

    return render_template('users.html')




@app.route('/login', methods = ['POST'])
def process_login():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = crud.create_user(email, name, password)

    if session[email]:
        flash("That email or password will not work, please try again.")
    
    else:
        flash("Account successfully created!")
        session['email'] = email

    return redirect('/')






if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
