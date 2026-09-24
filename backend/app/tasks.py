from app.worker import celery_app
@celery_app.task(name="ragforge.healthcheck")
def healthcheck_task():
    return {"status":"ok"}
