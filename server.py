"""Server for Health Condition app"""
import os
from flask import Flask, render_template, request, flash, session, redirect, jsonify, request
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from pprint import pprint
from passlib.hash import argon2


API_KEY = os.environ['my_api_key']
secret_key = os.environ['secret_key']

app = Flask(__name__)
app.secret_key = secret_key
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

    #Get input user entered.
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #Check if email is taken.
    if crud.get_user_by_email(email):
        flash("Account already active, please log in.")

        return redirect ('/')

    #Create new user account and add to database.
    elif email and name and password:

        hash_password = argon2.hash(password)

        #Create new account
        user = crud.create_user(email, name, hash_password)
        db.session.add(user)
        db.session.commit()
        flash("Account successfully created.")

        #Store in session.
        session['email'] = email
        session['name'] = name
        session['user_id'] = user.user_id

        return redirect('/profile')
    
    else:
        flash("Missing values, please fill in all fields.")
        return redirect('/create_user')



@app.route('/login', methods = ['POST'])
def process_login():
    """Check login credentials."""

    #Check if user is logged in.
    if 'email' in session:
        return redirect('/profile')

    #get input user entered.
    email = request.form.get('email')
    password = request.form.get('password')

    #Get user email
    user = crud.get_user_by_email(email)

    #Login success, store session 'email'
    if user and argon2.verify(password, user.password):
        session['email'] = email
    
        return redirect('/profile')

    #Invalid login.
    else:
        flash("Invalid credentials.")

        return redirect('/')




@app.route('/profile')
def main_profile():
    """Shows main profile page."""
    
    #Check if user is logged in.
    if 'email' in session:

        #Get user id and user name.
        user = crud.get_user_by_email(session['email'])
        name = user.name
        user_id = user.user_id

        #Get all saved user conditions
        list_user_conditions = crud.get_all_conditions_by_user_id(user_id)
        set_user_conditions = set(list_user_conditions)
        all_user_conditions = list(set_user_conditions)
        
        #Sort saved user conditions alphabetically
        all_user_conditions = sorted(all_user_conditions, key=lambda x: x.condition.title)

        #Get all saved physicians of user
        saved_physicians = crud.get_physicians_by_user_id(user_id)

        #Get most recent vitals entered by user
        vitals = crud.get_recent_vital(user_id)

        return render_template("profile.html", name=name, all_user_conditions=all_user_conditions, saved_physicians=saved_physicians, vitals=vitals)
    
    #Redirect user to login.
    else:
        flash("You must login first.")
        return redirect('/')



@app.route("/conditions")
def all_conditions():
    """View all conditions."""

    #Check if user is logged in.
    if "email" in session:

        #Show all health conditions A to Z.
        conditions = crud.get_conditions()
        return render_template("all_conditions.html", conditions=conditions)

    #Redirect user to login.
    else:
        flash("You must login first.")
        return redirect('/')



@app.route('/conditions/search')
def search_conditions():
    """Search for conditions."""

    #Check if user is logged in.
    if 'email' in session:
        return render_template('condition_search.html')
    
    #Redirect user to login.
    else:
        flash("You must login first.")
        return redirect('/')



@app.route('/conditions/results')
def get_results():
    """Return search results."""

    #Check if user is logged in.
    if 'email' in session:

        #Get string user entered for health condition to search
        result = request.args.get("result")
        result = result.title()

        #Get search results back similar to what user searched
        results = crud.get_search_results(result)

        if results:
            return render_template('results.html', results=results, result=result)
        
        #No matches/results.
        else:
            flash("No matching results.")
            return redirect('/conditions/search')
    
    #Redirect user to login.
    else:
        flash("You must login first.")
        return redirect('/')
        


@app.route('/addcondition', methods = ["POST"])
def add_condition_to_user():

    #Get condition user wants to add from fetch request.
    condition = int(request.json.get("condition"))

    #Get user id
    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id

    #Get all conditions user has saved.
    list_user_conditions = crud.get_all_conditions_by_user_id(user_id)

    #Loop through all saved conditions to check if already added.
    for user_condition in list_user_conditions:
        if user_condition.condition_id == condition:
            flash("Condition already added.")

            return {"message": "Condition already previously added."}

    #Create new saved user condition, add to database.
    saved_condition = crud.create_user_condition(condition, user_id)
    flash("Condition has been added successfully.")
    db.session.add(saved_condition)
    db.session.commit()

    return {"message": "Condition has been successfully added."}
    


@app.route('/addcomments', methods = ["POST"])
def add_comments():
    """Adds users comments to own condition."""

    #Get saved user condition and comment user added from fetch request.
    favorite_id = request.json.get('favorite_id')
    formInput = request.json.get('comment')

    #Create new comment for user saved condition, add to database.
    comment = crud.create_comment(favorite_id, formInput)
    db.session.add(comment)
    db.session.commit()
    
    return {"message": "Comment added successfully."}


@app.route('/deletecomments', methods = ["POST"])
def delete_comments():
    """Deletes user comment."""

    #Get comment(s) from fetch request to delete.
    comment_ids = request.json.get("comment_ids")
  
    #for every comment, get the comment id
    for comment_id in comment_ids:
        comment = crud.get_comment_by_id(comment_id)

        #Delete comment from database
        if comment:
            db.session.delete(comment)
            db.session.commit()

    return {"message": "Comment deleted."}



