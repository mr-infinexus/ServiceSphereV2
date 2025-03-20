from app import app
from celery import Celery

celery = Celery("ServiceSphere Background Jobs")

celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"], result_backend=app.config["CELERY_RESULT_BACKEND"])
celery.conf.broker_connection_retry_on_startup = True
celery.conf.timezone = "Asia/Kolkata"


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
