# Copyright 2022 Google LLC
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
from airflow.providers.google.cloud.transfers import gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="human_variant_annotation.clinvar",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    clinvar_vcf_grch37 = kubernetes_pod.KubernetesPodOperator(
        task_id="clinvar_vcf_grch37",
        startup_timeout_seconds=600,
        name="name_basics",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.human_variant_annotation.container_registry.run_csv_transform_kub }}",
        env_vars={
            "BASE_URL": "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/",
            "FOLDER": "vcf_GRCh37",
            "VERSION": "2.0",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_FOLDER": "data/human_variant_annotation/clinVar-vcf_GRCh37/",
            "PIPELINE": "clinvar",
        },
    )

    # Task to run a GoogleCloudStorageToGoogleCloudStorageOperator
    copy_clinvar_v1_to_gcs_destination_bucket = gcs_to_gcs.GCSToGCSOperator(
        task_id="copy_clinvar_v1_to_gcs_destination_bucket",
        source_bucket="{{ var.value.composer_bucket }}",
        source_object="data/human_variant_annotation/clinVar-vcf_GRCh37/*",
        destination_bucket="{{ var.json.human_variant_annotation.destination_bucket }}",
        destination_object="human-variant-annotation/clinVar-vcf_GRCh37/",
        move_object=False,
        replace=False,
    )

    # Run CSV transform within kubernetes pod
    clinvar_vcf_grch38 = kubernetes_pod.KubernetesPodOperator(
        task_id="clinvar_vcf_grch38",
        startup_timeout_seconds=600,
        name="name_basics",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.human_variant_annotation.container_registry.run_csv_transform_kub }}",
        env_vars={
            "BASE_URL": "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/",
            "FOLDER": "vcf_GRCh38",
            "VERSION": "2.0",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_FOLDER": "data/human_variant_annotation/clinVar-vcf_GRCh38/",
            "PIPELINE": "db_snp",
        },
    )

    # Task to run a GoogleCloudStorageToGoogleCloudStorageOperator
    copy_clinvar_v2_to_gcs_destination_bucket = gcs_to_gcs.GCSToGCSOperator(
        task_id="copy_clinvar_v2_to_gcs_destination_bucket",
        source_bucket="{{ var.value.composer_bucket }}",
        source_object="data/human_variant_annotation/clinVar-vcf_GRCh38/*",
        destination_bucket="{{ var.json.human_variant_annotation.destination_bucket }}",
        destination_object="human-variant-annotation/clinVar-vcf_GRCh38/",
        move_object=False,
        replace=False,
    )

    clinvar_vcf_grch37 >> copy_clinvar_v1_to_gcs_destination_bucket
    clinvar_vcf_grch38 >> copy_clinvar_v2_to_gcs_destination_bucket
