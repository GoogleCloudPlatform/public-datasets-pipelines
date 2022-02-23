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
    "start_date": "2021-08-05",
}


with DAG(
    dag_id="google_cloud_release_notes.release_notes",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 5 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to run a BQ to BQ operator
    google_cloud_release_notes = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="google_cloud_release_notes",
        source_project_dataset_tables=[
            "{{ var.json.google_cloud_release_notes.release_notes.source_project_dataset_table }}"
        ],
        destination_project_dataset_table="{{ var.json.google_cloud_release_notes.release_notes.destination_project_dataset_table }}",
        impersonation_chain="{{ var.json.google_cloud_release_notes.service_account }}",
        write_disposition="WRITE_TRUNCATE",
        gcp_conn_id="google_cloud_release_notes_conn",
    )

    google_cloud_release_notes
