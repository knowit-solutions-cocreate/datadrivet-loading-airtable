from dagster import DefaultScheduleStatus, ScheduleDefinition

from dagster_project.jobs import airtable_job

airtable_schedule = ScheduleDefinition(
    job=airtable_job,
    # Run on weekdays 1-5 @ 09:05
    cron_schedule="09 5 * * 1-5",
    default_status=DefaultScheduleStatus.RUNNING,
)
