from flask import Flask
from dotenv import load_dotenv
import os

from app.extensions import db, migrate, jwt

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Import and register blueprints
    from app.api.routes import api_bp
    from app.api.auth_routes import auth_bp  # ✅ Register the auth routes
    from app.routes import main_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  # ✅ Add this line
    app.register_blueprint(main_bp)

    return app
