from typing import Iterable

from dagster import AssetExecutionContext, AssetKey, SourceAsset
from dagster_embedded_elt.dlt import (
    DagsterDltResource,
    DagsterDltTranslator,
    dlt_assets,
)
from dlt import pipeline
from dlt.destinations import snowflake
from dlt.extract.resource import DltResource

from data_sources.airtable import airtable

from ..constants import (
    source_base_name,
    source_schema_name,
)

pipeline_name = f"{source_base_name}_dlt_pipeline"


class DltPipelineTranslator(DagsterDltTranslator):
    """inspired by: https://github.com/dagster-io/dagster/issues/21049#issuecomment-2043147862"""

    def get_deps_asset_keys(self, resource: DltResource) -> Iterable[AssetKey]:
        return [AssetKey([pipeline_name])]


@dlt_assets(
    dlt_source=airtable(),
    dlt_pipeline=pipeline(
        pipeline_name=pipeline_name,
        dataset_name=source_schema_name,
        destination=snowflake(),
        progress="enlighten",
    ),
    name=f"{source_base_name}",
    group_name=f"{source_base_name}",
    dagster_dlt_translator=DltPipelineTranslator(),
)
def airtable_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


"""
Modifies metadata group name for the dlt_assets 
to have depedencies in same group as assets.
SourceAsset is deprecated but this does not work with AssetSpec yet.
"""
airtable_assets_source = [
    SourceAsset(
        key=key,
        group_name=source_base_name,
    )
    for key in airtable_assets.dependency_keys
]
