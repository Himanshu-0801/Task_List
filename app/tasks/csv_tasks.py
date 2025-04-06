from app.extensions import db
from app.models.task import Task, TaskLogger
from celery import shared_task

@shared_task()
def process_csv_async(data, user_id):
    for item in data:
        task = Task(
            title=item.get('title'),
            description=item.get('description', ''),
            status=item.get('status', 'pending'),
            user_id=user_id
        )
        db.session.add(task)

    db.session.commit()

    log = TaskLogger(
        task_id=None,
        title="CSV Import (Async)",
        status="imported",
        user_id=user_id
    )
    db.session.add(log)
    db.session.commit()
