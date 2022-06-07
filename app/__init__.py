from flask import Flask

from app.config import Configuration

from app.resources import order_bp
from app.db import db
from app.schemes import ma

def create_app():

    from app.models import Customer, Product, Order
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)
    ma.init_app(app)  
    
    with app.app_context():
        db.create_all()

    app.register_blueprint(order_bp)

    
    @app.errorhandler(422)
    def error422(error):
        return error
    
    @app.errorhandler(404)
    def error404(error):
        return error
        
#     products = [
#     Product('mesa', 'mesa de madera', 12.5),
#     Product('silla', 'silla de madera', 9.58),
#     Product('mesedora', 'mesedora metalica', 19.8),
#     Product('cama ', 'cama detalica', 50.2),
#     Product('mesa de noche', 'mesa de noche en madera', 25.6),
#     Product('portatil', 'portatil hp', 500.5),
#     Product( 'table', 'table samsung', 200.9),
#     Product('celular', 'celular huawei', 580.8),
#     Product('escritorio', 'escritorio en madera y metal', 150.7)
# ]
#     customers = [
#     Customer('mauricio', 'mauricio@gmail.com'),
#     Customer('jose', 'jose@gmail.com'),
#     Customer('marcelo', 'marcelo@gmail.com'),
#     Customer('carlos', 'carlos@gmail.com'),
#     Customer('esteban', 'esteban@gmail.com'),
#     Customer('johan', 'johan@gmail.com'),
#     Customer('carolina', 'carolina@gmail.com'),
#     Customer('carmen', 'carmen@gmail.com')
#     ]
    
#     [p.save() for p in products]
#     [c.save() for c in customers]


    return app


app = create_app()


