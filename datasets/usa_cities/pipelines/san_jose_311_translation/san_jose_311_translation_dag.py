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
    "start_date": "2022-06-01",
}


with DAG(
    dag_id="usa_cities.san_jose_311_translation",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to download the TSV files.
    download_tsv_files = bash.BashOperator(
        task_id="download_tsv_files",
        bash_command="mkdir -p $data_dir/\ncurl -o $data_dir/sentencepairs_en_es.tsv -L $tsv_es_source_url\ncurl -o $data_dir/sentencepairs_en_vi.tsv -L $tsv_vi_source_url\n",
        env={
            "tsv_es_source_url": "https://data.sanjoseca.gov/dataset/b7763cdb-cac2-4d24-a069-0d61dd0cf6fe/resource/1efa692e-efac-4dee-911c-39ac5a1ebbdc/download/sentencepairs_en_es-sheet1-2020-07-20t21_10_43.010z.tsv",
            "tsv_vi_source_url": "https://data.sanjoseca.gov/dataset/b7763cdb-cac2-4d24-a069-0d61dd0cf6fe/resource/8b0d4e19-685d-43d3-8301-a1ff4b4d00bb/download/201013_training-en-vi-vi-to-en-2020-10-13t22_27_18.444z.tsv",
            "data_dir": "/home/airflow/gcs/data/usa_cities/san_jose_311_translation",
        },
    )

    # Task to load the data from Airflow data folder to BigQuery
    load_tsv_es_file_to_bq_table = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_tsv_es_file_to_bq_table",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/usa_cities/san_jose_311_translation/sentencepairs_en_es.tsv"
        ],
        source_format="CSV",
        field_delimiter="\t",
        destination_project_dataset_table="usa_cities.san_jose_311_english_spanish",
        skip_leading_rows=0,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "english",
                "type": "STRING",
                "description": "The phrase in English",
                "mode": "NULLABLE",
            },
            {
                "name": "spanish",
                "type": "STRING",
                "description": "The phrase in Spanish",
                "mode": "NULLABLE",
            },
        ],
    )

    # Task to load the data from Airflow data folder to BigQuery
    load_tsv_vi_file_to_bq_table = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_tsv_vi_file_to_bq_table",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/usa_cities/san_jose_311_translation/sentencepairs_en_vi.tsv"
        ],
        source_format="CSV",
        field_delimiter="\t",
        destination_project_dataset_table="usa_cities.san_jose_311_vietnamese_english",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "vietnamese",
                "type": "STRING",
                "description": "The phrase in Vietnamese",
                "mode": "NULLABLE",
            },
            {
                "name": "english",
                "type": "STRING",
                "description": "The phrase in English",
                "mode": "NULLABLE",
            },
        ],
    )

    download_tsv_files >> [load_tsv_es_file_to_bq_table, load_tsv_vi_file_to_bq_table]
