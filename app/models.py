from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Referenced this document to create relationships between tables
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html

##class User(db.Model):
##    __tablename__ = 'user'
##    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
##    username = db.Column(db.String(64), index=True, unique=True)
##    email = db.Column(db.String(120), index=True, unique=True)
##    password_hash = db.Column(db.String(128))
##    first_name = db.Column(db.String(128))
##    last_name = db.Column(db.String(128))
##    middle_name = db.Column(db.String(128))
##    phone_number = db.Column(db.String(16))
##    gender = db.Column(db.String(1))
##    marital_status = (db.String(16))
##    mailing_addresses = db.relationship("Mailing_Address", backref="owner")
##    billing_addresses = db.relationship("Billing_Address", backref="owner")
##    #type is for keeping track of the types of classes that inherit from this class
##    type = db.Column(db.String(50))
##
### for inheritance to other classes in the ORM
##    __mapper_args__ = {
##            'polymorphic_identity': 'user',
##            'with_polymorphic': '*',
##            "polymorphic_on": type
##        }

### sets a password using the hashing algo
##    def set_password(self, password):
##        """ Passwords can only be added as such and is hashed """
##        self.password_hash = generate_password_hash(password)
##
### checks to see if a password provided matches the hash in the db
##    def check_password(self, password):
##        """ Returns hashed password if it is correct """
##        return check_password_hash(self.password_hash, password)
##
##    def __repr__(self):
##        return '<User {}>'.format(self.username)

class Customer(db.Model):
    __tablename__ = 'customer'
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
    mailing_addresses = db.relationship("Mailing_Address", backref="customer")
    billing_addresses = db.relationship("Billing_Address", backref="customer")
    #type is for keeping track of the types of classes that inherit from this class
    type = db.Column(db.String(50))
    orders = db.relationship("Order", backref = "customer")
    cart = db.relationship("Cart", uselist=False, back_populates="customer")

    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)
        # Every customer is instantiated with a one to one relationship
        # with a cart in the database.
        self.cart = Cart(cust_id=self.id)
        db.session.add(self.cart)
        db.session.commit()


        
    def __repr__(self):
        return '<Customer {}>'.format(self.username)

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['username'] = self.username
        attributes['email'] = self.email
        attributes['first_name'] = self.first_name
        attributes['middle_name'] = self.middle_name
        attributes['last_name'] = self.last_name
        attributes['phone_number'] = self.phone_number
        attributes['gender'] = self.gender
        attributes['marital_status'] = self.marital_status
        attributes['mailing_addresses'] = [mailing_address.id for mailing_address in self.mailing_addresses]
        attributes['billing_addresses'] = [billing_address.id for billing_address in self.billing_addresses]
        attributes['type'] = self.type
        attributes['orders'] = [order.id for order in self.orders]
        attributes['cart'] = self.ssn


    # sets a password using the hashing algo
    def set_password(self, password):
        """ Passwords can only be added as such and is hashed """
        self.password_hash = generate_password_hash(password)

    # checks to see if a password provided matches the hash in the db
    def check_password(self, password):
        """ Returns hashed password if it is correct """
        return check_password_hash(self.password_hash, password)


