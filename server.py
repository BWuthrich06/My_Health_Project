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
        flash("Account already active, please log in.")
        return redirect ('/')

    else:
        user = crud.create_user(email, name, password)
        db.session.add(user)
        db.session.commit()
        flash("Account succesfully created.")

        session['email'] = email
        session['name'] = name
        session['user_id'] = user.user_id

    return redirect('/profile')



@app.route('/login', methods = ['POST'])
def process_login():
    """Check login credentials."""

    if 'email' in session:
        return redirect('/profile')

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if not user or user.password != password:
        flash("Invalid credentials.")
        return redirect('/')

    else:
        flash("Login successful.")
        session['email'] = email
    

    return redirect('/profile')



@app.route('/profile')
def main_profile():
    """Shows main profile page."""
    
    user = crud.get_user_by_email(session['email'])
    name = user.name

    return render_template("profile.html", name=name)



@app.route("/conditions")
def all_conditions():
    """View all conditions."""

    conditions = crud.get_conditions()

    return render_template("all_conditions.html", conditions=conditions)



@app.route('/conditions/search')
def search_conditions():
    """Search for conditions."""

    return render_template('condition_search.html')



@app.route('/conditions/results')
def get_results():
    """Return search results."""

    result = request.args.get("result")
    result = result.title()

    results = crud.get_search_results(result)

    if results:
        return render_template('results.html', results = results, result = result)
    else:
        flash("No results matched.")
        return redirect('/conditions/search')
    


@app.route('/addcondition', methods = ["POST"])
def add_condition_to_user():

    condition = int(request.json.get("condition"))
    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id

    list_user_conditions = crud.get_all_conditions_by_user_id(user_id)

    for user_condition in list_user_conditions:
        if user_condition.condition_id == condition:
            flash("Condition already previously added.")
            return {"message": "Condition already previously added."}


    saved_condition = crud.create_user_condition(condition, user_id)
    flash("Condition has been successfully added.")
    db.session.add(saved_condition)
    db.session.commit()

    return {"message": "Condition has been successfully added."}
    


@app.route('/profile/saved')
def get_saved_conditions():
    """Return saved conditions."""

    email = session['email']
    
    user = crud.get_user_by_email(email)
    user_id = user.user_id
    
    list_user_conditions = crud.get_all_conditions_by_user_id(user_id)
    set_user_conditions = set(list_user_conditions)
    all_user_conditions = list(set_user_conditions)

    return render_template('/saved_conditions.html', all_user_conditions=all_user_conditions)


@app.route('/addcomments', methods = ["POST"])
def add_comments():
    """Adds users comments to own condition."""

    favorite_id = request.json.get('favorite_id')
    formInput = request.json.get('comment')

    comment = crud.create_comment(favorite_id, formInput)
    # db.session.add(comment)
    db.session.commit()

    return {"message": "Comment has been successfully added."}





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

