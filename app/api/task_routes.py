# app/api/task_routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])  # ✅ This is correct
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_bp.route('/tasks', methods=['GET'])  # ✅ This too
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])
