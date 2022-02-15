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
    dag_id="covid19_tracking.national_testing_and_outcomes",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy `national-history.csv` from COVID-19 Tracking Project to GCS
    copy_csv_file_to_gcs = bash_operator.BashOperator(
        task_id="copy_csv_file_to_gcs",
        bash_command="echo $airflow_data_folder\necho $csv_source_url\nmkdir -p $airflow_data_folder/covid19_tracking/national_testing_and_outcomes\ncurl -o $airflow_data_folder/covid19_tracking/national_testing_and_outcomes/national-history-{{ ds }}.csv -L $csv_source_url\n",
        env={
            "csv_source_url": "https://covidtracking.com/data/download/national-history.csv",
            "airflow_data_folder": "{{ var.value.airflow_data_folder }}",
        },
    )

    # Task to load the data from Airflow data folder to BigQuery
    load_csv_file_to_bq_table = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_csv_file_to_bq_table",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/covid19_tracking/national_testing_and_outcomes/national-history-{{ ds }}.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_tracking.national_testing_and_outcomes",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "date",
                "type": "DATE",
                "mode": "REQUIRED",
                "description": "Date of the observations",
            },
            {
                "name": "death",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Total cumulative number of people that have died",
            },
            {
                "name": "death_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "The daily increase in the number of people that have died based on the previous day's value",
            },
            {
                "name": "in_icu_cumulative",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Total number of individuals who have ever been hospitalized in the Intensive Care Unit with COVID-19",
            },
            {
                "name": "in_icu_currently",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Individuals who are currently hospitalized in the Intensive Care Unit with COVID-19",
            },
            {
                "name": "hospitalized_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Daily increase in hospitalized_cumulative, calculated from the previous day's value",
            },
            {
                "name": "hospitalized_currently",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Individuals who are currently hospitalized with COVID-19",
            },
            {
                "name": "hospitalized_cumulative",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Total number of individuals who have ever been hospitalized with COVID-19",
            },
            {
                "name": "negative",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Total number of unique people with a completed PCR test that returns negative",
            },
            {
                "name": "negative_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Daily increase of unique people with a completed PCR test that returns negative based on the previous day's value",
            },
            {
                "name": "on_ventilator_cumulative",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Total number of individuals who have ever been hospitalized under advanced ventilation with COVID-19",
            },
            {
                "name": "on_ventilator_currently",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Individuals who are currently hospitalized under advanced ventilation with COVID-19",
            },
            {
                "name": "positive",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "Total number of confirmed plus probable cases of COVID-19 reported by the state or territory",
            },
            {
                "name": "positive_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "The daily increase in positive, which measures cases (confirmed plus probable) calculated based on the previous day's value",
            },
            {
                "name": "states",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "The number of states and territories included in the US dataset for this day",
            },
            {
                "name": "total_test_results",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "In most states, this field is currently computed by adding positive and negative values because, historically, some states do not report totals, and to work around different reporting cadences for cases and tests",
            },
            {
                "name": "total_test_results_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "The daily increase in total_test_results, calculated from the previous day's value",
            },
        ],
    )

    # Task to archive the CSV file in the destination bucket
    archive_csv_file_to_destination_bucket = gcs_to_gcs.GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id="archive_csv_file_to_destination_bucket",
        source_bucket="{{ var.value.composer_bucket }}",
        source_object="data/covid19_tracking/national_testing_and_outcomes/national-history-{{ ds }}.csv",
        destination_bucket="{{ var.json.covid19_tracking.destination_bucket }}",
        destination_object="datasets/covid19_tracking/national_testing_and_outcomes/national-history-{{ ds }}.csv",
        move_object=True,
    )

    copy_csv_file_to_gcs >> load_csv_file_to_bq_table
    load_csv_file_to_bq_table >> archive_csv_file_to_destination_bucket
