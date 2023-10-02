"""Models for health conditions app"""

# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(100), unique = True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(50))



    def __repr__(self):
        return f"<User user_id = {self.user_id} email = {self.email} name = {self.name}>"