from marshmallow import Schema, fields
from app.models import Customer,Product
from flask_marshmallow import Marshmallow

ma = Marshmallow()

class ListOrdersRequestShema(Schema):


    customer = fields.Integer(
        required=True,
        error_messages={
            'required': 'Es necesario ingresar un Cliente Id',
        })
    start_date = fields.Str(
        required=True, 
        error_messages={
            'required': 'Es necesario ingresar una fecha'
        }
    )
    end_date = fields.Str(
        required=True, 
        error_messages={
            'required': 'Es necesario ingresar una fecha'
        }
    )

class CreateOrderShema(Schema):
    customer = fields.Integer(
        required=True,
        error_messages={
            'required': 'Es necesario ingresar un Cliente Id',
        }
    )

    address_delivery = fields.Str()
    date_created = fields.Str()
    order_details = fields.List(fields.Dict(), required=True)
    count_products = fields.Function(lambda x: len(x.get('order_details')))

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    products = fields.Nested('ProductSchema', many= True, only=['product_id'])
    orders = fields.Nested('OrderSchema', only=['order_id'])

    class Meta:
        model = Customer


class ProductSchema(ma.SQLAlchemyAutoSchema):
    orders = fields.Nested('Order', many= True)
    class Meta:
        model = Product

