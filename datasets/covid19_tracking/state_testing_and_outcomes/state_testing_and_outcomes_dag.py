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
    dag_id="covid19_tracking.state_testing_and_outcomes",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to copy `case_demographics_age.csv` from HTTP source to GCS
    copy_csv_file_to_gcs = bash_operator.BashOperator(
        task_id="copy_csv_file_to_gcs",
        bash_command="echo $airflow_data_folder\necho $csv_source_url\nmkdir -p $airflow_data_folder/covid19_tracking/state_testing_and_outcomes\ncurl -o $airflow_data_folder/covid19_tracking/state_testing_and_outcomes/all-states-history-{{ ds }}.csv -L $csv_source_url\n",
        env={
            "csv_source_url": "https://covidtracking.com/data/download/all-states-history.csv",
            "airflow_data_folder": "{{ var.json.shared.airflow_data_folder }}",
        },
    )

    # Task to load the data from Airflow data folder to BigQuery
    load_csv_file_to_bq_table = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_csv_file_to_bq_table",
        bucket="{{ var.json.shared.composer_bucket }}",
        source_objects=[
            "data/covid19_tracking/state_testing_and_outcomes/all-states-history-{{ ds }}.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_tracking.state_testing_and_outcomes",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "date", "type": "DATE"},
            {"name": "state", "type": "STRING"},
            {"name": "death", "type": "INTEGER"},
            {"name": "death_confirmed", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "death_increase", "type": "INTEGER"},
            {"name": "death_probable", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hospitalized", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hospitalized_cumulative", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hospitalized_currently", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "hospitalized_increase", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "in_icu_cumulative", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "in_icu_currently", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "negative", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "negative_increase", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "negative_tests_antibody", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "negative_tests_people_antibody",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "negative_tests_viral", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "on_ventilator_cumulative", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "on_ventilator_currently", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "positive", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "positive_cases_viral", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "positive_increase", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "positive_score", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "positive_tests_antibody", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "positive_tests_antigen", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "positive_tests_people_antibody",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "name": "positive_tests_people_antigen",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "positive_tests_viral", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "recovered", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "total_test_encounters_viral",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "name": "total_test_encounters_viral_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "total_test_results", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "total_test_results_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "total_tests_antibody", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "total_tests_antigen", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "total_tests_people_antibody",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "name": "total_tests_people_antigen",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "total_tests_people_viral", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "total_tests_people_viral_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {"name": "total_tests_viral", "type": "INTEGER", "mode": "NULLABLE"},
            {
                "name": "total_tests_viral_increase",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
        ],
    )

    # Task to archive the CSV file in the destination bucket
    archive_csv_file_to_destination_bucket = gcs_to_gcs.GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id="archive_csv_file_to_destination_bucket",
        source_bucket="{{ var.json.shared.composer_bucket }}",
        source_object="data/covid19_tracking/state_testing_and_outcomes/all-states-history-{{ ds }}.csv",
        destination_bucket="{{ var.json.covid19_tracking.destination_bucket }}",
        destination_object="datasets/covid19_tracking/state_testing_and_outcomes/all-states-history-{{ ds }}.csv",
        move_object=True,
    )

    copy_csv_file_to_gcs >> load_csv_file_to_bq_table
    load_csv_file_to_bq_table >> archive_csv_file_to_destination_bucket
