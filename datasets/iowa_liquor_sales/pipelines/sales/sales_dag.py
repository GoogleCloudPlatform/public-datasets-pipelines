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

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-10-17",
}


with DAG(
    dag_id="iowa_liquor_sales.sales",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:

    # Download data
    bash_download = bash.BashOperator(
        task_id="bash_download",
        bash_command="wget -O /home/airflow/gcs/data/iowa_liquor_sales/raw_files/data.csv https://data.iowa.gov/api/views/m3tr-qhgy/rows.csv",
    )

    # Download data
    bash_split = bash.BashOperator(
        task_id="bash_split",
        bash_command="split -d -l 4000000 /home/airflow/gcs/data/iowa_liquor_sales/raw_files/data.csv /home/airflow/gcs/data/iowa_liquor_sales/raw_files/split_data_",
    )

    bash_download >> bash_split
