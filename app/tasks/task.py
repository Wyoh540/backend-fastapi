from app.celery import celery_app


@celery_app.task
def hello():
    return "Hello, world!"
