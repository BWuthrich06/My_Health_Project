"""Models for health conditions app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(50))

    user_conditions = db.relationship("User_condition", back_populates="user")


    def __repr__(self):
        return f"<User user_id = {self.user_id} email = {self.email} name = {self.name}>"
    



class User_condition(db.Model):
    """A user condition"""

    __tablename__ = "user_conditions"

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    condition_id = db.Column(db.Integer, db.ForeignKey("conditions.condition_id"))
    date_added = db.Column(db.Date)
    comments = db.Column(db.Text, nullable = True)

    user = db.relationship("User", back_populates="user_conditions")
    condition = db.relationship("Condition", back_populates="user_conditions")


    def __repr__(self):
        return f"<Favorite favorite_id = {self.favorite_id} date_added = {self.date_added}>"
    


class Condition(db.Model):
    """A Condition"""

    __tablename__ = "conditions"

    condition_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    all_synonyms = db.Column(db.String(500))
    word_synonyms = db.Column(db.String(500))
    url = db.Column(db.String(300))

    user_conditions = db.relationship("User_condition", back_populates="condition")
    synonyms = db.relationship("Synonym", secondary="condition_synonyms", back_populates = "conditions")


    def __repr__(self):
        return f"<Condition condition_id = {self.condition_id} title = {self.title}>"
    

class Synonym(db.Model):
    """A Synonym."""

    __tablename__ = "synonyms"

    synonym_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    synonym = db.Column(db.String(200))

    conditions = db.relationship("Condition", secondary="condition_synonyms", back_populates = "synonyms")

    

class ConditionSynonyms(db.Model):
    """A Condition's Synonyms."""

    __tablename__ = "condition_synonyms"

    condition_synonym_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    condition_id = db.Column(db.Integer, db.ForeignKey("conditions.condition_id"))
    synonym_id = db.Column(db.Integer, db. ForeignKey("synonyms.synonym_id"))




    

def connect_to_db(flask_app, db_uri="postgresql:///conditions", echo= True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)


