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
from airflow.contrib.operators import gcs_to_bq

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-05-01",
}


with DAG(
    dag_id="vaccination_access.vaccination_access_to_bq",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV file from covid19-open-data bucket to facility_boundary_us_walk_15min
    gcs_to_bq_table = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bq_table",
        bucket="covid19-open-data",
        source_objects=[
            "covid19-vaccination-access/facility_boundary_us_walk_15min.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="vaccination_access.facility_boundary_us_walk_15min",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "facility_place_id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "facility_provider_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "facility_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "facility_latitude", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "facility_longitude", "type": "FLOAT", "mode": "REQUIRED"},
            {"name": "facility_country_region", "type": "STRING", "mode": "NULLABLE"},
            {"name": "facility_country_code", "type": "STRING", "mode": "NULLABLE"},
            {"name": "facility_sub_region_1", "type": "STRING", "mode": "NULLABLE"},
            {
                "name": "facility_sub_region_1_code",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {"name": "facility_sub_region_2", "type": "STRING", "mode": "NULLABLE"},
            {
                "name": "facility_sub_region_2_code",
                "type": "STRING",
                "mode": "NULLABLE",
            },
            {"name": "facility_region_place_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "mode_of_transportation", "type": "STRING", "mode": "NULLABLE"},
            {
                "name": "travel_time_threshold_minutes",
                "type": "INTEGER",
                "mode": "NULLABLE",
            },
            {
                "name": "facility_catchment_boundary",
                "type": "STRING",
                "mode": "NULLABLE",
            },
        ],
    )

    gcs_to_bq_table
