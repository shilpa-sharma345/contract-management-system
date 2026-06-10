from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.reminder_service import ReminderService
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def start_scheduler():
    # Runs every day at 8:00 AM — checks all three thresholds (30, 7, 1 day)
    scheduler.add_job(
        run_daily_reminders,
        trigger=CronTrigger(hour=8, minute=0),
        id="daily_expiry_reminders",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler started — daily expiry reminders at 08:00 AM")


def stop_scheduler():
    scheduler.shutdown()
    logger.info("Scheduler stopped")


async def run_daily_reminders():
    logger.info("Running daily expiry reminder job...")
    for days in [30, 7, 1]:
        await ReminderService.send_expiry_reminders(days)
    logger.info("Daily expiry reminder job complete")