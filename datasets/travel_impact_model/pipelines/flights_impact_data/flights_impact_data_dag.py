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
    dag_id="travel_impact_model.flights_impact_data",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 15 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV data to a BigQuery table
    flights_impact_data_gcs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="flights_impact_data_gcs_to_bq",
        bucket="{{ var.json.travel_impact_model.source_bucket }}",
        source_objects=["flights_impact_data.csv"],
        source_format="CSV",
        destination_project_dataset_table="travel_impact_model.flights_impact_data",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "carrier",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "IATA code of the airline operating the flight",
            },
            {
                "name": "flight_number",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "Flight number assigned by the operating airline",
            },
            {
                "name": "departure_date",
                "type": "DATE",
                "mode": "REQUIRED",
                "description": "Departure date of the flight",
            },
            {
                "name": "origin",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "IATA airport code of the origin",
            },
            {
                "name": "destination",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "IATA airport code of the destination",
            },
            {
                "name": "economy_co2e_grams_per_pax",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Estimated CO2e in grams for one passenger in economy cabin including non-CO2 effects",
            },
            {
                "name": "premium_economy_co2e_grams_per_pax",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Estimated CO2e in grams for one passenger in premium economy cabin including non-CO2 effects",
            },
            {
                "name": "business_co2e_grams_per_pax",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Estimated CO2e in grams for one passenger in business cabin including non-CO2 effects",
            },
            {
                "name": "first_co2e_grams_per_pax",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Estimated CO2e in grams for one passenger in first cabin including non-CO2 effects",
            },
            {
                "name": "economy_co2_grams_per_pax",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Estimated CO2 in grams for one passenger in economy cabin excluding non-CO2 effects",
            },
            {
                "name": "premium_economy_co2_grams_per_pax",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Estimated CO2 in grams for one passenger in premium economy cabin excluding non-CO2 effects",
            },
            {
                "name": "business_co2_grams_per_pax",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Estimated CO2 in grams for one passenger in business cabin excluding non-CO2 effects",
            },
            {
                "name": "first_co2_grams_per_pax",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "Estimated CO2 in grams for one passenger in first cabin excluding non-CO2 effects",
            },
        ],
    )

    flights_impact_data_gcs_to_bq
