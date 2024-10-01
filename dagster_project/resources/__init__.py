import warnings

from dagster import EnvVar, ExperimentalWarning
from dagster_embedded_elt.dlt import DagsterDltResource
from dagster_snowflake import SnowflakeResource

warnings.filterwarnings("ignore", category=ExperimentalWarning)


# Resources
dlt_resource = DagsterDltResource()
snowflake_resource = SnowflakeResource(
    database=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE"),
    account=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__HOST"),
    user=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__USERNAME"),
    password=EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD"),
)
