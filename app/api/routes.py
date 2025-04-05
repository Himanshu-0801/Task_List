# app/api/routes.py

from flask import Blueprint
from app.api.auth_routes import auth_bp
from app.api.task_routes import task_bp

api_bp = Blueprint('api', __name__)

# register auth & task blueprints under the /api prefix
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(task_bp)
