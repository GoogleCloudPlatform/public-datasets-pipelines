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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-05-01",
}


with DAG(
    dag_id="google_dei.diversity_annual_report",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV data to a BigQuery table
    load_intersectional_attrition_index_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_intersectional_attrition_index_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/intersectional_attrition_index.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_intersectional_attrition_index",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "gender_us",
                "description": "Gender of Googler exits in the U.S.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The attrition index score of Googlers in the U.S. who identify as Asian and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The attrition index score of Googlers in the U.S. who identify as Black and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The attrition index score of Googlers in the U.S. who identify as Hispanic or Latinx and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The attrition index score of Googlers in the U.S. who identify as Native American and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The attrition index score of Googlers in the U.S. who identify as White and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_intersectional_hiring_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_intersectional_hiring_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/intersectional_hiring.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_intersectional_hiring",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "gender_us",
                "description": "Gender of Googlers hired in the U.S.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers hired in the U.S. who identify as Asian and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers hired in the U.S. who identify as Black and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers hired in the U.S. who identify as Hispanic or Latinx and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers hired in the U.S. who identify as Native American and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers hired in the U.S. who identify as White and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_intersectional_representation_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_intersectional_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/intersectional_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_intersectional_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "gender_us",
                "description": "Gender of Googlers in the U.S.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers in the U.S. who identify as Asian and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers in the U.S. who identify as Black and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers in the U.S. who identify as Hispanic or Latinx and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers in the U.S. who identify as Native American and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers in the U.S. who identify as White and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_intersectional_exits_representation_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_intersectional_exits_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/intersectional_exits_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_intersectional_exits_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "gender_us",
                "description": "Gender of Googler exits in the U.S.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googler exits in the U.S. who identify as Asian and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googler exits in the U.S. who identify as Black and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googler exits in the U.S. who identify as Hispanic or Latinx and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googler exits in the U.S. who identify as Native American and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googler exits in the U.S. who identify as White and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_non_intersectional_representation_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_non_intersectional_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/non_intersectional_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_non_intersectional_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers in the U.S. who identify as Asian and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers in the U.S. who identify as Black and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers in the U.S. who identify as Hispanic or Latinx and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers in the U.S. who identify as Native American and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers in the U.S. who identify as White and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_women",
                "description": "The percentage of Googlers in the U.S. who identify as women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_men",
                "description": "The percentage of Googlers in the U.S. who identify as men",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_women",
                "description": "The percentage of global Googlers who identify as women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_men",
                "description": "The percentage of global Googlers who identify as men",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_non_intersectional_exits_representation_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_non_intersectional_exits_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/non_intersectional_exits_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_non_intersectional_exits_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googler exits in the U.S. who identify as Asian and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googler exits in the U.S. who identify as Black and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googler exits in the U.S. who identify as Hispanic or Latinx and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googler exits in the U.S. who identify as Native American and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googler exits in the U.S. who identify as White and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_women",
                "description": "The percentage of Googler exits in the U.S. who identify as women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_men",
                "description": "The percentage of Googler exits in the U.S. who identify as men",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_women",
                "description": "The percentage of global Googler exits who identify as women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_men",
                "description": "The percentage of global Googler exits who identify as men",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_non_intersectional_attrition_index_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_non_intersectional_attrition_index_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/non_intersectional_attrition_index.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_non_intersectional_attrition_index",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The attrition index score of Googlers in the U.S. who identify as Asian and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The attrition index score of Googlers in the U.S. who identify as Black and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The attrition index score of Googlers in the U.S. who identify as Hispanic or Latinx and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The attrition index score of Googlers in the U.S. who identify as Native American and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The attrition index score of Googlers in the U.S. who identify as White and zero or more other races",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_us_women",
                "description": "The attrition index score of Googlers in the U.S. who are women",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_us_men",
                "description": "The attrition index score of Googlers in the U.S. who are men",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_global_women",
                "description": "The attrition index score of global Googlers who are women",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_global_men",
                "description": "The attrition index score of global Googlers who are men",
                "type": "integer",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_non_intersectional_hiring_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_non_intersectional_hiring_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/non_intersectional_hiring.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_non_intersectional_hiring",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers hired in the U.S. who identify as Asian and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers hired in the U.S. who identify as Black and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers hired in the U.S. who identify as Hispanic or Latinx and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers hired in the U.S. who identify as Native American and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers hired in the U.S. who identify as White and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_women",
                "description": "The percentage of Googlers hired in the U.S. who are women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_men",
                "description": "The percentage of Googlers hired in the U.S. who are men",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_women",
                "description": "The percentage of global Googlers hired who are women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_men",
                "description": "The percentage of global Googlers hired who are men",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_region_non_intersectional_attrition_index_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_region_non_intersectional_attrition_index_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/region_non_intersectional_attrition_index.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_region_non_intersectional_attrition_index",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "region",
                "description": "Region",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "gender_women",
                "description": "The attrition index score of Googlers in the region who are women",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_men",
                "description": "The attrition index score of Googlers in the region who are men",
                "type": "integer",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_region_non_intersectional_hiring_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_region_non_intersectional_hiring_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/region_non_intersectional_hiring.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_region_non_intersectional_hiring",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "region",
                "description": "Region",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "gender_women",
                "description": "The percentage of Googlers hired in the region who are women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_men",
                "description": "The percentage of Googlers hired in the region who are men",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_region_non_intersectional_representation_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_region_non_intersectional_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/region_non_intersectional_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_region_non_intersectional_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "region",
                "description": "Region",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers in the region who identify as Asian and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black_african",
                "description": "The percentage of Googlers in the region who identify as Black African and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latino_latinx",
                "description": "The percentage of Googlers in the region who identify as Hispanic, Latino, or Latinx and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_indigenous",
                "description": "The percentage of Googlers in the region who identify as Indigenous and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_mena",
                "description": "The percentage of Googlers in the region who identify as Middle Eastern or North African and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white_european",
                "description": "The percentage of Googlers in the region who identify as White or European and zero or more other races",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_women",
                "description": "The percentage of Googlers in the region who are women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_men",
                "description": "The percentage of Googlers in the region who are men",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_region_non_intersectional_exits_representation_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_region_non_intersectional_exits_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/region_non_intersectional_exits_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_region_non_intersectional_exits_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and sub-categories",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "region",
                "description": "Region",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "gender_women",
                "description": "The percentage of Googler exits in the region who are women",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_men",
                "description": "The percentage of Googler exits in the region who are men",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_selfid_representation_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_selfid_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/2022/selfid_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_selfid_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Self-identification category. lgbtq: Googlers who self-identify as LGBQ+ and/or Trans+; disability: Googlers who self-identify as having a disability; military: Googlers who self-identify as being or having been members of the military; nonbinary: Googlers who self-identify as non-binary",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "global",
                "description": 'The percentage of global Googlers who identify as being part of the self-identification category (i.e., "workforce" type)',
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    load_intersectional_attrition_index_to_bq
    load_intersectional_hiring_to_bq
    load_intersectional_representation_to_bq
    load_intersectional_exits_representation_to_bq
    load_non_intersectional_attrition_index_to_bq
    load_non_intersectional_hiring_to_bq
    load_non_intersectional_representation_to_bq
    load_non_intersectional_exits_representation_to_bq
    load_region_non_intersectional_attrition_index_to_bq
    load_region_non_intersectional_hiring_to_bq
    load_region_non_intersectional_representation_to_bq
    load_region_non_intersectional_exits_representation_to_bq
    load_selfid_representation_to_bq
