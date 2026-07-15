from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["tasks"]          # <-- Add this
)

celery.conf.timezone = "Asia/Kolkata"


celery.conf.beat_schedule = {

    "deadline-reminder-every-morning": {

        "task": "tasks.send_deadline_reminders",

        "schedule": crontab(minute="*"),
    },

    "monthly-placement-report": {

        "task": "tasks.send_monthly_activity_report",

        "schedule": crontab(
            hour=8,
            minute=0,
            day_of_month="1"
        ),
    },

}