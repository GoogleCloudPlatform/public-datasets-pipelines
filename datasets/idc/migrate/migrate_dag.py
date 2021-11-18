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
from airflow.providers.google.cloud.transfers import gcs_to_gcs

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="idc.idc_tcia_transfer_bq_data",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Transfer IDC Databases
    transfer_idc_db = kubernetes_pod.KubernetesPodOperator(
        task_id="transfer_idc_db",
        name="transfer_idc",
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
        image="{{ var.json.idc.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_PROJECT_ID": "{{ var.json.idc.container_registry.source_project }}",
            "SOURCE_DATASET_LIST": '[ "idc_v1", "idc_v2", "idc_v3", "idc_v4", "idc_v5" ]',
            "TARGET_PROJECT_ID": "{{ var.json.idc.container_registry.destination_project_id }}",
            "USER_ID": "{{ var.json.idc.container_registry.impersonation_account }}",
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Task to run a GoogleCloudStorageToGoogleCloudStorageOperator
    transfer_image_files = gcs_to_gcs.GCSToGCSOperator(
        task_id="transfer_image_files",
        source_bucket="{{ var.json.idc.source_bucket }}",
        source_object="{{ var.json.idc.source_object }}",
        destination_bucket="{{ var.json.idc.destination_bucket }}",
        destination_object="{{ var.json.idc.destination_path }}",
        move_object=False,
        replace=False,
        impersonation_chain="{{ var.json.idc.impersonation_account }}",
    )

    transfer_idc_v1_db >> transfer_image_files
