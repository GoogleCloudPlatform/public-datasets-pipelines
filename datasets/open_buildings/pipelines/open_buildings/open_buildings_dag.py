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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-09-02",
}


with DAG(
    dag_id="open_buildings.open_buildings",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@yearly",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="gsutil cp -R gs://open-buildings-data/v1/polygons_s2_level_4_gzip gs://{{ var.value.composer_bucket }}/data/open_buildings/source_files/",
    )

    # Unzip data
    batch1_bash_gunzip = bash.BashOperator(
        task_id="batch1_bash_gunzip",
        bash_command="gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/025_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/04f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/05b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/093_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/095_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0c3_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0c5_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0c7_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0d1_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0d7_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0d9_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0db_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0dd_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0df_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0e1_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0e3_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0e5_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0e7_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0e9_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0eb_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0ed_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0ef_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0f1_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0f9_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0fb_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0fd_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/0ff_buildings.csv.gz ; ",
    )

    # Unzip data
    batch2_bash_gunzip = bash.BashOperator(
        task_id="batch2_bash_gunzip",
        bash_command="gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/103_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/105_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/107_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/109_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/10b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/10d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/10f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/111_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/113_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/117_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/119_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/11b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/11d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/11f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/121_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/123_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/125_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/127_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/129_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/12f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/131_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/137_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/139_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/13b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/13d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/141_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/143_buildings.csv.gz ; ",
    )

    # Unzip data
    batch3_bash_gunzip = bash.BashOperator(
        task_id="batch3_bash_gunzip",
        bash_command="gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/145_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/147_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/149_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/14f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/15b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/15d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/161_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/163_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/165_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/167_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/169_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/16b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/16d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/16f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/171_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/173_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/175_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/177_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/179_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/17b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/17d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/17f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/181_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/183_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/185_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/189_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/18b_buildings.csv.gz ; ",
    )

    # Unzip data
    batch4_bash_gunzip = bash.BashOperator(
        task_id="batch4_bash_gunzip",
        bash_command="gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/18d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/18f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/191_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/193_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/195_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/197_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/199_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/19b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/19d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/19f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1a1_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1a3_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1a5_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1a7_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1a9_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1b9_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1bb_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1bd_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1bf_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1c1_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1c3_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1c5_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1c7_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1dd_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1e5_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1e7_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1e9_buildings.csv.gz ; ",
    )

    # Unzip data
    batch5_bash_gunzip = bash.BashOperator(
        task_id="batch5_bash_gunzip",
        bash_command="gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1eb_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1ed_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1ef_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1f1_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1f3_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1f5_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/1f7_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/217_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/219_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/21d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/21f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/221_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/223_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/225_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/227_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/22f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/231_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/233_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/23b_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/23d_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/23f_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/3d1_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/3d5_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/3d7_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/3d9_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/3db_buildings.csv.gz ; gunzip -f -v -k /home/airflow/gcs/data/open_buildings/source_files/polygons_s2_level_4_gzip/b5b_buildings.csv.gz ; ",
    )

    # ETL within the kubernetes pod
    py_gcs_to_bq = kubernetes_pod.KubernetesPodOperator(
        task_id="py_gcs_to_bq",
        startup_timeout_seconds=1000,
        name="load_data",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.open_buildings.container_registry.run_script_kub }}",
        env_vars={
            "SOURCE_GCS_PATH": "{{ var.json.open_buildings.source_gcs_path }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.open_buildings.dataset_id }}",
            "GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SCHEMA_FILEPATH": "schema.json",
        },
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    (
        bash_gcs_to_gcs
        >> batch1_bash_gunzip
        >> batch2_bash_gunzip
        >> batch3_bash_gunzip
        >> batch4_bash_gunzip
        >> batch5_bash_gunzip
        >> py_gcs_to_bq
    )
