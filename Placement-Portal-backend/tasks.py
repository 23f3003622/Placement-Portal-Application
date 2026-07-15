from datetime import date, timedelta
from flask import render_template
from celery_worker import celery
from app import app, mail
from models import Student, JobPosition, Application
from flask_mail import Message
from datetime import datetime
from calendar import month_name
import csv
import os




@celery.task
def send_deadline_reminders():

    with app.app_context():

        tomorrow = date.today() + timedelta(days=1)

        print("Checking deadline:", tomorrow)

        jobs = JobPosition.query.filter(
            JobPosition.application_deadline == tomorrow
        ).all()

        print("Jobs found:", len(jobs))

        for job in jobs:

            print("Processing job:", job.title)

            students = Student.query.all()

            print("Students found:", len(students))

            for student in students:

                print(
                    "Checking student:",
                    student.full_name,
                    student.user.email
                )

                applied = Application.query.filter_by(
                    student_id=student.id,
                    job_id=job.id
                ).first()

                if applied:
                    print(
                        student.full_name,
                        "already applied"
                    )
                    continue

                msg = Message(
                    subject="Placement Deadline Reminder",
                    sender="shriyakuhu534@gmail.com",
                    recipients=[student.user.email]
                )

                msg.body = f"""
Hello {student.full_name},

This is a friendly reminder that the application deadline for the following job is tomorrow.

Job Title: {job.title}
Company: {job.company.company_name}
Deadline: {job.application_deadline.strftime("%d %B %Y")}

Please submit your application before the deadline if you are interested.

Best regards,
Placement Portal
"""

                try:
                    mail.send(msg)
                    print("Sent to", student.user.email)

                except Exception as e:
                    print("Failed:", student.user.email)
                    print(e)

                print(
                    "Email sent to:",
                    student.user.email
                )

        return "Reminder task completed"
    

@celery.task
def send_monthly_activity_report():

    with app.app_context():

        today = date.today()

        # First day of current month
        first_day_current = today.replace(day=1)

        # Last day of previous month
        last_day_previous = first_day_current - timedelta(days=1)

        # First day of previous month
        first_day_previous = last_day_previous.replace(day=1)

        print("Generating report...")

        '''

        # -----------------------------
        # Total Placement Drives
        # -----------------------------

        total_drives = JobPosition.query.filter(
            JobPosition.created_at >= first_day_previous,
            JobPosition.created_at <= last_day_previous
        ).count()

        # -----------------------------
        # Total Applications
        # -----------------------------

        total_applied = Application.query.filter(
            Application.applied_at >= first_day_previous,
            Application.applied_at <= last_day_previous
        ).count()

        # -----------------------------
        # Total Selected
        # -----------------------------

        total_selected = Application.query.filter(
            Application.status == "Selected",
            Application.applied_at >= first_day_previous,
            Application.applied_at <= last_day_previous
        ).count()

        '''

        total_drives = JobPosition.query.count()
        total_applied = Application.query.count()
        total_selected = Application.query.filter_by(
                status="Selected"
            ).count()
        
        print("Total Drives:", total_drives)
        print("Total Applied:", total_applied)
        print("Total Selected:", total_selected)

        html = render_template(
            "emails/monthly_report.html",

            month_name=month_name[last_day_previous.month],

            total_drives=total_drives,

            total_applied=total_applied,

            total_selected=total_selected,

            generated_date=today.strftime("%d %B %Y")
        )

        msg = Message(
            subject="Monthly Placement Activity Report",
            sender="shriyakuhu534@gmail.com",
            recipients=["admin@gmail.com"]      
        )

        msg.html = html

        mail.send(msg)

        print("Monthly Report Sent")

        return "Monthly report sent"
    

@celery.task
def export_applications_csv(student_id):

    with app.app_context():

        student = Student.query.get(student_id)

        if not student:
            return "Student not found"

        applications = Application.query.filter_by(
            student_id=student.id
        ).all()

        # Create exports folder if it doesn't exist
        export_folder = "exports"

        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        filename = f"{export_folder}/applications_{student.id}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Student ID",
                "Company Name",
                "Drive Title",
                "Application Status",
                "Application Date"
            ])

            for application in applications:

                writer.writerow([
                    student.id,
                    application.job.company.company_name,
                    application.job.title,
                    application.status,
                    application.application_date.strftime("%d-%m-%Y")
                ])

        msg = Message(
            subject="Placement Applications Export",
            sender="shriyakuhu534@gmail.com",
            recipients=[student.user.email]
        )

        msg.body = f"""
Hello {student.full_name},

Your placement application history has been exported successfully.

The CSV file is attached with this email.

Regards,
Placement Portal
"""

        with open(filename, "rb") as fp:

            msg.attach(
                filename=f"Applications_{student.id}.csv",
                content_type="text/csv",
                data=fp.read()
            )

        mail.send(msg)

        # Delete file after sending email
        os.remove(filename)

        print(f"CSV exported and emailed to {student.user.email}")

        return "Export completed"