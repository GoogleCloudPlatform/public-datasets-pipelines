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
    "start_date": "2022-10-27",
}


with DAG(
    dag_id="covid19_symptom_search.covid19_symptom_search",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@yearly",
    catchup=False,
    default_view="graph",
) as dag:

    # Fetch data gcs - gcs
    bash_gcs_to_gcs = bash.BashOperator(
        task_id="bash_gcs_to_gcs",
        bash_command="gsutil cp -R gs://covid-st-prod-datasets-bigquery/ssd_i18n_expansion/ gs://{{ var.value.composer_bucket }}/data/covid19_symptom_search/",
    )

    bash_gcs_to_gcs
