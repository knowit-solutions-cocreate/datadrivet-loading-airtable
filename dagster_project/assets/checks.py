import json

from dagster import (
    AssetCheckExecutionContext,
    AssetCheckResult,
    AssetCheckSeverity,
    asset_check,
)
from dagster_snowflake import SnowflakeResource
from pandera import Column, DataFrameSchema, errors

from dagster_project.constants import (
    snowflake_database,
    source_base_name,
    source_schema_name,
)


@asset_check(asset="dlt_airtable_availability")
def validate_schema_airtable_availability(
    context: AssetCheckExecutionContext, snowflake: SnowflakeResource
) -> AssetCheckResult:
    schema = DataFrameSchema(
        {"ID": Column(str), "FIELDS__CONSULTANTS": Column(str)},
        # Only check columns defined in schema.
        strict=False,
        report_duplicates="all",
    )

    with snowflake.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"USE DATABASE {snowflake_database}")
            cursor.execute(f"USE SCHEMA {source_schema_name}")

            table_name = (
                context.check_specs[0]
                .asset_key.to_user_string()
                .removeprefix(f"dlt_{source_base_name}_")
            )

            cursor.execute(f"SELECT * FROM {table_name.upper()}")
            df = cursor.fetch_pandas_all()

    try:
        schema.validate(df, lazy=True)

        return AssetCheckResult(passed=True)

    except errors.SchemaErrors as e:
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.ERROR,
            metadata={"error": json.dumps(e.message, indent=2)},
        )

    except Exception as e:
        return AssetCheckResult(
            passed=False, severity=AssetCheckSeverity.ERROR, metadata={"error": str(e)}
        )
