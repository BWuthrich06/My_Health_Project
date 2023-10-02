"""Models for health conditions app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(100), unique = True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(150))

    favorites = db.relationship("Favorites", back_populates = "user")


    def __repr__(self):
        return f"<User user_id = {self.user_id} email = {self.email} name = {self.name}>"
    


class Condition(db.Model):
    """A Condition"""

    __tablename__ = "conditions"

    condition_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(150))
    synonyms = db.Column(db.Text)
    url = db.Column(db.String(300))

    favorites = db.relationship("Favorites", back_populates = "condition")


    def __repr__(self):
        return f"<Condition condition_id = {self.condition_id} title = {self.title}>"
    


class Favorite(db.Model):
    """A favorite"""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    condition_id = db.Column(db.Integer, db.ForeignKey("conditions.condition_id"))
    date_added = db.Column(db.Datetime)
    comments = db.Column(db.Text)

    user = db.relationship("User", back_populates = "favorites")
    condition = db.relationship("Condition", back_populates = "favorites")


    def __repr__(self):
        return f"<Favorite favorite_id = {self.favorite_id} date_added = {self.date_added}>"
    

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


