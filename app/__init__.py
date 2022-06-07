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

    return app


app = create_app()


