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
from airflow.contrib.operators import bigquery_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-06-01",
}


with DAG(
    dag_id="google_trends.top_terms",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to run a BQ to BQ operation
    fetch_and_load_top_n = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="fetch_and_load_top_n",
        source_project_dataset_tables=[
            "{{ var.json.google_trends.top_n.source_project_dataset_table }}"
        ],
        destination_project_dataset_table="{{ var.json.google_trends.top_n.destination_project_dataset_table }}",
        impersonation_chain="{{ var.json.google_trends.service_account }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to run a BQ to BQ operation
    fetch_and_load_top_rising = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="fetch_and_load_top_rising",
        source_project_dataset_tables=[
            "{{ var.json.google_trends.top_rising.source_project_dataset_table }}"
        ],
        destination_project_dataset_table="{{ var.json.google_trends.top_rising.destination_project_dataset_table }}",
        impersonation_chain="{{ var.json.google_trends.service_account }}",
        write_disposition="WRITE_TRUNCATE",
    )

    fetch_and_load_top_n
    fetch_and_load_top_rising
