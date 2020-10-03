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
    mailing_addresses = db.relationship("mailing_address", backref="user", lazy="dynamic")
    billing_addresses = db.relationship("billing_address", backref="user", lazy="dynamic")
    windows = db.relationship("window", backref="user", lazy="dynamic")

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Customer(User):
    
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

class mailing_address(db.Model):
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))

    def __repr__(self):
         return '<mailing_address {}>'.format(self.street_address)

class biiling_address(db.Model):
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))

    def __repr__(self):
         return '<billing_address {}>'.format(self.street_address)

class window(db.Model):
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

    def __repr__(self):
         return '<window {}>'.format(self.street_address)
