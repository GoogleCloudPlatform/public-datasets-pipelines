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
from airflow.contrib.operators import gcs_delete_operator, gcs_to_bq, gcs_to_gcs
from airflow.operators import bash_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="covid19_tracking.state_screenshots",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Run the custom/generate_csv.py script to scrape the webpage and generate a CSV file of the state screenshots
    generate_csv_data_from_web_scraping = bash_operator.BashOperator(
        task_id="generate_csv_data_from_web_scraping",
        bash_command='mkdir -p $airflow_home/data/$dataset/$pipeline/run_date={{ ds }}\nSOURCE_URL=$source_url CSV_OUTPUT_PATH=$airflow_home/data/$dataset/$pipeline/run_date={{ ds }}/data.csv GCS_PATH_PREFIX="gs://$destination_bucket/datasets/$dataset/$pipeline/run_date={{ ds }}/screenshots" python $airflow_home/dags/$dataset/$pipeline/custom/web_scrape_and_generate_csv.py\n',
        env={
            "airflow_home": "{{ var.value.airflow_home }}",
            "destination_bucket": "{{ var.json.covid19_tracking.destination_bucket }}",
            "source_url": "https://screenshots.covidtracking.com",
            "dataset": "covid19_tracking",
            "pipeline": "state_screenshots",
        },
    )

    # Run the custom/download_screenshots.py script to download all the screenshots to the local file system (mounted GCS)
    download_screenshots = bash_operator.BashOperator(
        task_id="download_screenshots",
        bash_command='CSV_PATH=$airflow_home/data/$dataset/$pipeline/run_date={{ ds }}/data.csv \\\nSOURCE_COLUMN="source_url" \\\nDOWNLOAD_PREFIX=$airflow_home/data/$dataset/$pipeline/run_date={{ ds }} \\\npython $airflow_home/dags/$dataset/$pipeline/custom/download_screenshots.py\n',
        env={
            "airflow_home": "{{ var.value.airflow_home }}",
            "dataset": "covid19_tracking",
            "pipeline": "state_screenshots",
        },
    )

    # Upload all downloaded screenshots to the destination bucket
    upload_screenshots_to_destination_bucket = gcs_to_gcs.GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id="upload_screenshots_to_destination_bucket",
        source_bucket="{{ var.value.composer_bucket }}",
        source_object="data/covid19_tracking/state_screenshots/run_date={{ ds }}/*",
        destination_bucket="{{ var.json.covid19_tracking.destination_bucket }}",
        destination_object="datasets/covid19_tracking/state_screenshots/run_date={{ ds }}/",
        move_object=False,
    )

    # Task to load the data from Airflow data folder to BigQuery
    load_screenshots_to_bq_table = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_screenshots_to_bq_table",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/covid19_tracking/state_screenshots/run_date={{ ds }}/data.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_tracking.state_screenshots",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "state",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "2-letter postal abbreviation for the state",
            },
            {
                "name": "state_name",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The full state name",
            },
            {
                "name": "date",
                "type": "DATE",
                "mode": "REQUIRED",
                "description": "Date of the observations",
            },
            {
                "name": "source_type",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "How far from the original event or phenomenon the information source is created. Can be one of primary, secondary, tertiary, quaternary",
            },
            {
                "name": "time_of_day",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The time of day, based on a 12-hour clock in Eastern Time",
            },
            {
                "name": "source_url",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The URL where the screenshot or file was originally found",
            },
            {
                "name": "google_cloud_storage_uri",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The GCS location where the screenshot or file was copied to",
            },
        ],
    )

    # Delete downloaded screenshots from the Cloud Composer bucket
    delete_screenshots_from_composer_bucket = (
        gcs_delete_operator.GoogleCloudStorageDeleteOperator(
            task_id="delete_screenshots_from_composer_bucket",
            bucket_name="{{ var.value.composer_bucket }}",
            prefix="data/covid19_tracking/state_screenshots/run_date={{ ds }}",
        )
    )

    generate_csv_data_from_web_scraping >> download_screenshots
    download_screenshots >> upload_screenshots_to_destination_bucket
    upload_screenshots_to_destination_bucket >> load_screenshots_to_bq_table
    load_screenshots_to_bq_table >> delete_screenshots_from_composer_bucket
