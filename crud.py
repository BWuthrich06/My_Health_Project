from model import db, User, Condition, User_condition, connect_to_db



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



# def create_favorite(condition_id, user_id, title, date_added, comments=None):
#     """Create and return a favorite."""

#     favorite = Favorite(
#         condition_id = Condition.condition_id,
#         user_id = User.user_id,
#         title = Condition.title,
#         date_added = date_added,
#     )

#     return favorite

    
