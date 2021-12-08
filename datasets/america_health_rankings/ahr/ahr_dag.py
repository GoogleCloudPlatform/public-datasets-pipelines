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
    dag_id="america_health_rankings.ahr",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    ahr_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="ahr_transform_csv",
        startup_timeout_seconds=600,
        name="america_health_rankings_ahr",
        namespace="default",
        affinity={
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "cloud.google.com/gke-nodepool",
                                    "operator": "In",
                                    "values": ["pool-e2-standard-4"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        image_pull_policy="Always",
        image="{{ var.json.america_health_rankings.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://assets.americashealthrankings.org/app/uploads/ahr_heath-disparities_data.xlsx",
            "SOURCE_FILE": "files/data.xlsx",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/america_health_rankings/ahr/data_output.csv",
            "CSV_HEADERS": '["edition","report_type","measure_name","state_name","subpopulation","value","lower_ci","upper_ci","source","source_date"]',
            "RENAME_MAPPINGS": '{"Edition": "edition","Report Type": "report_type","Measure Name": "measure_name","State Name": "state_name","Subpopulation": "subpopulation","Value": "value","Lower CI": "lower_ci","Upper CI": "upper_ci","Source": "source","Source Date": "source_date"}',
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_ahr_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_ahr_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/america_health_rankings/ahr/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="america_health_rankings.ahr",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "edition", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "report_type", "type": "STRING", "mode": "NULLABLE"},
            {"name": "measure_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "state_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "subpopulation", "type": "STRING", "mode": "NULLABLE"},
            {"name": "value", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "lower_ci", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "upper_ci", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "source", "type": "STRING", "mode": "NULLABLE"},
            {"name": "source_date", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    ahr_transform_csv >> load_ahr_to_bq
