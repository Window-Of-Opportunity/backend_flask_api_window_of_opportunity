from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Customer, Sales_Rep, Mailing_Address, Billing_Address, Order, Order_Item, Product, Window, Cart, Cart_Item
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


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

class CustomerModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_customer_orders_relationship(self):
        cust = Customer(
                    username = "testy",
                    email = "testy@gmail.com",
                    first_name = "first_test",
                    last_name = "last_test",
                    middle_name = "middle_test",
                    phone_number = "123456789",
                    gender = "M",
                    marital_status = "Married"
                    )
        cust.set_password('test_pass')

        order = Order()
        order2 = Order()
        order3 = Order()

        order_item = Order_Item(quantity=5)
        order_item2 = Order_Item(quantity=10)
        order_item3 = Order_Item(quantity=15)
        
        product = Product(name="Spatula")
        product2 = Product(name="Spoon")
        product3 = Product(name="Spork")

        cust.orders.append(order)
        order.order_items.append(order_item)
        product.order_items.append(order_item)

        db.session.add(cust)
        db.session.add(order)
        db.session.add(product)
        db.session.add(order_item)
        db.session.commit()

##        print(Customer.query.all())
##        print(Order.query.all())
##        print(product.query.all())
##        print(Order_Item.query.all())
##
##        print("Order Items")
##        for ot in Order_Item.query.all():
##            print(ot.product_id)
##            print(ot.order_id)
##
##        print("Customers: ")
##        for c in Customer.query.all():
##            print(c)
##            for o in c.orders:
##                print(o)
##                for ot in o.order_items:
##                    print(ot)

    def test_customer_cart_relationship(self):
        cust = Customer(
                    username = "testy",
                    email = "testy@gmail.com",
                    first_name = "first_test",
                    last_name = "last_test",
                    middle_name = "middle_test",
                    phone_number = "123456789",
                    gender = "M",
                    marital_status = "Married"
                    )
        db.session.add(cust)
        db.session.commit()
        print(Cart.query.all())
        print(cust.cart)
        

    

    
if __name__ == '__main__':
    unittest.main(verbosity=2)
