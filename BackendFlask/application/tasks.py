from .workers import celery
from app import app, db
from application.models import User, ServiceRequest
from celery.schedules import crontab
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from sqlalchemy import select
import smtplib


def send_email(recipient, subject, body):
    msg = MIMEMultipart()
    msg["From"] = app.config["SENDER_EMAIL"]
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))
    with smtplib.SMTP(host=app.config["MAIL_SERVER"], port=app.config["MAIL_PORT"]) as server:
        server.login(app.config["SENDER_EMAIL"], app.config["SENDER_PASSWORD"])
        server.send_message(msg)


@celery.task
def daily_reminder():
    professionals = db.session.scalars(select(User).filter_by(role="professional")).all()
    for professional in professionals:
        pending_services = db.session.scalars(select(ServiceRequest)
                                              .filter(ServiceRequest.professional_id == professional.id, ServiceRequest.service_status == "requested")
                                              .order_by(ServiceRequest.time_of_request.desc())).all()
        if pending_services:
            with open("templates/p_daily.html") as file:
                template = Template(file.read())
                subject = f"Daily Reminder of {datetime.now().strftime("%d-%m-%Y")} for {professional.fullname}"
                message = template.render(professional=professional.fullname, pending_services=pending_services)
                send_email(professional.email, subject, message)


@celery.task
def monthly_report():
    customers = db.session.scalars(select(User).filter_by(role="customer")).all()
    for customer in customers:
        service_requests = db.session.scalars(select(ServiceRequest).filter_by(customer_id=customer.id)).all()
        if service_requests:
            service_counts = {"Requested": 0, "Accepted": 0, "Rejected": 0, "Closed": 0}
            for request in service_requests:
                if request.service_status == "requested":
                    service_counts["Requested"] += 1
                elif request.service_status == "accepted":
                    service_counts["Accepted"] += 1
                elif request.service_status == "rejected":
                    service_counts["Rejected"] += 1
                elif request.service_status == "closed":
                    service_counts["Closed"] += 1
            with open("templates/c_monthly.html") as file:
                template = Template(file.read())
                subject = f"Monthly Activity Report of {datetime.now().strftime("%B %Y")} for {customer.fullname}"
                message = template.render(customer=customer.fullname, service_counts=service_counts)
                send_email(customer.email, subject, message)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=6, minute=0), daily_reminder.s(), name="Daily Reminder")
    sender.add_periodic_task(crontab(hour="6", minute=0, day_of_month="1"), monthly_report.s(), name="Monthly Report")
