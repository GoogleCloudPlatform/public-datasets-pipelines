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
from airflow.contrib.operators import gcs_to_bq, gcs_to_gcs
from airflow.operators import bash_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="covid19_tracking.covid_racial_data_tracker",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy CRDT CSV file from COVID-19 Tracking Project to GCS
    download_raw_csv_file = bash_operator.BashOperator(
        task_id="download_raw_csv_file",
        bash_command="mkdir -p $airflow_home/data/covid19_tracking/covid_racial_data_tracker\ncurl -o $airflow_home/data/covid19_tracking/covid_racial_data_tracker/raw-crdt-data-{{ ds }}.csv -L $csv_source_url\n",
        env={
            "csv_source_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8SzaERcKJOD_EzrtCDK1dX1zkoMochlA9iHoHg_RSw3V8bkpfk1mpw4pfL5RdtSOyx_oScsUtyXyk/pub?gid=43720681&single=true&output=csv",
            "airflow_home": "{{ var.json.shared.airflow_home }}",
        },
    )

    # Run a custom/*.py script to process the raw CSV contents into a BigQuery friendly format
    process_raw_csv_file = bash_operator.BashOperator(
        task_id="process_raw_csv_file",
        bash_command="SOURCE_CSV=$airflow_home/data/$dataset/$pipeline/raw-crdt-data-{{ ds }}.csv TARGET_CSV=$airflow_home/data/$dataset/$pipeline/crdt-data-{{ ds }}.csv python $airflow_home/dags/$dataset/$pipeline/custom/transform_dates.py\n",
        env={
            "airflow_home": "{{ var.json.shared.airflow_home }}",
            "dataset": "covid19_tracking",
            "pipeline": "covid_racial_data_tracker",
        },
    )

    # Task to load the data from Airflow data folder to BigQuery
    load_csv_file_to_bq_table = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_csv_file_to_bq_table",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=[
            "data/covid19_tracking/covid_racial_data_tracker/crdt-data-{{ ds }}.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_tracking.covid_racial_data_tracker",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "date", "type": "DATE"},
            {"name": "state", "type": "STRING"},
            {"name": "cases_total", "type": "INTEGER"},
            {"name": "cases_white", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_black", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_latinx", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_asian", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_aian", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_nhpi", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_multiracial", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_other", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_unknown", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cases_ethnicity_hispanic", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "cases_ethnicity_nonhispanic",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "cases_ethnicity_unknown", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_total", "type": "INTEGER"},
            {"name": "deaths_white", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_black", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_latinx", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_asian", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_aian", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_nhpi", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_multiracial", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_other", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths_unknown", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "deaths_ethnicity_hispanic",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "name": "deaths_ethnicity_nonhispanic",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "deaths_ethnicity_unknown", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_total", "type": "INTEGER"},
            {"name": "hosp_white", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_black", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_latinx", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_asian", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_aian", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_nhpi", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_multiracial", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_other", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_unknown", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hosp_ethnicity_hispanic", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "hosp_ethnicity_nonhispanic",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "hosp_ethnicity_unknown", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_total", "type": "INTEGER"},
            {"name": "tests_white", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_black", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_latinx", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_asian", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_aian", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_nhpi", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_multiracial", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_other", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_unknown", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tests_ethnicity_hispanic", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "tests_ethnicity_nonhispanic",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "tests_ethnicity_unknow", "type": "INTEGER", "mode": "NULLABLE"},
        ],
    )

    # Task to archive the CSV file in the destination bucket
    archive_csv_file_to_destination_bucket = gcs_to_gcs.GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id="archive_csv_file_to_destination_bucket",
        source_bucket="{{ var.json.shared.composer_bucket }}",
        source_object="data/covid19_tracking/covid_racial_data_tracker/crdt-data-{{ ds }}.csv",
        destination_bucket="{{ var.json.covid19_tracking.destination_bucket }}",
        destination_object="datasets/covid19_tracking/covid_racial_data_tracker/crdt-data-{{ ds }}.csv",
        move_object=True,
    )

    download_raw_csv_file >> process_raw_csv_file
    process_raw_csv_file >> load_csv_file_to_bq_table
    load_csv_file_to_bq_table >> archive_csv_file_to_destination_bucket
