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



@app.route('/create_user')
def create_new_user():
    """View page to create new user."""


    return render_template('new_users.html')



@app.route('/users', methods = ['POST'])
def new_user():
    """Create new user."""

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash("Email unavailable")
        return redirect ('/create_user')

    else:
        user = crud.create_user(email, name, password)
        db.session.add(user)
        db.session.commit()
        flash("Account succesfully created.")

    return redirect('/')



@app.route('/login', methods = ['POST'])
def process_login():
    """Check login credentials."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("Invalid credentials.")

    else:
        flash("Login successful.")
        session['email'] = email
        name = user.name

    return render_template('profile.html', name = name)



@app.route("/conditions")
def all_conditions():
    """View all conditions."""

    conditions = crud.get_conditions()

    return render_template("all_conditions.html", conditions = conditions)



@app.route("/conditions/condition_id")
def show_condition(condition_id):
    """Show details on a condition."""

    condition = crud.get_condition_by_id(condition_id)

    return render_template("condition_details.html", condition = condition)



@app.route('/profile')
def main_profile():
    """Shows main profile page."""

    return render_template("profile.html")



@app.route('/conditions/results')
def get_results():
    """Return search results."""

    result = request.args.get("result")

    results = crud.get_search_results(result)
    print("this is our search results from get search results")
    print(results)


    for condition in results:
        if condition.all_synonyms is not None:
            condition.all_synonyms = condition.all_synonyms.split(',')

    return render_template('results.html', results = results)








    






if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
