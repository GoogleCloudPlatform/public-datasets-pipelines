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
from airflow.providers.google.cloud.operators import cloud_storage_transfer_service
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="us_climate_normals.us_climate_normals",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="0 * * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy source files to public bucket
    copy_source_files_to_public_bucket = (
        cloud_storage_transfer_service.CloudDataTransferServiceGCSToGCSOperator(
            task_id="copy_source_files_to_public_bucket",
            timeout=43200,
            retries=0,
            wait=True,
            project_id="bigquery-public-data-dev",
            source_bucket="normals",
            source_path="normals-hourly/access",
            destination_bucket="{{ var.value.composer_bucket }}",
            destination_path="data/us_climate_normals/hourly_access",
            transfer_options={"overwriteWhen": "DIFFERENT"},
        )
    )

    # Load U.S. Climate Normals Hourly Data (Most Recent)
    hourly_access = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="hourly_access",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/us_climate_normals/hourly_access/*.csv"],
        destination_project_dataset_table="us_climate_normals.hourly_access",
        source_format="CSV",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "STATION",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "DATE",
                "type": "TIMESTAMP",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "LATITUDE",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "LONGITUDE",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "ELEVATION",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": "",
            },
            {"name": "NAME", "type": "STRING", "mode": "NULLABLE", "description": ""},
            {
                "name": "HLY-CLDH-NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLDH-NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTBKN",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTBKN_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTCLR",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTCLR_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTFEW",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTFEW_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTOVC",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTOVC_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTSCT",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-CLOD-PCTSCT_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-DEWP-10PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-DEWP-10PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-DEWP-90PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-DEWP-90PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-DEWP-NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-DEWP-NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-HIDX-NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-HIDX-NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-HTDH-NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-HTDH-NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-PRES-10PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-PRES-10PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-PRES-90PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-PRES-90PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-PRES-NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-PRES-NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-TEMP-10PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-TEMP-10PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-TEMP-90PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-TEMP-90PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-TEMP-NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-TEMP-NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WCHL-NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WCHL-NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-1STDIR",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-1STDIR_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-1STPCT",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-1STPCT_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-2NDDIR",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-2NDDIR_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-2NDPCT",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-2NDPCT_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-AVGSPD",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-AVGSPD_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-PCTCLM",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-PCTCLM_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-VCTDIR",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-VCTDIR_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-VCTSPD",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY-WIND-VCTSPD_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
        ],
    )

    copy_source_files_to_public_bucket >> hourly_access
