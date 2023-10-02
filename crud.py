from model import db, User, Condition, Favorite, connect_to_db


def create_user(email, name, password):
    """Create a new user."""

    user = User(email=email, name=name, password=password)

    return user


def create_condition(title, synonym, url):
    """Create and return a condition."""

    condition = Condition(
        title = title,
        synonyms = synonyms,
        url = url,
    )

    return condition



def get_conditions():
    """Return all conditions."""

    return Condition.query.all()



def get_condition_by_id(condition_id):
    """Return condition by id."""

    return Condition.query.get(condition_id)



def create_favorite(condition_id, user_id, date_added, comments=None):
    """Create and return a favorite."""

    favorite = Favorite(
        condition_id = condition_id,
        user_id = user_id,
        date_added = date_added,
    )

    return favorite

    
