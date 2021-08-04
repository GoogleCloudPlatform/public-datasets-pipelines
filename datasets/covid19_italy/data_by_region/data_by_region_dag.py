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
from airflow.contrib.operators import gcs_to_bq, kubernetes_pod_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="covid19_italy.data_by_region",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    covid19_italy_data_by_region_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="covid19_italy_data_by_region_transform_csv",
        startup_timeout_seconds=600,
        name="covid19_italy_data_by_region",
        namespace="default",
        image_pull_policy="Always",
        image="{{ var.json.covid19_italy_data_by_region.container_registry.run_csv_transform_kub_data_by_region }}",
        env_vars={
            "SOURCE_URL": "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.json.shared.composer_bucket }}",
            "TARGET_GCS_PATH": "data/covid19_italy/data_by_region/data_output.csv",
        },
        resources={"limit_memory": "4G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_covid19_italy_data_by_region_to_bq = (
        gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
            task_id="load_covid19_italy_data_by_region_to_bq",
            bucket="{{ var.json.shared.composer_bucket }}",
            source_objects=["data/covid19_italy/data_by_region/data_output.csv"],
            source_format="CSV",
            destination_project_dataset_table="covid19_italy.data_by_region",
            skip_leading_rows=1,
            write_disposition="WRITE_TRUNCATE",
            schema_fields=[
                {"name": "date", "type": "TIMESTAMP", "mode": "NULLABLE"},
                {"name": "country", "type": "STRING", "mode": "NULLABLE"},
                {"name": "region_code", "type": "STRING", "mode": "NULLABLE"},
                {"name": "region_name", "type": "STRING", "mode": "NULLABLE"},
                {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
                {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
                {"name": "location_geom", "type": "GEOGRAPHY", "mode": "NULLABLE"},
                {
                    "name": "hospitalized_patients_symptoms",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {
                    "name": "hospitalized_patients_intensive_care",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {
                    "name": "total_hospitalized_patients",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {
                    "name": "home_confinement_cases",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {
                    "name": "total_current_confirmed_cases",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {
                    "name": "new_current_confirmed_cases",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {
                    "name": "new_total_confirmed_cases",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {"name": "recovered", "type": "INTEGER", "mode": "NULLABLE"},
                {"name": "deaths", "type": "INTEGER", "mode": "NULLABLE"},
                {
                    "name": "total_confirmed_cases",
                    "type": "INTEGER",
                    "mode": "NULLABLE",
                },
                {"name": "tests_performed", "type": "INTEGER", "mode": "NULLABLE"},
                {"name": "note", "type": "STRING", "mode": "NULLABLE"},
            ],
        )
    )

    covid19_italy_data_by_region_transform_csv >> load_covid19_italy_data_by_region_to_bq
