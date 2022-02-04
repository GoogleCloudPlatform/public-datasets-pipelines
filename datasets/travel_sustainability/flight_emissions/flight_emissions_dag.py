# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from airflow import DAG
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-01-09",
}


with DAG(
    dag_id="travel_sustainability.flight_emissions",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 15 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV data to a BigQuery table
    flight_emissions_gcs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="flight_emissions_gcs_to_bq",
        bucket="{{ var.json.travel_sustainability.source_bucket }}",
        source_objects=["flight_emissions.csv"],
        source_format="CSV",
        destination_project_dataset_table="travel_sustainability.flight_emissions",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "origin",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "IATA code for origin airport",
            },
            {
                "name": "destination",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "IATA code for destination airport",
            },
            {
                "name": "aircraft_model",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "IATA code for aircraft model",
            },
            {
                "name": "co2e_total_grams",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Total grams of CO2e estimated for the flight including non-CO2 effects",
            },
            {
                "name": "co2_total_grams",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Total grams of CO2 estimated for the flight",
            },
        ],
    )

    flight_emissions_gcs_to_bq
