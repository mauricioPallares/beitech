

from app.models import Customer

class Validate(object):
    
    @staticmethod
    def customers(customer_id):

        customers_list_id = Customer.list_id_customer()
        return (customer_id in customers_list_id)

    @staticmethod
    def quantity_products(quantity_product):
        return (quantity_product < 1 or quantity_product > 5)
        
    @staticmethod
    def products_available_to_customer(customer, *order_details):
        
        products_customer = Customer.get_product_from_user(customer)

        products_id = set(
            [detail["product_id"] for detail in order_details]
        )

        for product_id in products_id:
            if product_id not in products_customer:
                return False

        return True