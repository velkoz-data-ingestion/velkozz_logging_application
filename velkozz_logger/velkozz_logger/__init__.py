# Importing Flask Modules:
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Importing Flask REST API modules:
from flask_restful import Resource, Api

# Declaring global libraries: 
db = SQLAlchemy()

def init_app():
    "Method that creates and initalizes the core flask application"
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.DevConfig")

    # Initialize Plugins:
    db.init_app(app) # Database Connection

    # Adding Blueprints and Routes:
    with app.app_context():
        
        # Importing Routes:
        from .core import routes as core_routes
        from .microservice_logger import routes as microservice_routes

        # Creating database schema:
        db.create_all()

        #  Registering Blueprints:
        app.register_blueprint(core_routes.core_bp)
        app.register_blueprint(microservice_routes.microservice_bp)

        return app