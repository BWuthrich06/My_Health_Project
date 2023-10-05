from model import db, User, Condition, User_condition, connect_to_db
from datetime import datetime



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



def create_condition(title, all_synonyms, word_synonyms, url):
    """Create and return a condition."""

    condition = Condition(
        title = title,
        all_synonyms = all_synonyms,
        word_synonyms = word_synonyms,
        url = url,
    )
    return condition



def get_conditions():
    """Return all conditions."""

    return Condition.query.all()



def get_condition_by_id(condition_id):
    """Return condition by id."""

    return Condition.query.get(condition_id)



def get_search_results(result):
    """Return all results that match search."""

    title = Condition.query.filter(Condition.title.like(f"%{result}%")).all()
    all_synonyms = Condition.query.filter(Condition.all_synonyms.like(f"%{result}%")).all()

    results = title + all_synonyms
    set_results = set(results)
    all_results = list(set_results)
    
    
    return all_results





def create_user_condition(condition_id, user_id, title, date_added=datetime.now(), comments=None):
    """Create and return a user_condition."""

    new_user_condition = User_condition(
        condition_id = condition_id,
        user_id = user_id,
        title = Condition.title,
        date_added = date_added,
    )

    return new_user_condition

    
