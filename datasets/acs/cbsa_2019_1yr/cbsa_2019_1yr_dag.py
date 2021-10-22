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
    dag_id="acs.cbsa_2019_1yr",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    cbsa_2019_1yr_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="cbsa_2019_1yr_transform_csv",
        startup_timeout_seconds=600,
        name="cbsa_2019_1yr",
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
        image="{{ var.json.acs.container_registry.run_csv_transform_kub_national_level }}",
        env_vars={
            "YEAR_REPORT": "1",
            "API_NAMING_CONVENTION": "combined%20statistical%20area",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/acs/cbsa_2019_1yr/data_output.csv",
            "PIPELINE_NAME": "cbsa_2019_1yr",
            "RENAME_MAPPINGS": '{0:"name", 1:"KPI_Value", 2:"state", 3:"county", "group_id":"KPI_Name"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_cbsa_2019_1yr_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_cbsa_2019_1yr_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/acs/cbsa_2019_1yr/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="acs.cbsa_2019_1yr",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "name", "type": "string", "mode": "nullable"},
            {"name": "KPI_Value", "type": "float", "mode": "nullable"},
            {"name": "combined_statistical_area", "type": "string", "mode": "nullable"},
            {"name": "KPI_Name", "type": "string", "mode": "nullable"},
        ],
    )

    cbsa_2019_1yr_transform_csv >> load_cbsa_2019_1yr_to_bq
