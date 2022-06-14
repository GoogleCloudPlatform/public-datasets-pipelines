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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="nasa_wildfire.past_week",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    past_week_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="past_week_transform_csv",
        startup_timeout_seconds=600,
        name="past_week",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.nasa_wildfire.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_Global_7d.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/nasa_wildfire/past_week/data_output.csv",
            "PIPELINE_NAME": "past_week",
            "CSV_HEADERS": '["latitude","longitude","bright_ti4","scan","track","acq_date","acq_time","satellite", "confidence","version","bright_ti5","frp","daynight","acquisition_timestamp"]',
            "RENAME_MAPPINGS": '{"latitude":"latitude","longitude":"longitude","bright_ti4":"bright_ti4","scan":"scan", "track":"track","acq_date":"acq_date","acq_time":"acq_time","satellite":"satellite", "confidence":"confidence","version":"version","bright_ti5":"bright_ti5","frp":"frp", "daynight":"daynight"}',
        },
        resources={
            "request_memory": "3G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_past_week_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_past_week_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nasa_wildfire/past_week/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="nasa_wildfire.past_week",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "latitude",
                "type": "float",
                "description": "Center of nominal 375 m fire pixel",
                "mode": "nullable",
            },
            {
                "name": "longitude",
                "type": "float",
                "description": "Center of nominal 375 m fire pixel",
                "mode": "nullable",
            },
            {
                "name": "bright_ti4",
                "type": "float",
                "description": "Brightness temperature I-4: VIIRS I-4 channel brightness temperature of the fire pixel measured in Kelvin.",
                "mode": "nullable",
            },
            {
                "name": "scan",
                "type": "float",
                "description": "The algorithm produces approximately 375 m pixels at nadir. Scan and track reflect actual pixel size.",
                "mode": "nullable",
            },
            {
                "name": "track",
                "type": "float",
                "description": "The algorithm produces approximately 375 m pixels at nadir. Scan and track reflect actual pixel size.",
                "mode": "nullable",
            },
            {
                "name": "acq_date",
                "type": "date",
                "description": "Date of VIIRS acquisition.",
                "mode": "nullable",
            },
            {
                "name": "acq_time",
                "type": "time",
                "description": "Time of acquisition/overpass of the satellite (in UTC).",
                "mode": "nullable",
            },
            {
                "name": "satellite",
                "type": "string",
                "description": "N= Suomi National Polar-orbiting Partnership (Suomi-NPP)",
                "mode": "nullable",
            },
            {
                "name": "confidence",
                "type": "string",
                "description": "This value is based on a collection of intermediate algorithm quantities used in the detection process. It is intended to help users gauge the quality of individual hotspot/fire pixels. Confidence values are set to low nominal and high. Low confidence daytime fire pixels are typically associated with areas of sun glint and lower relative temperature anomaly (<15K) in the mid-infrared channel I4. Nominal confidence pixels are those free of potential sun glint contamination during the day and marked by strong (>15K) temperature anomaly in either day or nighttime data. High confidence fire pixels are associated with day or nighttime saturated pixels.",
                "mode": "nullable",
            },
            {
                "name": "version",
                "type": "string",
                "description": "Version identifies the collection (e.g. VIIRS Collection 1) and source of data processing: Near Real-Time (NRT suffix added to collection) or Standard Processing (collection only). 1.0NRT - Collection 1 NRT processing. 1.0 - Collection 1 Standard processing",
                "mode": "nullable",
            },
            {
                "name": "bright_ti5",
                "type": "float",
                "description": "Brightness temperature I-5: I-5 Channel brightness temperature of the fire pixel measured in Kelvin.",
                "mode": "nullable",
            },
            {
                "name": "frp",
                "type": "float",
                "description": "Fire Radiative Power: FRP depicts the pixel-integrated fire radiative power in MW (megawatts). FRP depicts the pixel-integrated fire radiative power in MW (megawatts). Given the unique spatial and spectral resolution of the data the VIIRS 375 m fire detection algorithm was customized and tuned in order to optimize its response over small fires while balancing the occurrence of false alarms. Frequent saturation of the mid-infrared I4 channel (3.55-3.93 µm) driving the detection of active fires requires additional tests and procedures to avoid pixel classification errors. As a result sub-pixel fire characterization (e.g. fire radiative power [FRP] retrieval) is only viable across small and/or low-intensity fires. Systematic FRP retrievals are based on a hybrid approach combining 375 and 750 m data. In fact starting in 2015 the algorithm incorporated additional VIIRS channel M13 (3.973-4.128 µm) 750 m data in both aggregated and unaggregated format.",
                "mode": "nullable",
            },
            {
                "name": "daynight",
                "type": "string",
                "description": "D= Daytime fire N= Nighttime fire",
                "mode": "nullable",
            },
            {
                "name": "acquisition_timestamp",
                "type": "timestamp",
                "description": "",
                "mode": "nullable",
            },
        ],
    )

    past_week_transform_csv >> load_past_week_to_bq
