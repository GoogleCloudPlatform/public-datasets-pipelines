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
    mobility_report = kubernetes_pod.KubernetesPodOperator(
        task_id="mobility_report",
        startup_timeout_seconds=600,
        name="mobility_report",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.covid19_google_mobility.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "Covid 19 Mobility Report",
            "SOURCE_URL": "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv",
            "SOURCE_FILE": "files/covid19_mobility_report_data.csv",
            "TARGET_FILE": "files/covid19_mobility_report_data_output.csv",
            "CHUNKSIZE": "1000000",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "covid19_google_mobility",
            "TABLE_ID": "mobility_report",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/covid19_google_mobility/mobility_report/data_output.csv",
            "SCHEMA_PATH": "data/covid19_google_mobility/schema/covid19_google_mobility_mobility_report_schema.json",
            "DROP_DEST_TABLE": "Y",
            "INPUT_FIELD_DELIMITER": ",",
            "REMOVE_SOURCE_FILE": "Y",
            "DELETE_TARGET_FILE": "Y",
            "INPUT_CSV_HEADERS": '[\n  "country_region_code",\n  "country_region",\n  "sub_region_1",\n  "sub_region_2",\n  "metro_area",\n  "iso_3166_2_code",\n  "census_fips_code",\n  "place_id",\n  "date",\n  "retail_and_recreation_percent_change_from_baseline",\n  "grocery_and_pharmacy_percent_change_from_baseline",\n  "parks_percent_change_from_baseline",\n  "transit_stations_percent_change_from_baseline",\n  "workplaces_percent_change_from_baseline",\n  "residential_percent_change_from_baseline"\n]',
            "DATA_DTYPES": '{\n  "country_region_code": "str",\n  "country_region": "str",\n  "sub_region_1": "str",\n  "sub_region_2": "str",\n  "metro_area": "str",\n  "iso_3166_2_code": "str",\n  "census_fips_code": "str",\n  "place_id": "str",\n  "date": "str",\n  "retail_and_recreation_percent_change_from_baseline": "str",\n  "grocery_and_pharmacy_percent_change_from_baseline": "str",\n  "parks_percent_change_from_baseline": "str",\n  "transit_stations_percent_change_from_baseline": "str",\n  "workplaces_percent_change_from_baseline": "str",\n  "residential_percent_change_from_baseline": "str"\n}',
            "RENAME_HEADERS_LIST": '{\n  "country_region_code": "country_region_code",\n  "country_region": "country_region",\n  "sub_region_1": "sub_region_1",\n  "sub_region_2": "sub_region_2",\n  "metro_area": "metro_area",\n  "iso_3166_2_code": "iso_3166_2_code",\n  "census_fips_code": "census_fips_code",\n  "place_id": "place_id",\n  "date":"date",\n  "retail_and_recreation_percent_change_from_baseline": "retail_and_recreation_percent_change_from_baseline",\n  "grocery_and_pharmacy_percent_change_from_baseline": "grocery_and_pharmacy_percent_change_from_baseline",\n  "parks_percent_change_from_baseline": "parks_percent_change_from_baseline",\n  "transit_stations_percent_change_from_baseline": "transit_stations_percent_change_from_baseline",\n  "workplaces_percent_change_from_baseline": "workplaces_percent_change_from_baseline",\n  "residential_percent_change_from_baseline":"residential_percent_change_from_baseline"\n}',
            "TABLE_DESCRIPTION": " Terms of use By downloading or using the data, you agree to Google's Terms of Service: https://policies.google.com/terms Description This dataset aims to provide insights into what has changed in response to policies aimed at combating COVID-19. It reports movement trends over time by geography, across different categories of places such as retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential. This dataset is intended to help remediate the impact of COVID-19. It shouldn’t be used for medical diagnostic, prognostic, or treatment purposes. It also isn’t intended to be used for guidance on personal travel plans. To learn more about the dataset, the place categories and how we calculate these trends and preserve privacy, read the data documentation: https://www.google.com/covid19/mobility/data_documentation.html ",
        },
        resources={
            "request_memory": "32G",
            "request_cpu": "2",
            "request_ephemeral_storage": "28G",
        },
    )

    mobility_report
