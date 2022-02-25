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
    dag_id="epa_historical_air_quality.nonoxnoy_hourly_summary",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="30 4 * * *",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="no2_hourly_summary",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.epa_historical_air_quality.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://aqs.epa.gov/aqsweb/airdata/hourly_NONOxNOy_YEAR_ITERATOR.zip",
            "START_YEAR": "1990",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "2500000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/epa_historical_air_quality/nonoxnoy_hourly_summary/files/data_output.csv",
            "DATA_NAMES": '[ "state_code", "county_code", "site_num", "parameter_code", "poc",\n  "latitude", "longitude", "datum", "parameter_name", "date_local",\n  "time_local", "date_gmt", "time_gmt", "sample_measurement", "units_of_measure",\n  "mdl", "uncertainty", "qualifier", "method_type", "method_code", "method_name",\n  "state_name", "county_name", "date_of_last_change" ]',
            "DATA_DTYPES": '{ "state_code": "str", "county_code": "str", "site_num": "str", "parameter_code": "int32", "poc": "int32",\n  "latitude": "float64", "longitude": "float64", "datum": "str", "parameter_name": "str", "date_local": "datetime64[ns]",\n  "time_local": "str", "date_gmt": "datetime64[ns]", "time_gmt": "str", "sample_measurement": "float64", "units_of_measure": "str",\n  "mdl": "float64", "uncertainty": "float64", "qualifier": "str", "method_type": "str", "method_code": "int32", "method_name": "str",\n  "state_name": "str", "county_name": "str", "date_of_last_change": "datetime64[ns]" }',
        },
        resources={
            "request_memory": "8G",
            "request_cpu": "3",
            "request_ephemeral_storage": "5G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/epa_historical_air_quality/nonoxnoy_hourly_summary/files/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.epa_historical_air_quality.destination_tables.nonoxnoy_hourly_summary }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "state_code",
                "type": "STRING",
                "description": "The FIPS code of the state in which the monitor resides.",
                "mode": "NULLABLE",
            },
            {
                "name": "county_code",
                "type": "STRING",
                "description": "The FIPS code of the county in which the monitor resides.",
                "mode": "NULLABLE",
            },
            {
                "name": "site_num",
                "type": "STRING",
                "description": "A unique number within the county identifying the site.",
                "mode": "NULLABLE",
            },
            {
                "name": "parameter_code",
                "type": "INTEGER",
                "description": "The AQS code corresponding to the parameter measured by the monitor.",
                "mode": "NULLABLE",
            },
            {
                "name": "poc",
                "type": "INTEGER",
                "description": "This is the “Parameter Occurrence Code” used to distinguish different instruments that measure the same parameter at the same site.",
                "mode": "NULLABLE",
            },
            {
                "name": "latitude",
                "type": "FLOAT",
                "description": "The monitoring site’s angular distance north of the equator measured in decimal degrees.",
                "mode": "NULLABLE",
            },
            {
                "name": "longitude",
                "type": "FLOAT",
                "description": "The monitoring site’s angular distance east of the prime meridian measured in decimal degrees.",
                "mode": "NULLABLE",
            },
            {
                "name": "datum",
                "type": "STRING",
                "description": "The Datum associated with the Latitude and Longitude measures.",
                "mode": "NULLABLE",
            },
            {
                "name": "parameter_name",
                "type": "STRING",
                "description": "The name or description assigned in AQS to the parameter measured by the monitor. Parameters may be pollutants or non-pollutants.",
                "mode": "NULLABLE",
            },
            {
                "name": "date_local",
                "type": "TIMESTAMP",
                "description": "The calendar date for the summary. All daily summaries are for the local standard day (midnight to midnight) at the monitor.",
                "mode": "NULLABLE",
            },
            {
                "name": "time_local",
                "type": "STRING",
                "description": "The time of day that sampling began on a 24-hour clock in Local Standard Time.",
                "mode": "NULLABLE",
            },
            {
                "name": "date_gmt",
                "type": "TIMESTAMP",
                "description": "The calendar date of the sample in Greenwich Mean Time.",
                "mode": "NULLABLE",
            },
            {
                "name": "time_gmt",
                "type": "STRING",
                "description": "The time of day that sampling began on a 24-hour clock in Greenwich Mean Time.",
                "mode": "NULLABLE",
            },
            {
                "name": "sample_measurement",
                "type": "FLOAT",
                "description": "The measured value in the standard units of measure for the parameter.",
                "mode": "NULLABLE",
            },
            {
                "name": "units_of_measure",
                "type": "STRING",
                "description": "The unit of measure for the parameter. QAD always returns data in the standard units for the parameter. Submitters are allowed to report data in any unit and EPA converts to a standard unit so that we may use the data in calculations.",
                "mode": "NULLABLE",
            },
            {
                "name": "mdl",
                "type": "FLOAT",
                "description": "The Method Detection Limit. The minimum sample concentration detectable for the monitor and method. Note: if samples are reported below this level, they may have been replaced by 1/2 the MDL.",
                "mode": "NULLABLE",
            },
            {
                "name": "uncertainty",
                "type": "FLOAT",
                "description": "The total measurement uncertainty associated with a reported measurement as indicated by the reporting agency.",
                "mode": "NULLABLE",
            },
            {
                "name": "qualifier",
                "type": "STRING",
                "description": "Sample values may have qualifiers that indicate why they are missing or that they are out of the ordinary. Types of qualifiers are: null data, exceptional event, natural events, and quality assurance. The highest ranking qualifier, if any, is described in this field.",
                "mode": "NULLABLE",
            },
            {
                "name": "method_type",
                "type": "STRING",
                "description": "An indication of whether the method used to collect the data is a federal reference method (FRM), equivalent to a federal reference method, an approved regional method, or none of the above (non-federal reference method).",
                "mode": "NULLABLE",
            },
            {
                "name": "method_code",
                "type": "STRING",
                "description": "An internal system code indicating the method (processes, equipment, and protocols) used in gathering and measuring the sample. The method name is in the next column.",
                "mode": "NULLABLE",
            },
            {
                "name": "method_name",
                "type": "STRING",
                "description": "A short description of the processes, equipment, and protocols used in gathering and measuring the sample.",
                "mode": "NULLABLE",
            },
            {
                "name": "state_name",
                "type": "STRING",
                "description": "The name of the state where the monitoring site is located.",
                "mode": "NULLABLE",
            },
            {
                "name": "county_name",
                "type": "STRING",
                "description": "The name of the county where the monitoring site is located.",
                "mode": "NULLABLE",
            },
            {
                "name": "date_of_last_change",
                "type": "TIMESTAMP",
                "description": "The date the last time any numeric values in this record were updated in the AQS data system.",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
