from app import app, db
from flask import request, jsonify, make_response
from functools import wraps
from app.models import User, Mailing_Address, Billing_Address


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
            current_user = User.query.filter_by(public_id = data['public_id']).first() 
        except: 
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
        
        
        {
        "User":
            {
                "username": "jeeeeffff",
                "email": "example@email.com",
                "password": "this_is_secret"
                "firstName": "Jason",
                "lastName": "Kyle",
                "middleName": "",
                "phoneNumber": "123456789",
                "gender": "F",
                "mairtalStatus": "Married"
            },
        "MailingAddress":
            {
                "streetAddress1": "first street"
                "streetAddress2": "continuation"
                "zipCode": "12345"
                "state": "CA"
                "country": "United States"
            }
        "BillingAddress":
            {
                "streetAddress1": "first street"
                "streetAddress2": "continuation"
                "zipCode": "12345"
                "state": "CA"
                "country": "United States"
            }
        }
    """
    # Converts json to python object
    req_data = request.get_json()

    # get email, name, password and username
    user = User.query.filter_by(email = req_data['User']['email']).first()

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
        
@app.route('/register', methods=['POST'])
def login():
    return jsonify("Work in progress")

        
    

    
