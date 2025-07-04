from .workers import celery
from app import app, db
from application.models import User, ServiceRequest
from celery.schedules import crontab
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from sqlalchemy import select, func
import csv
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
def export_csv():
    service_history = db.session.scalars(select(ServiceRequest)).all()
    csv_file_name = f"requests_{int(datetime.now().timestamp())}.csv"
    with open(f"static/{csv_file_name}", "w", newline="") as csvfile:
        csv_file = csv.writer(csvfile, delimiter=",")
        csv_file.writerow(["ID", "Service Name", "Customer Name", "Professional Name", "Time of Request", "Time of Completion", "Task", "Service Status", "Rating", "Remarks"])
        for service_request in service_history:
            csv_file.writerow([service_request.id,
                               service_request.service.name,
                               service_request.customer.fullname,
                               service_request.professional.fullname,
                               service_request.time_of_request.strftime("%d-%m-%Y %H:%M:%S"),
                               service_request.time_of_completion.strftime("%d-%m-%Y %H:%M:%S") if service_request.time_of_completion else "N/A",
                               service_request.task,
                               service_request.service_status,
                               service_request.review.rating if service_request.review else "N/A",
                               service_request.review.remarks if service_request.review else "N/A"
                               ])
    return csv_file_name


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
        service_requests = dict(db.session.execute(select(ServiceRequest.service_status, func.count())
                                                   .where(ServiceRequest.customer_id == customer.id)
                                                   .group_by(ServiceRequest.service_status)).all())
        if service_requests:
            service_counts = {"Requested": 0, "Accepted": 0, "Rejected": 0, "Closed": 0}
            if "requested" in service_requests.keys():
                service_counts["Requested"] = service_requests["requested"]
            if "accepted" in service_requests.keys():
                service_counts["Accepted"] = service_requests["accepted"]
            if "rejected" in service_requests.keys():
                service_counts["Rejected"] = service_requests["rejected"]
            if "closed" in service_requests.keys():
                service_counts["Closed"] = service_requests["closed"]
            with open("templates/c_monthly.html") as file:
                template = Template(file.read())
                subject = f"Monthly Activity Report of {datetime.now().strftime("%B %Y")} for {customer.fullname}"
                message = template.render(customer=customer.fullname, service_counts=service_counts)
                send_email(customer.email, subject, message)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour="6", minute="30"), daily_reminder.s(), name="Daily Reminder")
    sender.add_periodic_task(crontab(hour="7", minute="30", day_of_month="1"), monthly_report.s(), name="Monthly Report")
