from flask_restful import Resource, Api, abort
from flask import Blueprint, request
from datetime import datetime

from app.schemes import ListOrdersRequestShema, CreateOrderShema
from app.models import Customer, Order, Product
from app.validation import Validate

order_bp = Blueprint("Orders", __name__, url_prefix="/api")
order_api = Api(order_bp)


class Orders(Resource):
    def get(self):
        result = []
        schemaRequest = ListOrdersRequestShema()

        if schemaRequest.validate(request.args):
            return abort(422, **error)

        parseDate = lambda date: datetime.strptime(date, "%d/%m/%Y").date()

        customer = schemaRequest.dump(request.args).get("customer")
        start_date = parseDate(schemaRequest.dump(request.args).get("start_date"))
        end_date = parseDate(schemaRequest.dump(request.args).get("end_date"))

        if not Validate.customers(customer):
            error = {"Error": "Customer Id Invalido"}
            return abort(422, **error)

        orders = Order.get_orders(
            customer_id=customer, start_date=start_date, end_date=end_date
        )

        if not orders:
            return {"mensaje": "No hay ordenes para ese Cliente en ese rango de fechas"}

        for i, order in enumerate(orders):
            order_detail = [detail for detail in Order.get_order_detail(order.order_id)]
            order_product = []

            for detail in order_detail:
                product = Product.get_by_id(detail[1])
                order_product.append((product, detail[3]))

            order_data = {
                "creation_date": str(order.created_at),
                "order_id": order.order_id,
                "total": order.total,
                "address_delivery": order.address_delivery,
                "order_product": [{"name": product.name, "unit": detail[3]}],
            }

            result.append({i: order_data})

        return {"orders": result}

    def post(self):
        order_shema = CreateOrderShema()

        if order_shema.validate(request.json):
            abort(422, **error)

        data = order_shema.dump(request.get_json())

        # Validaciones

        if not Validate.customers(data.get("customer")):
            error = {"Error": "Customer Id Invalido"}
            return abort(422, **error)

        if Validate.quantity_products(data.get("count_products")):
            error = {"Error": "Cantidad de productos no permitida"}
            return abort(422, **error)

        if not Validate.products_available_to_customer(
            data.get("customer"), *data.get("order_details")
        ):
            error = {"Error": "Productos no permitidos para el customer"}
            return abort(422, **error)

        order = Order(
            customer_id=data.get("customer"),
            address_delivery=data.get("address_delivery"),
        )

        order.get_total(*data.get("order_details"))

        order.save()

        [
            order.add_order_detail(order.order_id, **order_detail)
            for order_detail in data.get("order_details")
        ]

        return {
            "mensaje": "Orden Ingresada",
            "order_id": order.order_id,
            "total": order.total,
        }


class Users(Resource):
    def get(self):
        customers = Customer.get_all()

        result = []

        for i, customer in enumerate(customers):

            c = {
                "customer_id": customer.customer_id,
                "customer_name": customer.name,
                "products_available": [
                    {"product_id": p.product_id, "name": p.name}
                    for p in customer.products
                ],
            }

            result.append({i: c})

        return {"customers": result}


order_api.add_resource(Orders, "/orders")
order_api.add_resource(Users, "/users")
