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
    dag_id="vqa.vqa",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Run VQA annotations load processes
    extract_annotations = kubernetes_pod.KubernetesPodOperator(
        task_id="extract_annotations",
        name="vqa.extract_annotations",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.vqa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "Extract Annotations",
            "SOURCE_URL": '[\n  [\n    "Training annotations 2017 v2.0",\n    "https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Train_mscoco.zip",\n    "training_ann_2017",\n    "data/vqa/schema/vqa_annotations_schema.json",\n    "data/vqa/schema/vqa_annotations_detail_schema.json",\n    [ "v2_mscoco_train2014_annotations.json" ]\n  ],\n  [\n    "Validation annotations 2017 v2.0",\n    "https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Val_mscoco.zip",\n    "validation_ann_2017",\n    "data/vqa/schema/vqa_annotations_schema.json",\n    "data/vqa/schema/vqa_annotations_detail_schema.json",\n    [ "v2_mscoco_val2014_annotations.json" ]\n  ]\n]',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "1000000",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "vqa",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/vqa/data_output.csv",
            "DROP_DEST_TABLE": "N",
            "REMOVE_SOURCE_FILE": "Y",
            "DELETE_TARGET_FILE": "Y",
            "REORDER_HEADERS_LIST": '[\n  "data_subtype",\n  "data_type",\n  "info_description",\n  "info_url",\n  "info_version",\n  "info_year",\n  "info_contributor",\n  "info_date_created",\n  "license_url",\n  "license_name"\n]',
            "DETAIL_DATA_HEADERS_LIST": '[\n  "question_type",\n  "multiple_choice_answer",\n  "answer_type",\n  "question_id"\n]',
        },
        resources={"limit_memory": "16G", "limit_cpu": "3"},
    )

    # Run VQA questions load processes
    extract_questions = kubernetes_pod.KubernetesPodOperator(
        task_id="extract_questions",
        name="vqa.extract_questions",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.vqa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "Extract Questions",
            "SOURCE_URL": '[\n  [\n    "Testing questions 2017 v2.0",\n    "https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Test_mscoco.zip",\n    "testing_questions_2017",\n    "data/vqa/schema/vqa_questions_schema.json",\n    "data/vqa/schema/vqa_questions_detail_schema.json",\n    [\n      "v2_OpenEnded_mscoco_test2015_questions.json",\n      "v2_OpenEnded_mscoco_test-dev2015_questions.json"\n    ]\n  ],\n  [\n    "Training questions 2017 v2.0",\n    "https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Train_mscoco.zip",\n    "training_questions_2017",\n    "data/vqa/schema/vqa_questions_schema.json",\n    "data/vqa/schema/vqa_questions_detail_schema.json",\n    [\n      "v2_OpenEnded_mscoco_train2014_questions.json"\n    ]\n  ],\n  [\n    "Validation questions 2017 v2.0",\n    "https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Val_mscoco.zip",\n    "validation_questions_2017",\n    "data/vqa/schema/vqa_questions_schema.json",\n    "data/vqa/schema/vqa_questions_detail_schema.json",\n    [ "v2_OpenEnded_mscoco_val2014_questions.json" ]\n  ]\n]',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "1000000",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "vqa",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/vqa/data_output.csv",
            "DROP_DEST_TABLE": "N",
            "REMOVE_SOURCE_FILE": "Y",
            "DELETE_TARGET_FILE": "Y",
            "REORDER_HEADERS_LIST": '[\n  "task_type",\n  "data_type",\n  "data_subtype",\n  "info_description",\n  "info_url",\n  "info_version",\n  "info_year",\n  "info_contributor",\n  "info_date_created",\n  "license_url",\n  "license_name"\n]',
            "DETAIL_DATA_HEADERS_LIST": '[\n  "image_id",\n  "question",\n  "question_id"\n]',
        },
        resources={"limit_memory": "16G", "limit_cpu": "3"},
    )

    # Run VQA complimentary pairs load processes
    extract_complementary_pairs = kubernetes_pod.KubernetesPodOperator(
        task_id="extract_complementary_pairs",
        name="vqa.extract_complementary_pairs",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.vqa.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE_NAME": "Extract Complimentary Pairs",
            "SOURCE_URL": '[\n  [\n    "Training complementary pairs",\n    "https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Complementary_Pairs_Train_mscoco.zip",\n    "training_complimentary_pairs",\n    "data/vqa/schema/vqa_complementary_pairs_schema.json",\n    "",\n    [\n      "v2_mscoco_train2014_complementary_pairs.json"\n    ]\n  ],\n  [\n    "Validation complementary pairs",\n    "https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Complementary_Pairs_Val_mscoco.zip",\n    "validation_complimentary_pairs",\n    "data/vqa/schema/vqa_complementary_pairs_schema.json",\n    "",\n    [\n      "v2_mscoco_val2014_complementary_pairs.json"\n    ]\n  ]\n]',
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "1000000",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "vqa",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/vqa/data_output.csv",
            "SCHEMA_PATH": "data/vqa/schema/complementary_pairs_schema.json",
            "DROP_DEST_TABLE": "N",
            "REMOVE_SOURCE_FILE": "Y",
            "DELETE_TARGET_FILE": "Y",
            "REORDER_HEADERS_LIST": '[\n  "question_id_1",\n  "question_id_2"\n]',
        },
        resources={"limit_memory": "16G", "limit_cpu": "3"},
    )

    extract_annotations >> extract_questions >> extract_complementary_pairs
