from flask import Blueprint
from app.controllers.onboarding_controller import OnboardingController

onboarding_bp = Blueprint('onboarding', __name__, url_prefix='/onboarding')

# Single onboarding route with step parameter
onboarding_bp.route('/', methods=['GET', 'POST'])(OnboardingController.process_onboarding_step)

# Update route for modifications
onboarding_bp.route('/update', methods=['PUT'])(OnboardingController.update_onboarding_data)