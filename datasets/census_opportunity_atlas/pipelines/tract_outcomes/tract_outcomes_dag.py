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
    dag_id="census_opportunity_atlas.tract_outcomes",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="tract_outcomes",
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
        image="{{ var.json.census_opportunity_atlas.container_registry.run_csv_transform_kub_tract_outcomes }}",
        env_vars={
            "SOURCE_URL": "https://opportunityinsights.org/wp-content/uploads/2018/10/tract_outcomes.zip",
            "SOURCE_FILE": "files/data.csv",
            "SOURCE_FILE_UNZIPPED": "files/tract_outcomes_early.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "50000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/census_opportunity_atlas/tract_outcomes/files/data_output.csv",
            "ENGLISH_PIPELINE_NAME": "Census Opportunity Atlas - Tract Outcomes",
            "resources": None,
            "limit_memory": "4G",
            "limit_cpu": "1",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/census_opportunity_atlas/tract_outcomes/files/data_output.csv"
        ],
        schema_object="data/census_opportunity_atlas/tract_outcomes/schema.json",
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.census_opportunity_atlas.container_registry.tract_outcomes_destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
    )

    transform_csv >> load_to_bq
