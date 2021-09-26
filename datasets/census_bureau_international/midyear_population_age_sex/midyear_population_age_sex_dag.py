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
    dag_id="census_bureau_international.midyear_population_age_sex",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    midyear_population_age_sex_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="midyear_population_age_sex_transform_csv",
        startup_timeout_seconds=600,
        name="midyear_population_age_sex",
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
        image="{{ var.json.census_bureau_international.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '["gs://pdp-feeds-staging/Census/idbzip/IDBext194.csv","gs://pdp-feeds-staging/Census/idbzip/IDBextCTYS.csv"]',
            "SOURCE_FILE": '["files/data1.csv","files/data2.csv"]',
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/census_bureau_international/midyear_population_age_sex/data_output.csv",
            "PIPELINE_NAME": "midyear_population_age_sex",
            "FILE_PATH": "files/",
            "CSV_HEADERS": '["country_code","country_name","year","sex","max_age","population_age_0","population_age_1","population_age_2","population_age_3","population_age_4","population_age_5","population_age_6","population_age_7","population_age_8","population_age_9","population_age_10","population_age_11","population_age_12","population_age_13","population_age_14","population_age_15","population_age_16","population_age_17","population_age_18","population_age_19","population_age_20","population_age_21","population_age_22","population_age_23","population_age_24","population_age_25","population_age_26","population_age_27","population_age_28","population_age_29","population_age_30","population_age_31","population_age_32","population_age_33","population_age_34","population_age_35","population_age_36","population_age_37","population_age_38","population_age_39","population_age_40","population_age_41","population_age_42","population_age_43","population_age_44","population_age_45","population_age_46","population_age_47","population_age_48","population_age_49","population_age_50","population_age_51","population_age_52","population_age_53","population_age_54","population_age_55","population_age_56","population_age_57","population_age_58","population_age_59","population_age_60","population_age_61","population_age_62","population_age_63","population_age_64","population_age_65","population_age_66","population_age_67","population_age_68","population_age_69","population_age_70","population_age_71","population_age_72","population_age_73","population_age_74","population_age_75","population_age_76","population_age_77","population_age_78","population_age_79","population_age_80","population_age_81","population_age_82","population_age_83","population_age_84","population_age_85","population_age_86","population_age_87","population_age_88","population_age_89","population_age_90","population_age_91","population_age_92","population_age_93","population_age_94","population_age_95","population_age_96","population_age_97","population_age_98","population_age_99","population_age_100"]',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_midyear_population_age_sex_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_midyear_population_age_sex_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/census_bureau_international/midyear_population_age_sex/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="census_bureau_international.midyear_population_age_sex",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "country_code", "type": "STRING", "mode": "REQUIRED"},
            {"name": "country_name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "year", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "sex", "type": "STRING", "mode": "NULLABLE"},
            {"name": "max_age", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_0", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_1", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_2", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_3", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_4", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_5", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_6", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_7", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_8", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_9", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_10", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_11", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_12", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_13", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_14", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_15", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_16", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_17", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_18", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_19", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_20", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_21", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_22", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_23", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_24", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_25", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_26", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_27", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_28", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_29", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_30", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_31", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_32", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_33", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_34", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_35", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_36", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_37", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_38", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_39", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_40", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_41", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_42", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_44", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_45", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_46", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_47", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_48", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_49", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_50", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_51", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_52", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_53", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_54", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_55", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_56", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_57", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_58", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_59", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_60", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_61", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_62", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_63", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_64", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_65", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_66", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_67", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_68", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_69", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_70", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_71", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_72", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_73", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_74", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_75", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_76", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_77", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_78", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_79", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_80", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_81", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_82", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_83", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_84", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_85", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_86", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_87", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_88", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_89", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_90", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_91", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_92", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_93", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_94", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_95", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_96", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_97", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_98", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_99", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "population_age_100", "type": "INTEGER", "mode": "NULLABLE"},
        ],
    )

    midyear_population_age_sex_transform_csv >> load_midyear_population_age_sex_to_bq
