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
from airflow.operators import bash
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-06-17",
}


with DAG(
    dag_id="usa_names.usa_1910_current",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy `namesbystate.zip` from Social Security Administration to GCS
    download_and_process_source_zip_file = bash.BashOperator(
        task_id="download_and_process_source_zip_file",
        bash_command="mkdir -p $data_dir/{{ ds }}\ncurl -o $data_dir/{{ ds }}/namesbystate.zip -L $zip_source_url\nunzip $data_dir/{{ ds }}/namesbystate.zip -d $data_dir/{{ ds }}\ncat $data_dir/{{ ds }}/*.TXT \u003e\u003e $data_dir/{{ ds }}/data.csv\n",
        env={
            "zip_source_url": "https://www.ssa.gov/OACT/babynames/state/namesbystate.zip",
            "data_dir": "/home/airflow/gcs/data/usa_names/usa_1910_current",
        },
    )

    # Task to load the data from Airflow data folder to BigQuery
    load_csv_file_to_bq_table = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_csv_file_to_bq_table",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=["data/usa_names/usa_1910_current/{{ ds }}/data.csv"],
        source_format="CSV",
        destination_project_dataset_table="usa_names.usa_1910_current",
        skip_leading_rows=0,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "state",
                "type": "STRING",
                "description": "2-digit state code",
                "mode": "NULLABLE",
            },
            {
                "name": "gender",
                "type": "STRING",
                "description": "Sex (M=male or F=female)",
                "mode": "NULLABLE",
            },
            {
                "name": "year",
                "type": "INTEGER",
                "description": "4-digit year of birth",
                "mode": "NULLABLE",
            },
            {
                "name": "name",
                "type": "STRING",
                "description": "Given name of a person at birth",
                "mode": "NULLABLE",
            },
            {
                "name": "number",
                "type": "INTEGER",
                "description": "Number of occurrences of the name",
                "mode": "NULLABLE",
            },
        ],
    )

    download_and_process_source_zip_file >> load_csv_file_to_bq_table