@app.route('/deleteusercondition', methods = ["POST"])
def delete_condition():
    """Deletes user condition."""

    #Get user saved condition from fetch request to delete.
    favorite_id = int(request.json.get("favorite_id"))

    #Delete user saved condition from database.
    user_condition = crud.delete_user_condition(favorite_id)
    db.session.delete(user_condition)
    db.session.commit()

    return {"message": "Condition deleted."}



@app.route('/logout', methods = ['POST'])
def logout_user():
    """Logs out user from session."""

    #Clears user session on logout.
    session.clear()

    return redirect('/')


@app.route('/vitals')
def document_vitals():
    """User can input vitals."""

    #Check to see if user is logged in.
    if 'email' in session: 
        return render_template('vitals.html')
    
    #Redirect user to login.
    else:
        flash("You must login first.")
        return redirect('/')
   


@app.route('/vitals/results', methods= ['POST'])
def get_vital_results():
    """Results of vitals input."""

    #Get form input results of users vitals entered.
    systolic = request.json.get("systolic")
    diastolic = request.json.get("diastolic")
    heart_rate = request.json.get("heartRate")
    oxygen = request.json.get("oxygen")
    weight = request.json.get("weight")
    glucose = request.json.get("glucose")

    if systolic:
        systolic = int(systolic)
    else:
        systolic = None

    if diastolic:
        diastolic = int(diastolic)
    else:
        diastolic = None

    if heart_rate:
        heart_rate = int(heart_rate)
    else:
        heart_rate = None

    if oxygen:
        oxygen = int(oxygen)
    else:
        oxygen = None

    if weight:
        weight = float(weight)
    else:
        weight = None

    if glucose:
        glucose = int(glucose)
    else:
        glucose = None

    #Get user_id
    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id

    #Create new set of vitals user entered and add to database.
    vitals = crud.create_vital(user_id, systolic, diastolic, heart_rate, oxygen, weight, glucose)
    flash("Vitals documented.")
    db.session.add(vitals)
    db.session.commit()

    return {"Message": "Vitals added successfully."}




@app.route('/vitals/allrecords')
def show_all_vitals():
    """Shows all records of vitals."""

    #Check to see if user is logged in
    if 'email' in session:

        #Get user id and user name
        user = crud.get_user_by_email(session['email'])
        user_id = user.user_id
        name = user.name

        #Get all vitals by user id
        vitals = crud.get_vitals_by_user_id(user_id)

        return render_template("vitals_results.html", vitals=vitals, name=name)
    
    #Redirect user to login.
    else:
        flash("You must login first.")
        return redirect('/')


@app.route('/vitals_graph')
def show_vital_graphs():
    """Shows graphs of vital signs."""

    #Check to see if user is logged in.
    if 'email' in session:
        return render_template('vitals_graph.html')
    
    #Redirect user to login.
    else:
        flash("You must login first.")
        return redirect('/')



@app.route('/all_vitals_graph')
def get_all_vitals_for_graph():
    """Gets all vitals."""

    #Get user id
    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id

    #Get all vitals of user
    vitals = crud.get_vitals_by_user_id(user_id)

    #List to hold all vitals
    data = []

    #Loop through all vitals and put values in dictionary
    for vital in vitals:
        vital = {
            'date_time': vital.date_time.strftime("%m/%d/%Y %I:%M %p"),
            'systolic': vital.systolic,
            'diastolic': vital.diastolic,
            'heart_rate': vital.heart_rate,
            'oxygen': vital.oxygen,
            'weight': vital.weight,
            'glucose': vital.glucose
            }
        data.append(vital)

    return jsonify ({'vitals': data})



@app.route('/findphysician')
def find_physician():
    """Search for physician."""

    #Check to see if user is logged in
    if 'email' in session:
        return render_template('find_physician.html', APIKEY=API_KEY)
    
    #Redirect user to login.
    else:
        flash("You must login first.")
        return redirect('/')



@app.route('/add_physician', methods=['POST'])
def add_physician():
    """Add physician to user profile."""

    #Data sent over from fetch request.
    place_id = request.json.get("place_id")
    name = request.json.get("name")
    address = request.json.get("address")
    phone = request.json.get("phone")
    url = request.json.get("url")

    #Get user_id
    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id

    #Get all saved physicians of user.
    physicians = crud.get_physicians_by_user_id(user_id)
    print(physicians)

    #Check physicians already saved to user
    if physicians:

        for physician in physicians:

            if physician.place_id == place_id:
                flash("Physician already added.")

                return {"message": "Physician already previously added."}
            
    #Create user physician and save to database.
    saved_physician = crud.create_physician(place_id, name, address, phone, url, user_id)
    print(saved_physician)
    db.session.add(saved_physician)
    db.session.commit()
    flash("Physician has been successfully added.")

    return jsonify ({"message": "Condition has been successfully added."})


@app.route('/delete_physician', methods=["POST"])
def delete_physician():

    #Get id of delete button user clicked
    physician_id = request.form.get("physician_id")

    #Get physician to delete by id, delete from database.
    physician = crud.delete_physician(physician_id)
    db.session.delete(physician)
    db.session.commit()
    flash("Physician deleted successfully.")

    return redirect('/profile')


    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

