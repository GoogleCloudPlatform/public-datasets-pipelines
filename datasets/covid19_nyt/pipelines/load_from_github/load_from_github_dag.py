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
    "start_date": "2022-06-08",
}


with DAG(
    dag_id="covid19_nyt.load_from_github",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to download and concat `us-counties-YYYY.csv` files
    download_csv_files = bash.BashOperator(
        task_id="download_csv_files",
        bash_command="mkdir -p $data_dir/us-counties\ncurl -o $data_dir/us-counties/us-counties-2020.csv -L $us_counties_2020\ncurl -o $data_dir/us-counties/us-counties-2021.csv -L $us_counties_2021\ncurl -o $data_dir/us-counties/us-counties-2022.csv -L $us_counties_2022\nmkdir -p $data_dir/us-states\ncurl -o $data_dir/us-states/us-states.csv -L $us_states\nmkdir -p $data_dir/excess-deaths\ncurl -o $data_dir/excess-deaths/excess-deaths.csv -L $excess_deaths\nmkdir -p $data_dir/mask-use\ncurl -o $data_dir/mask-use/mask-use-by-county.csv -L $mask_use_by_county\n",
        env={
            "data_dir": "/home/airflow/gcs/data/covid19-nyt",
            "us_counties_2020": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2020.csv",
            "us_counties_2021": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2021.csv",
            "us_counties_2022": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2022.csv",
            "us_states": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
            "excess_deaths": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/excess-deaths/deaths.csv",
            "mask_use_by_county": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/mask-use/mask-use-by-county.csv",
        },
    )

    # Task to load the data from Airflow data folder (GCS Composer bucket) to BigQuery
    load_us_counties_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_us_counties_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/covid19-nyt/us-counties/us-counties-*.csv"],
        source_format="CSV",
        destination_project_dataset_table="covid19_nyt.us_counties",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "date", "type": "DATE", "mode": "NULLABLE"},
            {"name": "county", "type": "STRING", "mode": "NULLABLE"},
            {"name": "state_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "county_fips_code", "type": "STRING", "mode": "NULLABLE"},
            {"name": "confirmed_cases", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths", "type": "INTEGER", "mode": "NULLABLE"},
        ],
    )

    # Task to load the data from Airflow data folder (GCS Composer bucket) to BigQuery
    load_us_states_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_us_states_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/covid19-nyt/us-states/us-states.csv"],
        source_format="CSV",
        destination_project_dataset_table="covid19_nyt.us_states",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "date", "type": "DATE", "mode": "NULLABLE"},
            {"name": "state_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "state_fips_code", "type": "STRING", "mode": "NULLABLE"},
            {"name": "confirmed_cases", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths", "type": "INTEGER", "mode": "NULLABLE"},
        ],
    )

    # Task to load the data from Airflow data folder (GCS Composer bucket) to BigQuery
    load_excess_deaths_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_excess_deaths_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/covid19-nyt/excess-deaths/excess-deaths.csv"],
        source_format="CSV",
        destination_project_dataset_table="covid19_nyt.excess_deaths",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "country", "type": "STRING", "mode": "NULLABLE"},
            {"name": "placename", "type": "STRING", "mode": "NULLABLE"},
            {"name": "frequency", "type": "STRING", "mode": "NULLABLE"},
            {"name": "start_date", "type": "DATE", "mode": "NULLABLE"},
            {"name": "end_date", "type": "DATE", "mode": "NULLABLE"},
            {"name": "year", "type": "STRING", "mode": "NULLABLE"},
            {"name": "month", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "week", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "deaths", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "expected_deaths", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "excess_deaths", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "baseline", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    # Task to load the data from Airflow data folder (GCS Composer bucket) to BigQuery
    load_mask_use_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_mask_use_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/covid19-nyt/mask-use/mask-use-by-county.csv"],
        source_format="CSV",
        destination_project_dataset_table="covid19_nyt.mask_use_by_county",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "county_fips_code", "type": "STRING", "mode": "NULLABLE"},
            {"name": "never", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "rarely", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "sometimes", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "frequently", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "always", "type": "FLOAT", "mode": "NULLABLE"},
        ],
    )

    download_csv_files >> load_us_counties_to_bq
    download_csv_files >> load_us_states_to_bq
    download_csv_files >> load_excess_deaths_to_bq
    download_csv_files >> load_mask_use_to_bq