class Employee(db.Model):
    __tablename__='employee'
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
    mailing_addresses = db.relationship("Mailing_Address", backref="employee")
    billing_addresses = db.relationship("Billing_Address", backref="employee")
    #type is for keeping track of the types of classes that inherit from this class
    type = db.Column(db.String(50))
    employee_id = db.Column(db.Integer)
    ssn = db.Column(db.Integer)
    hire_date = db.Column(db.DateTime)
    end_employment_date = db.Column(db.DateTime)
    salary_type = db.Column(db.String(50))
    salary_amount = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id')) # need to make employee to order one to many
    order = db.relationship("Order", back_populates="sales_rep")

    # sets a password using the hashing algo
    def set_password(self, password):
        """ Passwords can only be added as such and is hashed """
        self.password_hash = generate_password_hash(password)

    # checks to see if a password provided matches the hash in the db
    def check_password(self, password):
        """ Returns hashed password if it is correct """
        return check_password_hash(self.password_hash, password)

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['username'] = self.username
        attributes['email'] = self.email
        attributes['first_name'] = self.first_name
        attributes['middle_name'] = self.middle_name
        attributes['last_name'] = self.last_name
        attributes['phone_number'] = self.phone_number
        attributes['gender'] = self.gender
        attributes['marital_status'] = self.marital_status
        attributes['mailing_addresses'] = [mailing_address.id for mailing_address in self.mailing_addresses]
        attributes['billing_addresses'] = [billing_address.id for billing_address in self.billing_addresses]
        attributes['type'] = self.type
        attributes['employee_id'] = self.employee_id
        attributes['ssn'] = self.ssn
        attributes['hire_date'] = self.hire_date
        attributes['end_employment_date'] = self.end_employment_date
        attributes['salary_type'] = self.salary_type
        attributes['salary_amount'] = self.salary_amount
        attributes['order_id'] = self.order_id
        
        return attributes

##class Sales_Rep(User):
##    __tablename__ = 'sales_rep'
##    ssn = db.Column(db.String(9))
##    position = db.Column(db.String(64))
##    hire_date = db.Column(db.DateTime)
##    salary_type = db.Column(db.String(64))
##    salary_amount = db.Column(db.String(16))
##
### for inheriting from the user class
##    __mapper_args__ = {
##            'polymorphic_identity': 'sales_rep',
##            'with_polymorphic': '*'
##        }

    def __repr__(self):
         return '<Sales_Rep {}>'.format(self.username)

class Mailing_Address(db.Model):
    __tablename__ = 'mailing_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    city = db.Column(db.String(32))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['street_address_1'] = self.street_address_1
        attributes['street_address_2'] = self.street_address_2
        attributes['zip_code'] = self.zip_code
        attributes['city'] = self.city
        attributes['state'] = self.state
        attributes['country'] = self.country
        attributes['customer_id'] = self.customer_id
        attributes['employee_id'] = self.employee_id
        
        return attributes

    def __repr__(self):
         return '<mailing_address {}>'.format(self.street_address_1)

class Billing_Address(db.Model):
    __tablename__ = 'billing_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    city = db.Column(db.String(32))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['street_address_1'] = self.street_address_1
        attributes['street_address_2'] = self.street_address_2
        attributes['zip_code'] = self.zip_code
        attributes['city'] = self.city
        attributes['state'] = self.state
        attributes['country'] = self.country
        attributes['order_id'] = self.order_id
        attributes['customer_id'] = self.customer_id
        attributes['employee_id'] = self.employee_id
        return attributes

    def __repr__(self):
         return '<billing_address {}>'.format(self.street_address_1)

# referenced this document to create a simple customers and orders relationships tables.
#https://stackoverflow.com/questions/17711324/database-structure-for-customer-table-having-many-orders-per-customer-and-many/17711375

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_items = db.relationship("Order_Item")
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'))      
    payment_plan = db.relationship("Payment_Plan", uselist=False, back_populates="order")
    sales_rep = db.relationship("Employee", uselist=False, back_populates="order")
    jobsite_address = db.relationship("Jobsite_Address", uselist=False, back_populates="order")
    agreement = db.relationship("Agreement", uselist=False, back_populates="order")
    transactions = db.relationship("Transaction", backref = "order")

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['order_items'] = self.order_items
        attributes['cust_id'] = self.cust_id
        attributes['transactions'] = self.transactions
        attributes['agreement'] = self.agreement.get_attributes() if self.agreement != None else self.agreement
        attributes['payment_plan'] = self.payment_plan.get_attributes() if self.payment_plan != None else self.payment_plan
        #attributes['sales_rep'] = self.sales_rep.get_attributes()
        attributes['jobsite_address'] = self.jobsite_address.get_attributes() if self.jobsite_address != None else self.jobsite_address
        
        return attributes

    def __repr__(self):
         return '<order {}>'.format(self.id)

