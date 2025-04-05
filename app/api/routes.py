# app/api/routes.py

from flask import Blueprint, jsonify
from app.api.task_routes import task_bp  # ✅ Good: importing sub-blueprint

api_bp = Blueprint('api', __name__)  # ✅ This is your main /api blueprint

@api_bp.route('/ping', methods=['GET'])  # ✅ Should work at /api/ping
def ping():
    return jsonify({"message": "pong"}), 200

# ✅ Now you're registering the task blueprint to this one
api_bp.register_blueprint(task_bp)
