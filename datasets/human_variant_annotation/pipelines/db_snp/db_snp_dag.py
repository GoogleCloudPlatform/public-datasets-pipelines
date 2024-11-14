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
from airflow.operators import bash
from airflow.providers.google.cloud.transfers import gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="human_variant_annotation.db_snp",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to download files from FTP to GCS
    download_dbsnp_v1_files = bash.BashOperator(
        task_id="download_dbsnp_v1_files",
        bash_command="mkdir -p $data_dir\nmkdir -p $data_dir/$target_dir\nwget -P $data_dir/$target_dir/ $source_url_2017\nwget -P $data_dir/$target_dir/ $source_url_2018\n",
        env={
            "data_dir": "/home/airflow/gcs/data/human_variant_annotation",
            "target_dir": "dbSNP-human_9606_b150_GRCh37p13",
            "source_url_2017": "https://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b150_GRCh37p13/VCF/All_20170710.vcf.gz",
            "source_url_2018": "https://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b151_GRCh37p13/VCF/All_20180423.vcf.gz",
        },
    )

    # Task to run a GCS to GCS
    copy_dbsnp_v1_to_gcs_destination_bucket = gcs_to_gcs.GCSToGCSOperator(
        task_id="copy_dbsnp_v1_to_gcs_destination_bucket",
        source_bucket="{{ var.value.composer_bucket }}",
        source_object="data/human_variant_annotation/dbSNP-human_9606_b150_GRCh37p13/*",
        destination_bucket="{{ var.json.human_variant_annotation.destination_bucket }}",
        destination_object="human-variant-annotation/dbSNP-human_9606_b150_GRCh37p13/",
        move_object=False,
        replace=False,
    )

    # Task to download files from FTP to GCS
    download_dbsnp_v2_files = bash.BashOperator(
        task_id="download_dbsnp_v2_files",
        bash_command="mkdir -p $data_dir\nmkdir -p $data_dir/$target_dir\nwget -P $data_dir/$target_dir/ $source_url_2017\nwget -P $data_dir/$target_dir/ $source_url_2018\n",
        env={
            "data_dir": "/home/airflow/gcs/data/human_variant_annotation",
            "target_dir": "dbSNP-human_9606_b150_GRCh38p7",
            "source_url_2017": "https://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b150_GRCh38p7/VCF/All_20170710.vcf.gz",
            "source_url_2018": "https://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b151_GRCh38p7/VCF/All_20180418.vcf.gz",
        },
    )

    # Task to run a GCS to GCS
    copy_dbsnp_v2_to_gcs_destination_bucket = gcs_to_gcs.GCSToGCSOperator(
        task_id="copy_dbsnp_v2_to_gcs_destination_bucket",
        source_bucket="{{ var.value.composer_bucket }}",
        source_object="data/human_variant_annotation/dbSNP-human_9606_b150_GRCh38p7/*",
        destination_bucket="{{ var.json.human_variant_annotation.destination_bucket }}",
        destination_object="human-variant-annotation/dbSNP-human_9606_b150_GRCh38p7/",
        move_object=False,
        replace=False,
    )

    download_dbsnp_v1_files >> copy_dbsnp_v1_to_gcs_destination_bucket
    download_dbsnp_v2_files >> copy_dbsnp_v2_to_gcs_destination_bucket
