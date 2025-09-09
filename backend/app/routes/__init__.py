from flask import Blueprint
from app.routes.onboarding_routes import onboarding_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(onboarding_bp)