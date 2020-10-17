from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    middle_name = db.Column(db.String(128))
    phone_number = db.Column(db.String(16))
    gender = db.Column(db.String(1))
    marital_status = (db.String(16))
    mailing_addresses = db.relationship("Mailing_Address", backref="owner")
    billing_addresses = db.relationship("Billing_Address", backref="owner")
    

    def set_password(self, password):
        """ Passwords can only be added as such and is hashed """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ Returns hashed password if it is correct """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Customer(User):
    windows = db.relationship("Window", backref = "customer")

    
    def __repr__(self):
        return '<Customer {}>'.format(self.username)

class Sales_Rep(User):
    ssn = db.Column(db.String(9))
    position = db.Column(db.String(64))
    hire_date = db.Column(db.DateTime)
    salary_type = db.Column(db.String(64))
    salary_amount = db.Column(db.String(16))

    def __repr__(self):
         return '<Sales_Rep {}>'.format(self.username)

class Mailing_Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
         return '<mailing_address {}>'.format(self.street_address_1)

class Billing_Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
         return '<billing_address {}>'.format(self.street_address_1)

class Window(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    window_type = db.Column(db.String(32))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    color = db.Column(db.String(32))
    manufacturer = db.Column(db.String(32))
    pane_width = db.Column(db.Integer)
    num_panes = db.Column(db.Integer)
    obscured = db.Column(db.Boolean)
    tempered = db.Column(db.Boolean)
    gas_fill_type = db.Column(db.String(16))
    lowe3 = db.Column(db.Boolean)
    frame_material = db.Column(db.String(64))
    nailing_flange = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
         return '<window {}>'.format(self.name)
