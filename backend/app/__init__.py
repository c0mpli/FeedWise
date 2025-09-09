from flask import Flask
from app.config import Config
from app.db.database import db
from app.utils.errors import APIError, handle_api_error
from app.routes import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(api_bp)
    
    app.register_error_handler(APIError, handle_api_error)
    
    with app.app_context():
        db.create_all()
    
    return app