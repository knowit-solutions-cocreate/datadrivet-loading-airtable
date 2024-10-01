import dlt
from dlt.sources.helpers import requests


@dlt.source(max_table_nesting=2)
def airtable():
    def _get_data(baseId, tableIdOrName, raise_for_errors=True):
        # Load airtable token
        token = dlt.secrets.get("SOURCE__AIRTABLE__CREDENTIALS__TOKEN")

        # Define headers
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = f"https://api.airtable.com/v0/{baseId}/{tableIdOrName}"

        response = requests.get(url, headers=headers)

        if raise_for_errors:
            response.raise_for_status()
        if response.status_code == 404:
            return {}
        return response.json()

    @dlt.resource(write_disposition="replace")
    def availability():
        # Table identifiers
        baseId = "appI7h5pbHI8hFOJp"
        tableIdOrName = "Availability"

        consultants = _get_data(baseId=baseId, tableIdOrName=tableIdOrName)["records"]
        for consultant in consultants:
            yield consultant

    return availability


if __name__ == "__main__":
    # configure the pipeline with your destination details
    pipeline = dlt.pipeline(
        pipeline_name="airtable", destination="snowflake", dataset_name="raw_airtable"
    )
    # run the pipeline with your parameters
    load_info = pipeline.run(airtable())

    # pretty print the information on data that was loaded
    print(load_info)
