from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Mailing_Address, Billing_Address

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_register_user(self):
        u1 = User(username='')

if __name__ == '__main__':
    unittest.main(verbosity=2)
