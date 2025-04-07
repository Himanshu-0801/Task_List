# app/services/csv_tasks.py

from celery import shared_task
from app.extensions import db
from app.models.task import Task

@shared_task
def process_csv_async(tasks_data, user_id):
    try:
        for data in tasks_data:
            task = Task(
                title=data.get('title'),
                description=data.get('description'),
                status=data.get('status', 'pending'),
                user_id=user_id
            )
            db.session.add(task)
        db.session.commit()
        return f"{len(tasks_data)} tasks saved successfully"
    except Exception as e:
        db.session.rollback()
        return f"Failed to process CSV: {str(e)}"
