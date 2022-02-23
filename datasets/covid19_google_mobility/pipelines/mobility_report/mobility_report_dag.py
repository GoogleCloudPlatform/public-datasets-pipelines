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
    dag_id="covid19_google_mobility.mobility_report",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    mobility_report_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="mobility_report_transform_csv",
        startup_timeout_seconds=600,
        name="mobility_report",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.covid19_google_mobility.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/covid19_google_mobility/mobility_report/data_output.csv",
            "PIPELINE_NAME": "mobility_report",
            "CSV_HEADERS": '["country_region_code" ,"country_region" ,"sub_region_1" ,"sub_region_2" ,"metro_area" ,"iso_3166_2_code" ,"census_fips_code" ,"place_id" ,"date" ,"retail_and_recreation_percent_change_from_baseline" ,"grocery_and_pharmacy_percent_change_from_baseline" ,"parks_percent_change_from_baseline" ,"transit_stations_percent_change_from_baseline" ,"workplaces_percent_change_from_baseline" ,"residential_percent_change_from_baseline"]',
            "RENAME_MAPPINGS": '{"country_region_code":"country_region_code" ,"country_region":"country_region" ,"sub_region_1":"sub_region_1" ,"sub_region_2":"sub_region_2" ,"metro_area":"metro_area" ,"iso_3166_2_code":"iso_3166_2_code" ,"census_fips_code":"census_fips_code" ,"place_id":"place_id" ,"date":"date" ,"retail_and_recreation_percent_change_from_baseline":"retail_and_recreation_percent_change_from_baseline" ,"grocery_and_pharmacy_percent_change_from_baseline":"grocery_and_pharmacy_percent_change_from_baseline" ,"parks_percent_change_from_baseline":"parks_percent_change_from_baseline" ,"transit_stations_percent_change_from_baseline":"transit_stations_percent_change_from_baseline" ,"workplaces_percent_change_from_baseline":"workplaces_percent_change_from_baseline" ,"residential_percent_change_from_baseline":"residential_percent_change_from_baseline"}',
        },
        resources={
            "request_memory": "8G",
            "request_cpu": "2",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_mobility_report_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_mobility_report_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/covid19_google_mobility/mobility_report/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="covid19_google_mobility.mobility_report",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "country_region_code",
                "type": "string",
                "description": "2 letter alpha code for the country/region in which changes are measured relative to the baseline. These values correspond with the ISO 3166-1 alpha-2 codes",
                "mode": "nullable",
            },
            {
                "name": "country_region",
                "type": "string",
                "description": "The country/region in which changes are measured relative to the baseline",
                "mode": "nullable",
            },
            {
                "name": "sub_region_1",
                "type": "string",
                "description": "First geographic sub-region in which the data is aggregated. This varies by country/region to ensure privacy and public health value in consultation with local public health authorities",
                "mode": "nullable",
            },
            {
                "name": "sub_region_2",
                "type": "string",
                "description": "Second geographic sub-region in which the data is aggregated. This varies by country/region to ensure privacy and public health value in consultation with local public health authorities",
                "mode": "nullable",
            },
            {
                "name": "metro_area",
                "type": "string",
                "description": "A specific metro area to measure mobility within a given city/metro area. This varies by country/region to ensure privacy and public health value in consultation with local public health authorities",
                "mode": "nullable",
            },
            {
                "name": "iso_3166_2_code",
                "type": "string",
                "description": "Unique identifier for the geographic region as defined by ISO Standard 3166-2.",
                "mode": "nullable",
            },
            {
                "name": "census_fips_code",
                "type": "string",
                "description": "Unique identifier for each US county as defined by the US Census Bureau. Maps to county_fips_code in other tables",
                "mode": "nullable",
            },
            {
                "name": "place_id",
                "type": "string",
                "description": "A textual identifier that uniquely identifies a place in the Google Places database and on Google Maps (details). For example ChIJd_Y0eVIvkIARuQyDN0F1LBA. For details see the following link: https://developers.google.com/places/web-service/place-id",
                "mode": "nullable",
            },
            {
                "name": "date",
                "type": "date",
                "description": "Changes for a given date as compared to baseline. Baseline is the median value for the corresponding day of the week during the 5-week period Jan 3–Feb 6 2020.",
                "mode": "nullable",
            },
            {
                "name": "retail_and_recreation_percent_change_from_baseline",
                "type": "integer",
                "description": "Mobility trends for places like restaurants cafes shopping centers theme parks museums libraries and movie theaters.",
                "mode": "nullable",
            },
            {
                "name": "grocery_and_pharmacy_percent_change_from_baseline",
                "type": "integer",
                "description": "Mobility trends for places like grocery markets food warehouses farmers markets specialty food shops drug stores and pharmacies.",
                "mode": "nullable",
            },
            {
                "name": "parks_percent_change_from_baseline",
                "type": "integer",
                "description": "Mobility trends for places like local parks national parks public beaches marinas dog parks plazas and public gardens.",
                "mode": "nullable",
            },
            {
                "name": "transit_stations_percent_change_from_baseline",
                "type": "integer",
                "description": "Mobility trends for places like public transport hubs such as subway bus and train stations.",
                "mode": "nullable",
            },
            {
                "name": "workplaces_percent_change_from_baseline",
                "type": "integer",
                "description": "Mobility trends for places of work.",
                "mode": "nullable",
            },
            {
                "name": "residential_percent_change_from_baseline",
                "type": "integer",
                "description": "Mobility trends for places of residence.",
                "mode": "nullable",
            },
        ],
    )

    mobility_report_transform_csv >> load_mobility_report_to_bq
