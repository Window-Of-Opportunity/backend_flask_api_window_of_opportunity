from app import db

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128))
    phone_number = db.Column(db.String(16))
    gender = db.Column(db.String(1))
    marital_status = (db.String(16))

    def __repr__(self):
        return '<User {}>'.format(self.username)
