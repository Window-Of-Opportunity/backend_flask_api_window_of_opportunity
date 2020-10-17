from app import app, db
from flask import request, jsonify, make_response
from functools import wraps
from app.models import User, Mailing_Address, Billing_Address
import jwt
from datetime import datetime, timedelta 

def token_required(f):
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
            print(data)
            current_user = User.query.filter_by(id = data['id']).first()
            print(current_user)
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
@token_required
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)

@app.route('/register', methods=['POST'])
def register():
    """
        Takes a json object structured as so:
        
    """
    # Converts json to python object
    req_data = request.get_json()

    # get email, name, password and username
    user = User.query.filter_by(username = req_data['User']['username']).first()

    if not user:
        # DB ORM object
        user = User(
            username = req_data['User']['username'],
            email = req_data['User']['email'],
            first_name = req_data['User']['firstName'],
            last_name = req_data['User']['lastName'],
            middle_name = req_data['User']['middleName'],
            phone_number = req_data['User']['phoneNumber'],
            gender = req_data['User']['gender'],
            marital_status = req_data['User']['maritalStatus']
            )
        user.set_password(req_data['User']['password'])
        
        address = req_data['MailingAddress']
        mail = Mailing_Address(
                street_address_1 = address['streetAddress1'],
                street_address_2 = address['streetAddress2'],
                zip_code = address["zipCode"],
                state = address["state"],
                country = address["country"],
                owner=user
            )
        bill = Billing_Address(
                street_address_1 = address['streetAddress1'],
                street_address_2 = address['streetAddress2'],
                zip_code = address["zipCode"],
                state = address["state"],
                country = address["country"],
                owner=user
            )
        db.session.add(user)
        db.session.add(mail)
        db.session.add(bill)
        db.session.commit()
        return make_response('Successfully registered.', 201)
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
   
    user = User.query.filter_by(username = auth.get('username')).first() 
   
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
@token_required
def get_all_users(current_user): 
    # querying the database 
    # for all the entries in it 
    users = User.query.all() 
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

    
