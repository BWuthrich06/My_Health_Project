from model import db, User, Condition, User_condition, Comment, Vital, Physician, connect_to_db
from datetime import date
from datetime import datetime
import time

import requests
import pprint
import os
import json


API_KEY = os.environ.get('my_api_key')



def create_user(email, name, password):
    """Create a new user."""

    user = User(email=email, name=name, password=password)

    return user



def get_user_by_id(user_id):
    """Returns user by id."""

    return User.query.get(user_id)



def get_user_by_email(email):
    """Returns user by email."""

    return User.query.filter(User.email == email).first()



def get_space_between_synonyms(synonyms):
    """Remove space between synonyms."""
    spaced_comma_synonyms = []

    for synonym in synonyms:
        list_synonyms = synonym.split(',')

        spaced_words = []
        for synonym in list_synonyms:
            synonym = synonym.strip()
            spaced_words.append(synonym)

        synonym = ', '.join(spaced_words)
        spaced_comma_synonyms.append(synonym)
        
    return spaced_comma_synonyms



def create_condition(title, all_synonyms, url):
    """Create and return a condition."""

    condition = Condition(
        title = title,
        all_synonyms = all_synonyms,
        url = url,
    )
    return condition



def get_conditions():
    """Return all conditions."""

    return Condition.query.all()



def get_comment_by_id(comment_id):
    """Return comment by id."""

    return Comment.query.get(comment_id)



def get_condition_by_id(condition_id):
    """Return condition by id."""

    return Condition.query.get(condition_id)



def get_all_conditions_by_user_id(user_id):
    """Return all conditions of user."""

    user = User.query.get(user_id)

    return user.user_conditions



def get_search_results(result):
    """Return all results that match search."""

    title = Condition.query.filter(Condition.title.like(f"%{result}%")).all()
    all_synonyms = Condition.query.filter(Condition.all_synonyms.like(f"%{result}%")).all()
    print(all_synonyms)

    results = title + all_synonyms
    set_results = set(results)
    all_results = list(set_results)

    all_results = sorted(all_results, key=lambda x: x.title)
    
    return all_results



def create_user_condition(condition_id, user_id):
    """Create and return a user_condition."""

    new_user_condition = User_condition(
        condition_id = condition_id,
        user_id = user_id,
        date_added = date.today(),
    )

    return new_user_condition



def create_comment(favorite_id, formInput):
    """Create a new comment."""

    new_comment = Comment(comment=formInput, favorite_id=favorite_id)

    return new_comment
    
    

def delete_user_condition(favorite_id):
    """Delete user condition."""

    user_condition = User_condition.query.get(favorite_id)

    return user_condition
   
   

def get_vitals_by_user_id(user_id):
    """Get vitals by user."""

    vitals = Vital.query.filter_by(user_id=user_id).all()

    return vitals



def create_vital(user_id, systolic=None, diastolic=None, heart_rate=None, oxygen=None, weight=None, glucose=None):
    "Create and return a new set of vitals."

    new_vital = Vital(
        user_id = user_id,
        date_time = datetime.now(),
        systolic = systolic,
        diastolic = diastolic,
        heart_rate = heart_rate,
        oxygen = oxygen,
        weight = weight,
        glucose = glucose
        )

    return new_vital


def get_physicians_by_user_id(user_id):
    """Returns physicians for user."""

    user = User.query.get(user_id)

    return user.physicians

def create_physician(place_id, name, address, phone, url, user_id):
    """Create and return a user physician."""

    physician = Physician(
        place_id = place_id,
        name = name,
        address = address,
        phone = phone,
        url = url,
        user_id = user_id
    )

    return physician


def delete_physician(physician_id):
    """Delete user physician."""

    physician = Physician.query.get(physician_id)

    return physician


def get_recent_vital(user_id):
    """Return user's most recent vitals."""

    vital = Vital.query.filter_by(user_id=user_id).order_by(Vital.date_time.desc()).first()

    return vital








    
