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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="decennial_census_quick_facts.united_states_census_bureau",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    facts_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="facts_transform_csv",
        startup_timeout_seconds=600,
        name="decennial_census_quick_facts_united_states_census_bureau",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.decennial_census_quick_facts.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://public-datasets-dev-decennial-census-quick-facts/QuickFacts_Dec-23-2021.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/decennial_census_quick_facts/united_states_census_bureau/data_output.csv",
            "CSV_HEADERS": '["fact","fact_note","united_states","value_note_for_united_states"]',
            "RENAME_MAPPINGS": '{"Fact": "fact","Fact Note": "fact_note","United States": "united_states","Value Note for United States": "value_note_for_united_states"}',
            "PIPELINE_NAME": "united_states_census_bureau",
        },
        resources={
            "limit_memory": "2G",
            "limit_cpu": "1",
            "request_ephemeral_storage": "8G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_facts_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_facts_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/decennial_census_quick_facts/united_states_census_bureau/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="decennial_census_quick_facts.united_states_census_bureau",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "fact", "type": "STRING", "mode": "NULLABLE"},
            {"name": "fact_note", "type": "STRING", "mode": "NULLABLE"},
            {"name": "united_states", "type": "STRING", "mode": "NULLABLE"},
            {
                "name": "value_note_for_united_states",
                "type": "STRING",
                "mode": "NULLABLE",
            },
        ],
    )

    facts_transform_csv >> load_facts_to_bq
