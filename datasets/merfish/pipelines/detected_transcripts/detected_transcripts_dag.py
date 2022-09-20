# Copyright 2022 Google LLC
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
    "start_date": "2022-08-20",
}


with DAG(
    dag_id="merfish.detected_transcripts",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV data to a BigQuery table
    load_detected_transcripts_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_detected_transcripts_to_bq",
        bucket="public-datasets-vizgen-merfish",
        source_objects=[
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice1/Replicate1/detected_transcripts_S1R1.csv",
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice1/Replicate2/detected_transcripts_S1R2.csv",
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice1/Replicate3/detected_transcripts_S1R3.csv",
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice2/Replicate1/detected_transcripts_S2R1.csv",
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice2/Replicate2/detected_transcripts_S2R2.csv",
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice2/Replicate3/detected_transcripts_S2R3.csv",
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice3/Replicate1/detected_transcripts_S3R1.csv",
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice3/Replicate2/detected_transcripts_S3R2.csv",
            "datasets/mouse_brain_map/BrainReceptorShowcase/Slice3/Replicate3/detected_transcripts_S3R3.csv",
        ],
        source_format="CSV",
        destination_project_dataset_table="bigquery-public-data-dev.merfish.detected_transcripts",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "barcode_id",
                "type": "string",
                "description": None,
                "mode": "nullable",
            },
            {
                "name": "global_x",
                "type": "string",
                "description": None,
                "mode": "nullable",
            },
            {
                "name": "global_y",
                "type": "string",
                "description": None,
                "mode": "nullable",
            },
            {
                "name": "global_z",
                "type": "string",
                "description": None,
                "mode": "nullable",
            },
            {"name": "x", "type": "string", "description": None, "mode": "nullable"},
            {"name": "y", "type": "string", "description": None, "mode": "nullable"},
            {"name": "fov", "type": "string", "description": None, "mode": "nullable"},
            {"name": "gene", "type": "string", "description": None, "mode": "nullable"},
        ],
    )

    load_detected_transcripts_to_bq
