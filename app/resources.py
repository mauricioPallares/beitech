from flask_restful import Resource, Api, abort
from flask import Blueprint, request
from datetime import datetime

from app.schemes import ListOrdersRequestShema, CreateOrderShema
from app.models import Customer, Order, Product, add_order_detail, get_order_detail

order_bp = Blueprint("Orders", __name__, url_prefix="/api")
order_api = Api(order_bp)


class Orders(Resource):
    def get(self):
        result = []
        schemaRequest = ListOrdersRequestShema()
        customers_list_id = Customer.list_id_customer()

        error = schemaRequest.validate(request.args)
        if error:
            return abort(422, **error)

        parseDate = lambda date: datetime.strptime(date, "%d/%m/%Y").date()

        customer = schemaRequest.dump(request.args).get("customer")
        start_date = parseDate(schemaRequest.dump(request.args).get("start_date"))
        end_date = parseDate(schemaRequest.dump(request.args).get("end_date"))

        if customer not in customers_list_id:
            error = {"Error": "Customer Id Invalido"}
            return abort(422, **error)

        orders = Order().get_orders(
            customer_id=customer, start_date=start_date, end_date=end_date
        )

        if not orders:
            return {"mensaje": "No hay ordenes para ese Cliente en ese rango de fechas"}

        for order in orders:
            order_detail = [detail for detail in get_order_detail(order.order_id)]
            order_product = []

            for detail in order_detail:
                product = Product().get_by_id(detail[1])
                order_product.append((product, detail[3]))

            order_data = {
                "creation_date": str(order.created_at),
                "order_id": order.order_id,
                "total": order.total,
                "address_delivery": order.address_delivery,
                "order_product": [{"name": product.name, "unit": detail[3]}],
            }

            result.append(order_data)

        return result

    def post(self):
        order_shema = CreateOrderShema()

        # validacion de los esquemas
        error = order_shema.validate(request.json)
        if error:
            abort(422, **error)

        data = order_shema.dump(request.get_json())

        # valida que el customer_id sea valido
        customers_list_id = Customer.list_id_customer()

        if data.get("customer") not in customers_list_id:
            error = {"Error": "Customer Id Invalido"}
            return abort(422, **error)

        # valida que no exceda los 5 productos por cliente
        if data.get("count_products") < 1 or data.get("count_products") > 5:
            error = {"Error": "Cantidad de productos no permitida"}
            return abort(422, **error)

        # valida los productos validos para un cliente
        products_customer = Customer.get_product_from_user(data.get("customer"))
        products_id = set(
            [detail["product_id"] for detail in data.get("order_details")]
        )

        for product_id in products_id:
            if product_id not in products_customer:
                error = {"Error": "Productos no permitidos para el customer"}
                return abort(422, **error)

        totals = [
            (Product().get_by_id(detail["product_id"]).price * detail["quantity"])
            for detail in data.get("order_details")
        ]

        order = Order()

        order.customer_id = data.get("customer")
        order.address_delivery = data.get("address_delivery")
        order.total = sum(totals)

        order.save()

        [
            add_order_detail(order.order_id, **order_detail)
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

        for customer in customers:

            c = {
                "customer_name": customer.name,
                "customer_id": customer.customer_id,
                "products_available": [
                    {"product_id": p.product_id} for p in customer.products
                ],
            }

            print(customer.products[0].product_id)

            result.append(c)

        return result


order_api.add_resource(Orders, "/orders")
order_api.add_resource(Users, "/users")
