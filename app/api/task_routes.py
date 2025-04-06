# app/api/task_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.extensions import db
from datetime import datetime
from app.services.csv_loader import load_tasks_from_csv


task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id, is_active=True).all()
    return jsonify([task.to_dict() for task in tasks]), 200


@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()

    try:
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if data.get('due_date') else None

        task = Task(
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status', 'pending'),
            due_date=due_date,
            user_id=user_id
        )

        db.session.add(task)
        db.session.commit()

        return jsonify(task.to_dict()), 201

    except Exception as e:
        return jsonify({'error': f"Failed to create task: {str(e)}"}), 400


@task_bp.route('/upload-csv', methods=['POST'])
@jwt_required()
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "CSV file is required"}), 400

    file = request.files['file']
    if not file or not file.filename.endswith('.csv'):
        return jsonify({"error": "Only .csv files are allowed"}), 400

    user_id = get_jwt_identity()

    try:
        tasks = load_csv_to_tasks(file, user_id)
        return jsonify({
            "message": f"{len(tasks)} tasks uploaded successfully.",
            "tasks": [task.to_dict() for task in tasks]
        }), 201
    except Exception as e:
        return jsonify({"error": f"Failed to process CSV: {str(e)}"}), 500
