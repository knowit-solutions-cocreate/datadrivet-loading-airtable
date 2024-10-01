from dagster import AssetSelection, define_asset_job

from dagster_project.assets.assets import airtable_assets

from .constants import source_base_name

airtable_job = define_asset_job(
    name=f"{source_base_name}_job",
    selection=AssetSelection.assets(airtable_assets).downstream(),
    description="",
)
