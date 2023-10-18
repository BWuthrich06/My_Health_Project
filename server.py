"""Server for Health Condition app"""
import os
from flask import Flask, render_template, request, flash, session, redirect, jsonify, request
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import requests
import json
import time
import re



import googlemaps
from pprint import pprint
import time
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

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash("Account already active, please log in.")

        return redirect ('/')

    elif email and name and password:
        user = crud.create_user(email, name, password)
        db.session.add(user)
        db.session.commit()
        flash("Account succesfully created.")

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
    
    if 'email' in session:
        user = crud.get_user_by_email(session['email'])
        name = user.name
        user_id = user.user_id

        list_user_conditions = crud.get_all_conditions_by_user_id(user_id)
        set_user_conditions = set(list_user_conditions)
        all_user_conditions = list(set_user_conditions)
        
        all_user_conditions = sorted(all_user_conditions, key=lambda x: x.condition.title)

        return render_template("profile.html", name=name, all_user_conditions=all_user_conditions)
    
    else:
        flash("You must login first.")
        return redirect('/')



@app.route("/conditions")
def all_conditions():
    """View all conditions."""

    if "email" in session:

        conditions = crud.get_conditions()
        return render_template("all_conditions.html", conditions=conditions)

    else:
        flash("You must login first.")
        return redirect('/')



@app.route('/conditions/search')
def search_conditions():
    """Search for conditions."""

    if 'email' in session:
        return render_template('condition_search.html')
    
    else:
        flash("You must login first.")
        return redirect('/')



@app.route('/conditions/results')
def get_results():
    """Return search results."""

    if 'email' in session:

        result = request.args.get("result")
        result = result.title()

        results = crud.get_search_results(result)

        if results:
            return render_template('results.html', results = results, result = result)
        
        else:
            flash("No matching results.")
            return redirect('/conditions/search')
    
    else:
        flash("You must login first")
        return redirect('/')
        


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

    comment_ids = request.json.get("comment_ids")
  
    for comment_id in comment_ids:
        comment = crud.get_comment_by_id(comment_id)

        if comment:
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

    #Clears user session on logout.
    session.clear()

    return redirect('/')


@app.route('/vitals')
def document_vitals():
    """User can input vitals."""

    #Check to see if user is logged in.
    if 'email' in session: 
        return render_template('vitals.html')
    
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

    #Create new set of vitals user entered.
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

        #Get user
        user = crud.get_user_by_email(session['email'])
        user_id = user.user_id
        name = user.name

        #Get all vitals by user id
        vitals = crud.get_vitals_by_user_id(user_id)

        return render_template("vitals_results.html", vitals=vitals, name=name)
    
    else:
        flash("You must login first.")
        return redirect('/')


@app.route('/vitals_graph')
def show_vital_graphs():
    """Shows graphs of vital signs."""

    #Check to see if user is logged in.
    if 'email' in session:
        return render_template('vitals_graph.html')
    
    else:
        flash("You must login first.")
        return redirect('/')



@app.route('/all_vitals_graph')
def get_all_vitals_for_graph():
    """Gets all vitals."""

    user = crud.get_user_by_email(session['email'])
    user_id = user.user_id

    #Get all vitals of user
    vitals = crud.get_vitals_by_user_id(user_id)

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
        return render_template('find_physician.html')
    
    else:
        flash("You must login first.")
        return redirect('/')



@app.route("/physician/search")
def get_physician_results():
    """Return results of physicians for user."""

    #Get zipcode user entered
    zipcode = request.args.get("zipcode")
    print(zipcode)

    regex_zipcode = "\d{5}"

    #List to hold all dictionary results of relevant data
    all_details = [] 

    if len(zipcode) == 5 and re.match(regex_zipcode, zipcode):

        #Get latitude/longitude from user zipcode
        location = crud.get_lat_long(zipcode, API_KEY)

        if location:

    
            #Get results of doctors nearby location
            data = crud.find_nearby_doctors(location, API_KEY)
           
            if data:

                #loop through each result
                for result in data['results']:

                    #Get each results place_id
                    place_id = result['place_id']

                    #Get more details on each result from nearby doctors
                    place_details = crud.get_place_details(place_id, API_KEY)

                    #Dictionary of relevant data from place_details
                    rel_details = {
                        'name': place_details['result']['name'],
                        'address': place_details['result']['formatted_address'],
                        'phone': place_details['result']['formatted_phone_number'],
                        'url': place_details['result']['url'],
                    }

                    #Add dictionary to all_details list
                    all_details.append(rel_details)
                    
                    
            pprint(all_details)   

            return render_template('physician_results.html', all_details=all_details)

      
                        
        else:
            flash("Please enter a valid zipcode.")
            return redirect('/findphysician')
     
    else:
        flash("Please enter a valid zipcode.")
        return redirect('/findphysician')

    
   




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

