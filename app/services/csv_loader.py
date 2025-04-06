import csv
from io import TextIOWrapper
from app.models.task import Task, TaskLogger
from app.extensions import db
from flask_jwt_extended import get_jwt_identity

def load_tasks_from_csv(file_storage):
    decoded_file = TextIOWrapper(file_storage.stream, encoding='utf-8')
    reader = csv.DictReader(decoded_file)
    tasks = []
    user_id = get_jwt_identity()

    for index, row in enumerate(reader, start=1):
        # Fix: Get 'subject' instead of 'title'
        subject = str(row.get('subject', '')).strip()
        description = str(row.get('description', '')).strip()
        status = str(row.get('status', 'pending')).strip().lower()

        if not subject:
            print(f"Skipping row {index}: Invalid subject -> {row}")
            continue

        task = Task(
            title=subject,
            description=description,
            status=status,
            user_id=user_id
        )
        tasks.append(task)

    db.session.add_all(tasks)
    db.session.commit()

    # Log the bulk import
    log = TaskLogger(
        task_id=None,
        title="CSV Import",
        status="imported",
        user_id=user_id
    )
    db.session.add(log)
    db.session.commit()

    return tasks
