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
    dag_id="news_hatecrimes.hatecrimes",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    hatecrimes_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="hatecrimes_transform_csv",
        startup_timeout_seconds=600,
        name="hatecrimes",
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
        image="{{ var.json.news_hatecrimes.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://raw.githubusercontent.com/GoogleTrends/data/master/Documenting_Hate_latest.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/news_hatecrimes/hatecrimes/data_output.csv",
            "PIPELINE_NAME": "hatecrimes",
            "CSV_HEADERS": '["date","title","organization","city","state","url","keyword","summary"]',
            "RENAME_MAPPINGS": '{"Date":"date","Title":"title","Organization":"organization","City":"city","State":"state","URL":"url","Keyword":"keyword","Summary":"summary"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_hatecrimes_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_hatecrimes_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/news_hatecrimes/hatecrimes/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="news_hatecrimes.hatecrimes",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "date", "type": "timestamp", "mode": "nullable"},
            {"name": "title", "type": "string", "mode": "nullable"},
            {"name": "organization", "type": "string", "mode": "nullable"},
            {"name": "city", "type": "string", "mode": "nullable"},
            {"name": "state", "type": "string", "mode": "nullable"},
            {"name": "url", "type": "string", "mode": "nullable"},
            {"name": "keyword", "type": "string", "mode": "nullable"},
            {"name": "summary", "type": "string", "mode": "nullable"},
        ],
    )

    hatecrimes_transform_csv >> load_hatecrimes_to_bq
