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
    user_id = user.user_id

    list_user_conditions = crud.get_all_conditions_by_user_id(user_id)
    set_user_conditions = set(list_user_conditions)
    all_user_conditions = list(set_user_conditions)
    
    all_user_conditions = sorted(all_user_conditions, key=lambda x: x.condition.title)

    return render_template("profile.html", name=name, all_user_conditions=all_user_conditions)



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
            flash("Condition already added.")

            return {"message": "Condition already previously added."}

    saved_condition = crud.create_user_condition(condition, user_id)
    flash("Condition has been successfully added.")
    db.session.add(saved_condition)
    db.session.commit()

    return {"message": "Condition has been successfully added."}
    


@app.route('/addcomments', methods = ["POST"])
def add_comments():
    """Adds users comments to own condition."""

    favorite_id = request.json.get('favorite_id')
    formInput = request.json.get('comment')

    comment = crud.create_comment(favorite_id, formInput)
   
    db.session.add(comment)
    db.session.commit()
    
    return {"message": "Comment added successfully."}


@app.route('/deletecomments', methods = ["POST"])
def delete_comments():
    """Deletes user comment."""

    comment_id = request.json.get("comment_id")

    comment = crud.get_comment_by_id(comment_id)

    db.session.delete(comment)
    db.session.commit()

    return {"message": "Comment deleted."}



@app.route('/deleteusercondition', methods = ["POST"])
def delete_condition():
    """Deletes user condition."""

    favorite_id = int(request.json.get("favorite_id"))

    user_condition = crud.delete_user_condition(favorite_id)

    db.session.delete(user_condition)
    db.session.commit()

    return {"message": "Condition deleted."}



@app.route('/logout', methods = ['POST'])
def logout_user():
    """Logs out user from session."""

    session.clear()

    return redirect('/')


@app.route('/vitals')
def document_vitals():
    """User can input vitals."""

    return render_template('vitals.html')


@app.route('/vitals/results', methods= ['POST'])
def get_vital_results():
    """Results of vitals input."""

    systolic = int(request.form.get("systolic"))
    diastolic = int(request.form.get("diastolic"))
    heart_rate = int(request.form.get("heart_rate"))
    oxygen = int(request.form.get("oxygen"))
    weight = float(request.form.get("weight"))
    glucose = int(request.form.get("glucose"))

    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id

    vitals = crud.create_vital(user_id, systolic, diastolic, heart_rate, oxygen, weight, glucose)
    flash("Vitals documented.")
    db.session.add(vitals)
    db.session.commit()

    return redirect('/vitals/allrecords')


@app.route('/vitals/allrecords')
def show_all_vitals():
    """Shows all records of vitals."""

    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id
    vitals = crud.get_vitals_by_user_id(user_id)

    return render_template("vitals_results.html", vitals=vitals)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

