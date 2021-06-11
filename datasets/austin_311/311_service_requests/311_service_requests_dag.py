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
from airflow.operators import bash_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="austin_311.311_service_requests",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@hourly",
    catchup=False,
    default_view="graph",
) as dag:

    # Download source CSV file for austin 311 service requests data table
    austin_311_service_requests_download_csv = bash_operator.BashOperator(
        task_id="austin_311_service_requests_download_csv",
        bash_command="mkdir -p $airflow_home/data/$dataset/$pipeline\ncurl -o $airflow_home/data/$dataset/$pipeline/data.csv -L $csv_source_url\n",
        env={
            "airflow_home": "{{ var.json.shared.airflow_home }}",
            "dataset": "austin_311",
            "pipeline": "311_service_requests",
            "csv_source_url": "https://data.austintexas.gov/api/views/i26j-ai4z/rows.csv?accessType=DOWNLOAD",
        },
    )

    austin_311_service_requests_download_csv
