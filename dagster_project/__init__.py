from dagster import (
    Definitions,
    load_asset_checks_from_package_module,
    load_assets_from_package_module,
)

from dagster_project import assets
from dagster_project.jobs import airtable_job
from dagster_project.resources import dlt_resource, snowflake_resource
from dagster_project.schedules import airtable_schedule

all_assets = load_assets_from_package_module(assets)
all_checks = load_asset_checks_from_package_module(assets)

# Definitions
defs = Definitions(
    assets=all_assets,
    asset_checks=all_checks,
    jobs=[airtable_job],
    schedules=[airtable_schedule],
    resources={
        "snowflake": snowflake_resource,
        "dlt": dlt_resource,
    },
)
