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
    dag_id="fda_food.food_events",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="food_events",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.fda_food.container_registry.run_csv_transform_kub }}",
        env_vars={
            "PIPELINE": "food events",
            "SOURCE_URL": "https://download.open.fda.gov/food/event/food-event-0001-of-0001.json.zip",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/fda_food/food_events/files/data_output.csv",
            "DATA_NAMES": '[ "role", "name_brand", "industry_code", "industry_name", "report_number",\n  "outcomes", "date_created", "reactions", "date_started", "consumer.age",\n  "consumer.age_unit", "consumer.gender" ]',
            "DATA_DTYPES": '{ "role": "str", "name_brand": "str", "industry_code": "str", "industry_name": "str", "report_number": "str",\n  "outcomes": "str", "date_created": "str", "reactions": "str", "date_started": "str", "consumer.age": "float64",\n  "consumer.age_unit": "str", "consumer.gender": "str" }',
            "RENAME_MAPPINGS": '{ "report_number": "report_number", "reactions": "reactions", "outcomes": "outcomes", "name_brand": "products_brand_name", "industry_code": "products_industry_code",\n  "role": "products_role", "industry_name": "products_industry_name", "date_created": "date_created", "date_started": "date_started", "consumer.gender": "consumer_gender",\n  "consumer.age": "consumer_age", "consumer.age_unit": "consumer_age_unit" }',
            "REORDER_HEADERS": '[ "report_number", "reactions", "outcomes", "products_brand_name", "products_industry_code",\n  "products_role", "products_industry_name", "date_created", "date_started", "consumer_gender",\n  "consumer_age", "consumer_age_unit" ]',
            "RECORD_PATH": "products",
            "META": '[\n  "report_number", "outcomes", "date_created", "reactions", "date_started",\n  ["consumer", "age"], ["consumer", "age_unit"], ["consumer", "gender"]\n]',
        },
        resources={
            "request_memory": "4G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/fda_food/food_events/files/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.fda_food.food_events_destination_table }}",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        field_delimiter=",",
        quote_character='"',
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "report_number",
                "type": "STRING",
                "description": "The report number",
                "mode": "NULLABLE",
            },
            {
                "name": "reactions",
                "type": "STRING",
                "description": "Information on the reactions or symptoms experienced by the individual involved",
                "mode": "NULLABLE",
            },
            {
                "name": "outcomes",
                "type": "STRING",
                "description": "Information on known outcomes or consequences of the adverse event. For more info, refer: https://open.fda.gov/food/event/reference/",
                "mode": "NULLABLE",
            },
            {
                "name": "products_brand_name",
                "type": "STRING",
                "description": "The reported brand name of the product.",
                "mode": "NULLABLE",
            },
            {
                "name": "products_industry_code",
                "type": "STRING",
                "description": "The FDA industry code for the product. Results in this endpoint are generally limited to products tagged with industry codes related to human food and nutritional supplements or cosmetics.  For more info, refer: https://open.fda.gov/food/event/reference/",
                "mode": "NULLABLE",
            },
            {
                "name": "products_role",
                "type": "STRING",
                "description": "",
                "mode": "NULLABLE",
            },
            {
                "name": "products_industry_name",
                "type": "STRING",
                "description": "The FDA industry name associated with the product.",
                "mode": "NULLABLE",
            },
            {
                "name": "date_created",
                "type": "DATE",
                "description": "Date the report was received by FDA.",
                "mode": "NULLABLE",
            },
            {
                "name": "date_started",
                "type": "DATE",
                "description": "Date of the adverse event (when it was considered to have started).",
                "mode": "NULLABLE",
            },
            {
                "name": "consumer_gender",
                "type": "STRING",
                "description": "The reported gender of the consumer. Female = Female Male = Male Not Available = Unknown",
                "mode": "NULLABLE",
            },
            {
                "name": "consumer_age",
                "type": "FLOAT",
                "description": "The reported age of the consumer at the time of the adverse event report, expressed in the unit in the field age_unit",
                "mode": "NULLABLE",
            },
            {
                "name": "consumer_age_unit",
                "type": "STRING",
                "description": "Encodes the unit in which the age of the consumer is expressed.  Day(s) = age is expressed in days Week(s) = age is expressed in weeks Month(s) = age is expressed in months Year(s) = age is expressed in years Decade(s) = age is expressed in decades Not Available = Unknown",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
