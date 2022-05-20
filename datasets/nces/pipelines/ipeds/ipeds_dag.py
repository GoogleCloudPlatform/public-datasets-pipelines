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
    "start_date": "2021-05-01",
}


with DAG(
    dag_id="nces.ipeds",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV data to a BigQuery table
    load_c2020_a_csv_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_c2020_a_csv_to_bq",
        bucket="{{ var.json.nces.storage_bucket }}",
        source_objects=["IPEDS/2020/c2020_a.csv"],
        source_format="CSV",
        destination_project_dataset_table="nces_ipeds.c2020_a",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_c2020_a_dict_frequencies_csv_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_c2020_a_dict_frequencies_csv_to_bq",
        bucket="{{ var.json.nces.storage_bucket }}",
        source_objects=["IPEDS/2020/c2020_a_dict_frequencies.csv"],
        source_format="CSV",
        destination_project_dataset_table="nces_ipeds.c2020_a_dict_frequencies",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_hd2020_csv_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_hd2020_csv_to_bq",
        bucket="{{ var.json.nces.storage_bucket }}",
        source_objects=["IPEDS/2020/hd2020.csv"],
        source_format="CSV",
        destination_project_dataset_table="nces_ipeds.hd2020",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_hd2020_dict_frequencies_csv_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_hd2020_dict_frequencies_csv_to_bq",
        bucket="{{ var.json.nces.storage_bucket }}",
        source_objects=["IPEDS/2020/hd2020_dict_frequencies.csv"],
        source_format="CSV",
        destination_project_dataset_table="nces_ipeds.hd2020_dict_frequencies",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_ic2020_csv_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_ic2020_csv_to_bq",
        bucket="{{ var.json.nces.storage_bucket }}",
        source_objects=["IPEDS/2020/ic2020.csv"],
        source_format="CSV",
        destination_project_dataset_table="nces_ipeds.ic2020",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
    )

    # Task to load CSV data to a BigQuery table
    load_ic2020_dict_frequencies_csv_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_ic2020_dict_frequencies_csv_to_bq",
        bucket="{{ var.json.nces.storage_bucket }}",
        source_objects=["IPEDS/2020/ic2020_dict_frequencies.csv"],
        source_format="CSV",
        destination_project_dataset_table="nces_ipeds.ic2020_dict_frequencies",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
    )

    load_c2020_a_csv_to_bq
    load_c2020_a_dict_frequencies_csv_to_bq
    load_hd2020_csv_to_bq
    load_hd2020_dict_frequencies_csv_to_bq
    load_ic2020_csv_to_bq
    load_ic2020_dict_frequencies_csv_to_bq
