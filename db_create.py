from app import db
from app.models import (Customer, Employee,
                        Mailing_Address, Billing_Address,
                        Order, Order_Item, Product, Window,
                        Cart, Cart_Item)
try:
    db.create_all()
except Exception as e:
    print(e)
    
cust = Customer(username = "test",
                    email = "test@gmail.com",
                    first_name = "first_test",
                    last_name = "last_test",
                    middle_name = "middle_test",
                    phone_number = "123456789",
                    gender = "M",
                    marital_status = "Married")
cust.set_password('test_pass')

prod1 = Product(
                    name = "test_window_wide",
                    type = "window"
                )
prod2 = Product(
                    name = "test_window_square",
                    type = "window"
                )
prod3 = Product(
                    name = "test_window_tall",
                    type = "window"
                )

wind1 = Window(
                    window_type = "singlehung",
                    width = 25,
                    height = 10,
                    color = "white",
                    manufacturer = "Amerimax"
                    )
wind2 = Window(
                    window_type = "singlehung",
                    width = 25,
                    height = 25,
                    color = "white",
                    manufacturer = "Amerimax"
                    )
wind3 = Window(
                    window_type = "singlehung",
                    width = 25,
                    height = 50,
                    color = "white",
                    manufacturer = "Amerimax"
                    )


db.session.add(wind1)
db.session.add(wind2)
db.session.add(wind3)

db.session.add(prod1)
db.session.add(prod2)
db.session.add(prod3)

cartItem1 = Cart_Item(cart_id=cust.cart.id, product_id=prod1.id)
cartItem2 = Cart_Item(cart_id=cust.cart.id, product_id=prod2.id)
cartItem3 = Cart_Item(cart_id=cust.cart.id, product_id=prod3.id)

prod1.window = wind1
prod2.window = wind2
prod3.window = wind3

db.session.add(cartItem1)
db.session.add(cartItem2)
db.session.add(cartItem3)

cust.cart.cart_items.append(cartItem1)
cust.cart.cart_items.append(cartItem2)
cust.cart.cart_items.append(cartItem3)

cust.cart.selected_cart_item_id = 0

db.session.commit()
