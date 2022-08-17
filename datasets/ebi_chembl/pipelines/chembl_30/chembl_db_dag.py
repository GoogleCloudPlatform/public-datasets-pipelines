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
from airflow.operators import bash
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="ebi_chembl.chembl_db",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to 'start' CloudSQL Database Instance.
    start_db_instance = bash.BashOperator(
        task_id="start_db_instance",
        bash_command="echo $instance_id\ngcloud sql instances patch $instance_id --activation-policy=ALWAYS\n",
        env={"instance_id": "bq-public-datasets-dev-v2"},
    )

    # Run CSV transform within kubernetes pod
    activities_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="activities_transform_csv",
        startup_timeout_seconds=600,
        name="activities",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.ebi_chembl.container_registry.run_csv_transform_kub }}",
        env_vars={
            "TABLES": '["activities"]',
            "CHUNK_SIZE": "100000",
            "OUTPUT_FOLDER": "./files/output",
            "TARGET_GCS_FOLDER": "data/ebi_chembl/chembl_30/output",
            "CHECKS": [
                "os.system('pwd')",
                "os.system('apt-get install sudo')",
                "os.system('sudo apt-get update')",
                "os.system('sudo apt-get install postgres postgresql-contrib -y')",
                "os.system('dpkg -l | grep postgres')",
            ],
        },
        resources={
            "request_memory": "8G",
            "request_cpu": "2",
            "request_ephemeral_storage": "10G",
        },
    )

    activities_transform_csv
