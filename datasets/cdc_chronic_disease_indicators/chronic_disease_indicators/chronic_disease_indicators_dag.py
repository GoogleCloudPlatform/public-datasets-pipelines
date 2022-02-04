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
    dag_id="cdc_chronic_disease_indicators.chronic_disease_indicators",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    chronic_disease_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="chronic_disease_transform_csv",
        startup_timeout_seconds=600,
        name="cdc_chronic_disease_indicators_chronic_disease_indicators",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.cdc_chronic_disease_indicators.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://chronicdata.cdc.gov/resource/g4ie-h725.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/cdc_chronic_disease_indicators/chronic_disease_indicators/data_output.csv",
            "CSV_HEADERS": '["yearstart","yearend","locationabbr","locationdesc","datasource","topic","question","response","datavalueunit","datavaluetype","datavalue","datavaluealt","datavaluefootnotesymbol","datavaluefootnote","lowconfidencelimit","highconfidencelimit","stratificationcategory1","stratification1","stratificationcategory2","stratification2","stratificationcategory3","stratification3","geolocation","responseid","locationid","topicid","questionid","datavaluetypeid","stratificationcategoryid1","stratificationid1","stratificationcategoryid2","stratificationid2","stratificationcategoryid3","stratificationid3"]',
            "RENAME_MAPPINGS": '{"yearstart": "yearstart","yearend": "yearend","locationabbr": "locationabbr","locationdesc": "locationdesc","datasource": "datasource","topic": "topic","question": "question","response": "response","datavalueunit": "datavalueunit","datavaluetype": "datavaluetype","datavalue": "datavalue","datavaluealt": "datavaluealt","datavaluefootnotesymbol": "datavaluefootnotesymbol","datavaluefootnote": "datavaluefootnote","lowconfidencelimit": "lowconfidencelimit","highconfidencelimit": "highconfidencelimit","stratificationcategory1": "stratificationcategory1","stratification1": "stratification1","stratificationcategory2": "stratificationcategory2","stratification2": "stratification2","stratificationcategory3": "stratificationcategory3","stratification3": "stratification3","geolocation": "geolocation","responseid": "responseid","locationid": "locationid","topicid": "topicid","questionid": "questionid","datavaluetypeid": "datavaluetypeid","stratificationcategoryid1": "stratificationcategoryid1","stratificationid1": "stratificationid1","stratificationcategoryid2": "stratificationcategoryid2","stratificationid2": "stratificationid2","stratificationcategoryid3": "stratificationcategoryid3","stratificationid3": "stratificationid3"}',
            "PIPELINE_NAME": "chronic_disease_indicators",
        },
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_chronic_disease_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_chronic_disease_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/cdc_chronic_disease_indicators/chronic_disease_indicators/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="cdc_places.chronic_disease_indicators",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "yearstart", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "yearend", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "locationabbr", "type": "STRING", "mode": "NULLABLE"},
            {"name": "locationdesc", "type": "STRING", "mode": "NULLABLE"},
            {"name": "datasource", "type": "STRING", "mode": "NULLABLE"},
            {"name": "topic", "type": "STRING", "mode": "NULLABLE"},
            {"name": "question", "type": "STRING", "mode": "NULLABLE"},
            {"name": "response", "type": "STRING", "mode": "NULLABLE"},
            {"name": "datavalueunit", "type": "STRING", "mode": "NULLABLE"},
            {"name": "datavaluetype", "type": "STRING", "mode": "NULLABLE"},
            {"name": "datavalue", "type": "STRING", "mode": "NULLABLE"},
            {"name": "datavaluealt", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "datavaluefootnotesymbol", "type": "STRING", "mode": "NULLABLE"},
            {"name": "datavaluefootnote", "type": "STRING", "mode": "NULLABLE"},
            {"name": "lowconfidencelimit", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "highconfidencelimit", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "stratificationcategory1", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratification1", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratificationcategory2", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratification2", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratificationcategory3", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratification3", "type": "STRING", "mode": "NULLABLE"},
            {"name": "geolocation", "type": "GEOGRAPHY", "mode": "NULLABLE"},
            {"name": "responseid", "type": "STRING", "mode": "NULLABLE"},
            {"name": "locationid", "type": "STRING", "mode": "NULLABLE"},
            {"name": "topicid", "type": "STRING", "mode": "NULLABLE"},
            {"name": "questionid", "type": "STRING", "mode": "NULLABLE"},
            {"name": "datavaluetypeid", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratificationcategoryid1", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratificationid1", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratificationcategoryid2", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratificationid2", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratificationcategoryid3", "type": "STRING", "mode": "NULLABLE"},
            {"name": "stratificationid3", "type": "STRING", "mode": "NULLABLE"},
        ],
    )

    chronic_disease_transform_csv >> load_chronic_disease_to_bq
