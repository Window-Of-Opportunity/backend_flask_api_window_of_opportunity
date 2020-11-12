from app import app, db
from flask import request, jsonify, make_response
from functools import wraps
from app.models import Mailing_Address, Billing_Address, Customer, Order, Product, Window, Cart, Cart_Item, Jobsite_Address
import jwt
from datetime import datetime, timedelta 

# Referenced this document to setup jwt token authentication
#https://www.geeksforgeeks.org/using-jwt-for-user-authentication-in-flask/


def customer_token_required(f):
    @wraps(f) 
    def decorated(*args, **kwargs): 
        token = None
        # jwt is passed in the request header 
        if 'x-access-token' in request.headers: 
            token = request.headers['x-access-token'] 
        # return 401 if token is not passed 
        if not token: 
            return jsonify({'message' : 'Token is missing !!'}), 401
   
        try: 
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = Customer.query.filter_by(id = data['id']).first()
        except Exception as e:
            print(e)
            return jsonify({ 
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes 
        return  f(current_user, *args, **kwargs)
   
    return decorated 
   
@app.route('/')
@app.route('/index')
@customer_token_required
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/register_customer', methods=['POST'])
def register_customer():
    """
        Takes a json object structured as so:
        
    """
    # Converts json to python object
    req_data = request.get_json()

    # get email, name, password and username
    user = Customer.query.filter_by(username = req_data['Customer']['username']).first()

    if not user:
        try:
            # DB ORM object
            user = Customer(
                username = req_data['Customer']['username'],
                email = req_data['Customer']['email'],
                first_name = req_data['Customer']['firstName'],
                last_name = req_data['Customer']['lastName'],
                middle_name = req_data['Customer']['middleName'],
                phone_number = req_data['Customer']['phoneNumber'],
                gender = req_data['Customer']['gender'],
                marital_status = req_data['Customer']['maritalStatus']
                )
            user.set_password(req_data['Customer']['password'])
            
            address = req_data['MailingAddress']
            mail = Mailing_Address(
                    street_address_1 = address['streetAddress1'],
                    street_address_2 = address['streetAddress2'],
                    zip_code = address["zipCode"],
                    state = address["state"],
                    country = address["country"],
                    customer=user
                )
            bill = Billing_Address(
                    street_address_1 = address['streetAddress1'],
                    street_address_2 = address['streetAddress2'],
                    zip_code = address["zipCode"],
                    state = address["state"],
                    country = address["country"],
                    customer=user
                )
            db.session.add(user)
            db.session.add(mail)
            db.session.add(bill)
            db.session.commit()
            return make_response('Successfully registered.', 201)
        except KeyError as e:
            return make_response("No attribute %s exists" % e, 400)
        except Exception as e:
            return make_response("Error, could not register user: %s" % e, 400)
    else:
        return make_response('User already exists. Please Log in.', 202) 
        
@app.route('/login', methods=['POST'])
def login():
    """
    Logs a user in with username and password

    """
    # Converts json to python object
    auth = request.get_json()

    if not auth or not auth.get('username') or not auth.get('password'):
        # returns 401 if any email or / and password is missing 
        return make_response( 
            'Could not verify', 
            401, 
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'} 
        ) 
   
    user = Customer.query.filter_by(username = auth.get('username')).first() 
   
    if not user: 
        # returns 401 if user does not exist 
        return make_response( 
            'Could not verify', 
            401, 
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'} 
        ) 
   
    if user.check_password(auth.get('password')): 
        # generates the JWT Token 
        token = jwt.encode({ 
            'id': user.id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30) 
        }, app.config['SECRET_KEY']) 
   
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201) 
    # returns 403 if password is wrong 
    return make_response( 
        'Could not verify', 
        403, 
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'} 
    )

# User Database Route 
# this route sends back list of users users 
@app.route('/user', methods =['GET']) 
@customer_token_required
def get_all_customers(current_user): 
    # querying the database 
    # for all the entries in it
    users = Customer.query.all() 
    # converting the query objects 
    # to list of jsons 
    output = [] 
    for user in users: 
        # appending the user data json  
        # to the response list 
        output.append({ 
            'public_id': user.id, 
            'username' : user.username, 
            'email' : user.email 
        }) 
   
    return jsonify({'users': output}) 

@app.route('/add_windows_to_cart', methods=['POST'])
@customer_token_required
def add_windows(current_cust):
    """
    Takes a json object required as such:

    {
        "Windows" : {
        {
            "window_name" :
            }
                "type": "window_type",
                "width": 5,
                "height": 5,
                "color": "white",
                "manufacturer" : "Marvin"
           }
    }

    """
    # Converts json to python object
    data = request.get_json()

    for window in data["Windows"]:
        prod = Product(
                name = window,
                type = "window"
            )
        wind = Window(
                window_type = data["Windows"][window]["type"],
                width = data["Windows"][window]["width"],
                height = data["Windows"][window]["height"],
                color = data["Windows"][window]["color"],
                manufacturer = data["Windows"][window]["manufacturer"]
                )
        db.session.add(wind)
        db.session.add(prod)
        cartItem = Cart_Item(cart_id=current_cust.cart.id, product_id=prod.id)
        prod.window = wind
        db.session.add(prod)
        db.session.add(cartItem)
        current_cust.cart.cart_items.append(cartItem)
        
        
    db.session.commit()

    return make_response('Successfully added windows to shopping cart.', 201)


@app.route('/get_items_from_cart', methods=['GET'])
@customer_token_required
def get_items_from_cart(current_cust):
    products = {}
    
    for item in current_cust.cart.cart_items:
        
        prod = Product.query.get(item.product_id)
        if prod != None:
            products[item.id] = {}
            products[item.id]["product_id"] = prod.id
            products[item.id]["name"] = prod.name
            products[item.id]["type"] = prod.type
            if prod.type == "window" and prod.window != None:
                print(prod.window)
                products[item.id]["product"] = prod.window.get_attributes()
    
    return jsonify(products)



@app.route('/create_new_order', methods=['GET'])
@customer_token_required
def create_customer_order(current_cust):

    data = request.get_json()

    jobsite_address_data = data["jobsite_address"]

    order = Order(cust_id=current_cust.id)
    db.session.add(order)

    jobsite_address = Jobsite_Address(street_address_1=jobsite_address_data['street_address_1'],
                                      street_address_2=jobsite_address_data['street_address_2'],
                                      zip_code=jobsite_address_data['zip_code'],
                                      city=jobsite_address_data['city'],
                                      state=jobsite_address_data['state'],
                                      country=jobsite_address_data['country'],
                                      order_id=order.id)
    db.session.add(jobsite_address)
    db.session.commit()

    return jsonify(order.get_attributes())


@app.route('/get_customer_orders', methods=['GET'])
@customer_token_required
def get_customer_orders(current_cust):
    orders = {}

    for order in current_cust.orders:
        orders[order.id] = order.get_attributes()

    return jsonify(orders)

    
        

@app.route('/get_agreement_info', methods=['GET'])
@customer_token_required
def get_agreement_info(current_cust):
    """
        Should pass the order id to this api path
    """
    data = request.get_json()

    order_id = data["order_id"]

    order = Order.get(order_id)
    
    
        
        
    
    

        


    
