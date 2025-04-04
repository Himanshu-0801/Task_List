from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/postgres')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ✅ Ensure Both Blueprints Are Imported & Registered
    from app.api.routes import api_bp
    from app.routes import main_bp  # Ensure the blueprint is properly imported

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)  # Register the default `/` route

    return app
