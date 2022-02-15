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
    dag_id="race_and_economic_opportunity.intergenerational_transition_matrices_of_educational_attainment_by_race_and_gender",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transition_matrices_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="transition_matrices_transform_csv",
        startup_timeout_seconds=600,
        name="race_and_economic_opportunity_intergenerational_transition_matrices_of_educational_attainment_by_race_and_gender",
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
        image="{{ var.json.race_and_economic_opportunity.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www2.census.gov/ces/opportunity/table_7.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/race_and_economic_opportunity/intergenerational_transition_matrices_of_educational_attainment_by_race_and_gender/data_output.csv",
            "CSV_HEADERS": '["kid_race","gender","count","kid_edu1","kid_edu2","kid_edu3","kid_edu4","par_edu1","par_edu2","par_edu3","par_edu4","kid_edu1_cond_par_edu1","kid_edu1_cond_par_edu2","kid_edu1_cond_par_edu3","kid_edu1_cond_par_edu4","kid_edu2_cond_par_edu1","kid_edu2_cond_par_edu2","kid_edu2_cond_par_edu3","kid_edu2_cond_par_edu4","kid_edu3_cond_par_edu1","kid_edu3_cond_par_edu2","kid_edu3_cond_par_edu3","kid_edu3_cond_par_edu4","kid_edu4_cond_par_edu1","kid_edu4_cond_par_edu2","kid_edu4_cond_par_edu3","kid_edu4_cond_par_edu4"]',
            "RENAME_MAPPINGS": '{"kid_race": "kid_race","gender": "gender","count": "count","kid_edu1": "kid_edu1","kid_edu2": "kid_edu2","kid_edu3": "kid_edu3","kid_edu4": "kid_edu4","par_edu1": "par_edu1","par_edu2": "par_edu2","par_edu3": "par_edu3","par_edu4": "par_edu4","kid_edu1_cond_par_edu1": "kid_edu1_cond_par_edu1","kid_edu1_cond_par_edu2": "kid_edu1_cond_par_edu2","kid_edu1_cond_par_edu3": "kid_edu1_cond_par_edu3","kid_edu1_cond_par_edu4": "kid_edu1_cond_par_edu4","kid_edu2_cond_par_edu1": "kid_edu2_cond_par_edu1","kid_edu2_cond_par_edu2": "kid_edu2_cond_par_edu2","kid_edu2_cond_par_edu3": "kid_edu2_cond_par_edu3","kid_edu2_cond_par_edu4": "kid_edu2_cond_par_edu4","kid_edu3_cond_par_edu1": "kid_edu3_cond_par_edu1","kid_edu3_cond_par_edu2": "kid_edu3_cond_par_edu2","kid_edu3_cond_par_edu3": "kid_edu3_cond_par_edu3","kid_edu3_cond_par_edu4": "kid_edu3_cond_par_edu4","kid_edu4_cond_par_edu1": "kid_edu4_cond_par_edu1","kid_edu4_cond_par_edu2": "kid_edu4_cond_par_edu2","kid_edu4_cond_par_edu3": "kid_edu4_cond_par_edu3","kid_edu4_cond_par_edu4": "kid_edu4_cond_par_edu4"}',
            "PIPELINE_NAME": "intergenerational_transition_matrices_of_educational_attainment_by_race_and_gender",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_transition_matrices_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_transition_matrices_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/race_and_economic_opportunity/intergenerational_transition_matrices_of_educational_attainment_by_race_and_gender/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="race_and_economic_opportunity.intergenerational_transition_matrices_of_educational_attainment_by_race_and_gender",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "kid_race", "type": "STRING", "mode": "NULLABLE"},
            {"name": "gender", "type": "STRING", "mode": "NULLABLE"},
            {"name": "count", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "kid_edu1", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu2", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu3", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu4", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "par_edu1", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "par_edu2", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "par_edu3", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "par_edu4", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu1_cond_par_edu1", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu1_cond_par_edu2", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu1_cond_par_edu3", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu1_cond_par_edu4", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu2_cond_par_edu1", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu2_cond_par_edu2", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu2_cond_par_edu3", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu2_cond_par_edu4", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu3_cond_par_edu1", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu3_cond_par_edu2", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu3_cond_par_edu3", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu3_cond_par_edu4", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu4_cond_par_edu1", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu4_cond_par_edu2", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu4_cond_par_edu3", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_edu4_cond_par_edu4", "type": "FLOAT", "mode": "NULLABLE"},
        ],
    )

    transition_matrices_transform_csv >> load_transition_matrices_to_bq