class Jobsite_Address(db.Model):
    __tablename__ = 'jobsite_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_address_1 = db.Column(db.String(32))
    street_address_2 = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    city = db.Column(db.String(32))
    state = db.Column(db.String(2))
    country = db.Column(db.String(32))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order", back_populates="jobsite_address")
    

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['street_address_1'] = self.street_address_1
        attributes['street_address_2'] = self.street_address_2
        attributes['zip_code'] = self.zip_code
        attributes['city'] = self.city
        attributes['state'] = self.state
        attributes['country'] = self.country
        attributes['order_id'] = self.order_id
        return attributes
    
class Order_Item(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['order_id'] = self.order_id
        attributes['cust_id'] = self.cust_id
        attributes['quantity'] = self.quantity
        return attributes

    def __repr__(self):
         return '<order_item {}>'.format(self.id)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    order_items = db.relationship("Order_Item")
    cart_items = db.relationship("Cart_Item")
    #type is for keeping track of the types of classes that inherit from this class
    type = db.Column(db.String(50))
    window = db.relationship("Window", uselist=False, back_populates="product")

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        #attributes['order_items'] = self.order_items
        #attributes['cart_items'] = self.cart_items
        attributes['type'] = self.type
        #attributes['window'] = self.window.get_attributes()
        return attributes

    def __repr__(self):
         return '<product {}>'.format(self.name)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer", back_populates="cart")
    cart_items = db.relationship("Cart_Item")

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['cust_id'] = self.cust_id
        #attributes['cart_items'] = self.cart_items
        return attributes

    def __repr__(self):
         return '<cart{}>'.format(self.id)

class Cart_Item(db.Model):
    __tablename__ = 'cart_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['order_id'] = self.order_id
        attributes['cust_id'] = self.cust_id
        attributes['quantity'] = self.quantity
        return attributes

    def __repr__(self):
         return '<cart_item{}>'.format(self.id)

class Window(db.Model):
    __tablename__ = 'window'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product", back_populates="window")

    def __repr__(self):
         return '<window {}>'.format(self.id)

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['window_type'] = self.window_type
        attributes['width'] = self.width
        attributes['height'] = self.height
        attributes['color'] = self.color
        attributes['manufacturer'] = self.manufacturer
        attributes['pane_width'] = self.pane_width
        attributes['num_panes'] = self.num_panes
        attributes['obscured'] = self.obscured
        attributes['tempered'] = self.tempered
        attributes['gas_fill_type'] = self.gas_fill_type
        attributes['lowe3'] = self.lowe3
        attributes['frame_material'] = self.frame_material
        attributes['nailing_flang'] = self.nailing_flange
        return attributes
        

class Transaction(db.Model):
    __tablename__="transaction"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    #payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_type.id'))

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['amount'] = self.amount
        attributes['date'] = self.date
        attributes['order_id'] = self.order_id
        return attributes

class Agreement(db.Model):
    __tablename__="agreement"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document = db.Column(db.LargeBinary)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order", back_populates="agreement")

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        #attributes['document'] = self.document
        attributes['order_id'] = self.order_id
        return attributes

class Payment_Plan(db.Model):
    __tablename__='payment_plan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number_of_transactions_left = db.Column(db.Integer)
    amount_per_transaction = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    frequency = db.Column(db.VARCHAR)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order", back_populates="payment_plan")

    def get_attributes(self):
        attributes = {}
        attributes['id'] = self.id
        attributes['number_of_transactions'] = self.number_of_transactions
        attributes['amount_per_transaction'] = self.amount_per_transaction
        attributes['start_date'] = self.start_date
        attributes['frequency'] = self.frequency
        attributes['order_id'] = self.order_id
        return attributes

