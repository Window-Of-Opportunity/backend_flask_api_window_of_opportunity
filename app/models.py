from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Referenced this document to create relationships between tables
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html

class User(db.Model):
    __tablename__ = 'user'
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
    #type is for keeping track of the types of classes that inherit from this class
    type = db.Column(db.String(50))

# for inheritance to other classes in the ORM
    __mapper_args__ = {
            'polymorphic_identity': 'user',
            'with_polymorphic': '*',
            "polymorphic_on": type
        }

# sets a password using the hashing algo
    def set_password(self, password):
        """ Passwords can only be added as such and is hashed """
        self.password_hash = generate_password_hash(password)

# checks to see if a password provided matches the hash in the db
    def check_password(self, password):
        """ Returns hashed password if it is correct """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Customer(User):
    __tablename__ = 'customer'
    orders = db.relationship("Order", backref = "customer")
    cart = db.relationship("Cart", uselist=False, back_populates="customer")

# for inheriting from the User class
    __mapper_args__ = {
            'polymorphic_identity': 'customer',
            'with_polymorphic': '*'
        }

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Every customer is instantiated with a one to one relationship
        # with a cart in the database.
        self.cart = Cart(cust_id=self.id)
        db.session.add(self.cart)
        db.session.commit()
        
    def __repr__(self):
        return '<Customer {}>'.format(self.username)

class Sales_Rep(User):
    __tablename__ = 'sales_rep'
    ssn = db.Column(db.String(9))
    position = db.Column(db.String(64))
    hire_date = db.Column(db.DateTime)
    salary_type = db.Column(db.String(64))
    salary_amount = db.Column(db.String(16))

# for inheriting from the user class
    __mapper_args__ = {
            'polymorphic_identity': 'sales_rep',
            'with_polymorphic': '*'
        }

    def __repr__(self):
         return '<Sales_Rep {}>'.format(self.username)

class Mailing_Address(db.Model):
    __tablename__ = 'mailing_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
         return '<mailing_address {}>'.format(self.street_address_1)

class Billing_Address(db.Model):
    __tablename__ = 'billing_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
         return '<billing_address {}>'.format(self.street_address_1)

# referenced this document to create a simple customers and orders relationships tables.
#https://stackoverflow.com/questions/17711324/database-structure-for-customer-table-having-many-orders-per-customer-and-many/17711375

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_items = db.relationship("Order_Item")
    cust_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
         return '<order {}>'.format(self.id)
    
class Order_Item(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

    def __repr__(self):
         return '<order_item {}>'.format(self.id)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    order_items = db.relationship("Order_Item")
    #type is for keeping track of the types of classes that inherit from this class
    type = db.Column(db.String(50))
    
    __mapper_args__ = {
            'polymorphic_identity': 'product',
            'with_polymorphic': '*',
            "polymorphic_on": type
        }

    def __repr__(self):
         return '<product {}>'.format(self.name)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer = db.relationship("Customer", back_populates="cart")
    cart_items = db.relationship("Cart_Item")

    def __repr__(self):
         return '<cart{}>'.format(self.id)

class Cart_Item(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
         return '<cart_item{}>'.format(self.id)

class Window(Product):
    __tablename__ = 'window'
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

    # for inheriting from the User class
    __mapper_args__ = {
            'polymorphic_identity': 'window',
            'with_polymorphic': '*'
        }

    def __repr__(self):
         return '<window {}>'.format(self.name)
