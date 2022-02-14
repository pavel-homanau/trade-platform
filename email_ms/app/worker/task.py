from celery import shared_task

from app.worker.service.email_service import SendEmailService


@shared_task
def send_email_task():
    SendEmailService().send_email_task()
