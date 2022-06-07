from app.db import db, BaseModel
from datetime import datetime
from sqlalchemy.dialects.mysql import insert


customer_products = db.Table(
    "customer_has_product",
    db.Column("customer_id", db.Integer, db.ForeignKey('customer.customer_id')),
    db.Column("product_id", db.Integer, db.ForeignKey('product.product_id'))
)

order_detail = db.Table(
    "order_detail",
    db.Column("order_id",db.Integer, db.ForeignKey('order.order_id')),
    db.Column("product_id", db.Integer, db.ForeignKey('product.product_id')),
    db.Column("order_detail_id", db.Integer, primary_key=True),
    db.Column("quantity", db.Integer)
)

class Customer(db.Model,BaseModel):
    __tablename__ = 'customer'
   
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(300))

    products = db.relationship("Product", secondary=customer_products, backref ="_customer")
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __init__(self,name, email):
        self.name = name
        self.email = email

    @staticmethod
    def list_id_customer():
        records = db.session.query(Customer.customer_id).all()

        return [ record[0] for record in records]

    @staticmethod
    def get_product_from_user(id):
        user = db.session.query(Customer).filter_by(customer_id=id).first()

        return [product.product_id for product in user.products]
        
class Product(db.Model,BaseModel):
    __tablename__ = 'product'
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(191))
    description = db.Column(db.String(191))
    price = db.Column(db.Float)

    def __init__(self,name, description, price):
        self.name = name
        self.description = description
        self.price = price
        
    customer = db.relationship('Customer', secondary=customer_products, backref ="_product")
    orders = db.relationship('Order', secondary=order_detail, backref ="_order")

class Order(db.Model,BaseModel):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    address_delivery = db.Column(db.String(200))
    total = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))


    order_details = db.relationship("Product", secondary=order_detail, backref="_order")

    def __init__(self,customer_id, address_delivery):
        self.customer_id = customer_id
        self.adress_delivery = address_delivery
        
    
    def get_total(self, *details):
        self.total =sum([
            (Product.get_by_id(detail["product_id"]).price * detail["quantity"])
            for detail in details
        ])

    @staticmethod
    def get_orders(customer_id, start_date, end_date):
        
        return db.session.query(Order)\
            .filter(Order.customer_id == customer_id)\
            .filter(Order.created_at.between(start_date, end_date))\
            .all()
        
    
    @staticmethod
    def add_order_detail(order_id, **order_details):
        
        statements = insert(order_detail).values(
            order_id= order_id,
            quantity= order_details['quantity'],
            product_id = order_details['product_id']
        )

        db.session.execute(statements)
        db.session.commit()

    @staticmethod
    def get_order_detail(order_id):
        return db.session.query(order_detail)\
            .filter_by(order_id=order_id).all()