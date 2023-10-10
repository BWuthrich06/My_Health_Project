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

    user = db.relationship("User", back_populates="user_conditions")
    condition = db.relationship("Condition", back_populates="user_conditions")
    comments = db.relationship("Comment", back_populates="user_condition")

    def __repr__(self):
        return f"<Favorite favorite_id = {self.favorite_id} date_added = {self.date_added}>"
    

    
class Comment(db.Model):
    """A Comment."""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text)
    favorite_id = db.Column(db.Integer, db.ForeignKey("user_conditions.favorite_id"))

    user_condition = db.relationship("User_condition", back_populates="comments")

    def __repr__(self):
        return f"<Comment comment_id = {self.comment_id} comment = {self.comment}>"
    
    

class Condition(db.Model):
    """A Condition"""

    __tablename__ = "conditions"

    condition_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    all_synonyms = db.Column(db.String(800))
    word_synonyms = db.Column(db.String(500))
    url = db.Column(db.String(500))

    user_conditions = db.relationship("User_condition", back_populates="condition")

    def __repr__(self):
        return f"<Condition condition_id = {self.condition_id} title = {self.title}>"
    

    

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


