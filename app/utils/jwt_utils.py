import jwt
from flask import request, jsonify, g
from functools import wraps
from app.models.user import User
from app import db

SECRET_KEY = "your_secret_key_here"  # replace with your real key or import from config/env

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            if not user_id:
                return jsonify({"message": "Invalid token payload"}), 401

            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "User not found"}), 404

            g.current_user = user
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function
