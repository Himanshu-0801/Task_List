from celery import Celery
from app import create_app

celery = Celery(__name__)

def make_celery(app):
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

# Only initialize app and celery when this file is run (not on import)
def init_celery():
    app = create_app()
    make_celery(app)
