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

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="af_dag_monitoring.af_dag_monitoring",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Send Email Notification Of Failed DAGS
    send_email_notifications = kubernetes_pod.KubernetesPodOperator(
        task_id="send_email_notifications",
        name="send_email_notifications",
        startup_timeout_seconds=600,
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.af_dag_monitoring.container_registry.run_script }}",
        resources={
            "limit_memory": "8G",
            "limit_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
        env_vars={"EMAIL_TO": "nlarge@google.com"},
    )

    send_email_notifications