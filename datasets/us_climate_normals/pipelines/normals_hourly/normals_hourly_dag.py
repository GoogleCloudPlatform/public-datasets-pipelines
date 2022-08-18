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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery, gcs_to_gcs

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
    copy_source_files_to_public_bucket = gcs_to_gcs.GCSToGCSOperator(
        task_id="copy_source_files_to_public_bucket",
        source_bucket="normals",
        source_object="normals-hourly/access/*.csv",
        destination_bucket="{{ var.value.composer_bucket }}",
        destination_object="data/us_climate_normals/hourly_access/",
        move_object=False,
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
                "name": "HLY_CLDH_NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLDH_NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTBKN",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTBKN_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTCLR",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTCLR_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTFEW",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTFEW_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTOVC",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTOVC_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTSCT",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_CLOD_PCTSCT_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_DEWP_10PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_DEWP_10PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_DEWP_90PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_DEWP_90PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_DEWP_NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_DEWP_NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_HIDX_NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_HIDX_NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_HTDH_NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_HTDH_NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_PRES_10PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_PRES_10PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_PRES_90PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_PRES_90PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_PRES_NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_PRES_NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_TEMP_10PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_TEMP_10PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_TEMP_90PCTL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_TEMP_90PCTL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_TEMP_NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_TEMP_NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WCHL_NORMAL",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WCHL_NORMAL_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_1STDIR",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_1STDIR_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_1STPCT",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_1STPCT_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_2NDDIR",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_2NDDIR_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_2NDPCT",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_2NDPCT_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_AVGSPD",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_AVGSPD_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_PCTCLM",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_PCTCLM_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_VCTDIR",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_VCTDIR_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_VCTSPD",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "",
            },
            {
                "name": "HLY_WIND_VCTSPD_ATTRIBUTES",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "",
            },
        ],
    )

    copy_source_files_to_public_bucket >> hourly_access
