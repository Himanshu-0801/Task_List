import csv
from io import TextIOWrapper
from flask_jwt_extended import get_jwt_identity

from app.services.csv_tasks import process_csv_async  # ✅ corrected import path

def load_tasks_from_csv(file_storage):
    decoded_file = TextIOWrapper(file_storage.stream, encoding='utf-8')
    reader = csv.DictReader(decoded_file)
    tasks_data = []
    user_id = get_jwt_identity()

    for index, row in enumerate(reader, start=1):
        subject = str(row.get('subject', '')).strip()
        description = str(row.get('description', '')).strip()
        status = str(row.get('status', 'pending')).strip().lower()

        if not subject:
            print(f"Skipping row {index}: Invalid subject -> {row}")
            continue

        tasks_data.append({
            "title": subject,
            "description": description,
            "status": status,
        })

    if tasks_data:
        process_csv_async.delay(tasks_data, user_id)  # ✅ Celery task call

    return tasks_data
