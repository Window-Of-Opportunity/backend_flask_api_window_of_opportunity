from app import app, db
from flask import request, jsonify, make_response
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
    )
from functools import wraps
from app.models import (
    Mailing_Address, Billing_Address,
    Customer, Order, Product, Window,
    Cart, Cart_Item, Jobsite_Address
)

from flask_cors import cross_origin

from datetime import datetime, timedelta
   
@app.route('/')
@app.route('/index')
def index():
    return {"Welcome to BackWoop API": "The centralized api for window of opportunity!"}, 200

@app.route('/register_customer', methods=['POST'])
@cross_origin()
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
                first_name = req_data.get('Customer').get('firstName'),
                last_name = req_data.get('Customer').get('lastName'),
                middle_name = req_data.get('Customer').get('middleName'),
                phone_number = req_data.get('Customer').get('phoneNumber'),
                gender = req_data.get('Customer').get('gender'),
                marital_status = req_data.get('Customer').get('maritalStatus')
                )
            user.set_password(req_data['Customer']['password'])

            if req_data.get('MailingAddress'):
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
                db.session.add(mail)
                db.session.add(bill)
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'Successfully registered.'}), 201
        except KeyError as e:
            print(e)
            return jsonify({'message':"No attribute %s exists" % e}) , 400
        except Exception as e:
            print(e)
            return jsonify({'message':"Error, could not register user: %s" % e}), 400
    else:
        return jsonify({'message':'User already exists. Please Log in.'}), 202
        
@app.route('/login', methods=['POST'])
@cross_origin()
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
        ret = {
            'access_token': create_access_token(identity=auth.get('username')),
            'refresh_token': create_refresh_token(identity=auth.get('username'))
            }
   
        return make_response(jsonify(ret), 201) 
    # returns 403 if password is wrong 
    return make_response( 
        'Could not verify', 
        403, 
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'} 
    )

# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
@cross_origin()
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

# User Database Route 
# this route sends back list of users users 
@app.route('/user', methods =['GET'])
@cross_origin()
@jwt_required
def get_all_customers():
    current_user = Customer.query.filter_by(username = get_jwt_identity()).first()
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
   
    return {'users': output}, 200 

@app.route('/add_windows_to_cart', methods=['POST'])
@jwt_required
@cross_origin()
def add_windows():
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
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()
    # Converts json to python object
    data = request.get_json()

    try:
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
        return {"message": 'Successfully added windows to shopping cart.',
                "windows_added": True}, 201
    except KeyError as e:
        return {"message": "No attribute %s exists" % e,
                "windows_added": False}, 400
    except Exception as e:
        return {"message": "Error, could not register user: %s" % e,
                "windows_added": False}, 400
        
    


@app.route('/get_items_from_cart', methods=['GET'])
@jwt_required
@cross_origin()
def get_items_from_cart():
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()
    
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
    
    return products, 200

@app.route('/cart_item/<cart_id>', methods=['GET','DELETE'])
@jwt_required
@cross_origin()
def cart_item(cart_id):
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()

    try:
        cart_item = current_cust.cart.cart_items[int(cart_id)]
    except Exception as e:
        return jsonify({"message": "Error, could not find cart item: %s" %e}), 400

    if request.method == 'GET':
        return jsonify(cart_item.get_attributes()), 200
    elif request.method == 'DELETE':
        Cart_Item.query.filter_by(id=cart_item.cart_id).delete()
        db.session.commit()
        return jsonify({"message":"Cart item successfully deleted."}, 200)

@app.route('/product/<product_id>', methods=['GET', 'DELETE'])
@jwt_required
@cross_origin()
def product(product_id):
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()

    try:
        prod = Product.query.filter_by(id = int(product_id)).first()
    except Exception as e:
        return jsonify({"message": "Error, could not find product: %s" %e}), 400

    if request.method == 'GET':
        return jsonify(prod.get_attributes()), 200
    elif request.method == 'DELETE':
        Product.query.filter_by(id=prod.id).delete()
        db.session.commit()
        return jsonify({"message":"Product successfully deleted."}, 200)

@app.route('/product', methods=['POST'])
@jwt_required
@cross_origin()
def product_post():
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()

    return "Works", 200

@app.route('/cart', methods=['GET'])
@jwt_required
@cross_origin()
def cart():
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()

    try:
        crt = current_cust.cart
    except Exception as e:
        return jsonify({"message": "Error, could not find cart: %s" %e}), 400

    if request.method == 'GET':
        return jsonify(crt.get_attributes()), 200

@app.route('/window/<window_id>', methods=['GET', 'DELETE'])
@jwt_required
@cross_origin()
def window(window_id):
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()

    try:
        wind = Window.query.filter_by(id = int(window_id)).first()
    except Exception as e:
        return jsonify({"message": "Error, could not find window: %s" %e}), 400

    if request.method == 'GET':
        return jsonify(wind.get_attributes()), 200
    elif request.method == 'DELETE':
        Product.query.filter_by(id=wind.id).delete()
        db.session.commit()
        return jsonify({"message":"Window successfully deleted."}, 200)


@app.route('/create_new_order', methods=['POST'])
@jwt_required
@cross_origin()
def create_new_order():
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()
    data = request.get_json()

    try:
        jobsite_address_data = data["jobsite_address"]
    except KeyError as e:
        return make_response("No attribute %s exists" % e, 400)
    
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
    order.jobsite_address = jobsite_address
    db.session.commit()

    return order.get_attributes()


@app.route('/get_customer_orders', methods=['GET'])
@jwt_required
@cross_origin()
def get_customer_orders():
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()
    orders = {}

    for order in current_cust.orders:
        orders[order.id] = order.get_attributes()

    return orders, 200

    
        

@app.route('/get_agreement_info', methods=['GET'])
@jwt_required
@cross_origin()
def get_agreement_info():
    """
        Should pass the order id to this api path
    """
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()
    data = request.get_json()

    order_id = data["order_id"]

    order = Order.get(order_id)

@app.route('/get_selected_window', methods=['GET'])
@jwt_required
@cross_origin()
def get_selected_window():
    current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()

    elem = current_cust.cart.selected_cart_item_id
    cart_item = current_cust.cart.cart_items[elem]
    wind = Window.query.filter_by(product_id=cart_item.product_id).first()

    return jsonify(wind.get_attributes(), 200)

@app.route('/select_cart_item', methods=['POST'])
@jwt_required
@cross_origin()
def select_cart_item():
    try:
        current_cust = Customer.query.filter_by(username = get_jwt_identity()).first()
        data = request.get_json()
        cart_item_id = data['cart_id']
        current_cust.cart.cart_items[cart_item_id] # check to see if this is a valid element in the list of cart items.
    
        current_cust.cart.selected_cart_item_id = cart_item_id
        db.session.commit()
        return jsonify({"message":"Successfully selected window."}), 200
    except IndexError as e:
        print(e)
        return jsonify({"message":"Index Incorrect %s" % e}), 404
    except Exception as e:
        print(e)
        return jsonify({'message':"Unexpected Error: %s" % e}), 400        
        
    
    
    

        


    
