# app/api/auth_routes.py

from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ('username', 'email', 'password', 'role')
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"'{field}' is required and cannot be empty"}), 400

    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])
    role = data['role']

    user = User(username=username, email=email, password_hash=password, role=role)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201
