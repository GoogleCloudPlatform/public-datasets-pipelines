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
from airflow.contrib.operators import gcs_to_bq

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
    load_intersectional_attrition_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_intersectional_attrition_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/intersectional_attrition.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_intersectional_attrition",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. attrition_overall: Google’s overall index scores (both tech and non-tech); attrition_tech: Google’s attrition index scores for technical employees; attrition_non_tech: Google’s attrition index scores for technical employees.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "gender_us",
                "description": "Gender",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers who are Asian.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers who are Black.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers who are Hispanic or Latinx.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers who are Native American.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers who are white.",
                "type": "integer",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_intersectional_hiring_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_intersectional_hiring_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/intersectional_hiring.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_intersectional_hiring",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. hiring_overall: Google’s hiring representation (both tech and non-tech); hiring_tech: Google’s hiring representation for technical positions; hiring_non_tech: Google’s hiring representation for non-technical positions.; hiring_leadership: Google’s hiring representation for leadership positions.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "gender_us",
                "description": "Gender",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers who are Asian.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers who are Black.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers who are Hispanic or Latinx.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers who are Native American.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers who are white.",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_intersectional_representation_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_intersectional_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/intersectional_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_intersectional_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. representation_overall: Google’s overall representation (both tech and non-tech); representation_tech: Google’s technical employees representation; representation_non_tech: Google’s non-technical employees representation; representation_leadership: Google’s leadership representation.",
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
                "description": "Gender",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers who are Asian.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers who are Black.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers who are Hispanic or Latinx.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers who are Native American.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers who are white.",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_non_intersectional_representation_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_non_intersectional_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/non_intersectional_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_non_intersectional_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. representation_overall: Google’s overall representation (both tech and non-tech); representation_tech: Google’s technical employees representation; representation_non_tech: Google’s non-technical employees representation; representation_leadership: Google’s leadership representation.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers who are Asian.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers who are Black.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers who are Hispanic or Latinx.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers who are Native American.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers who are white.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_female",
                "description": "The percentage of Googlers who are female in the U.S.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_male",
                "description": "The percentage of Googlers who are male in the U.S.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_female",
                "description": "The percentage of Googlers who are female globally.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_male",
                "description": "The percentage of Googlers who are male globally.",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_non_intersectional_attrition_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_non_intersectional_attrition_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/non_intersectional_attrition.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_non_intersectional_attrition",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. attrition_overall: Google’s overall index scores (both tech and non-tech); attrition_tech: Google’s attrition index scores for technical employees; attrition_non_tech: Google’s attrition index scores for technical employees.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers who are Asian.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers who are Black.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers who are Hispanic or Latinx.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers who are Native American.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers who are white.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_us_female",
                "description": "The percentage of Googlers who are female in the U.S.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_us_male",
                "description": "The percentage of Googlers who are male in the U.S.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_global_female",
                "description": "The percentage of Googlers who are female globally.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_global_male",
                "description": "The percentage of Googlers who are male globally.",
                "type": "integer",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_non_intersectional_hiring_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_non_intersectional_hiring_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/non_intersectional_hiring.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_non_intersectional_hiring",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. hiring_overall: Google’s hiring representation (both tech and non-tech); hiring_tech: Google’s hiring representation for technical positions; hiring_non_tech: Google’s hiring representation for non-technical positions.; hiring_leadership: Google’s hiring representation for leadership positions.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers who are Asian.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black",
                "description": "The percentage of Googlers who are Black.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latinx",
                "description": "The percentage of Googlers who are Hispanic or Latinx.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_native_american",
                "description": "The percentage of Googlers who are Native American.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white",
                "description": "The percentage of Googlers who are white.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_female",
                "description": "The percentage of Googlers who are female in the U.S.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_us_male",
                "description": "The percentage of Googlers who are male in the U.S.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_female",
                "description": "The percentage of Googlers who are female globally.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_global_male",
                "description": "The percentage of Googlers who are male globally.",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_region_non_intersectional_attrition_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_region_non_intersectional_attrition_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/region_non_intersectional_attrition.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_region_non_intersectional_attrition",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. attrition_overall: Google’s overall index scores (both tech and non-tech); attrition_tech: Google’s attrition index scores for technical employees; attrition_non_tech: Google’s attrition index scores for technical employees.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "region",
                "description": "Region",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "gender_female",
                "description": "The attrition index score of Googlers who are female.",
                "type": "integer",
                "mode": "nullable",
            },
            {
                "name": "gender_male",
                "description": "The attrition index score of Googlers who are male.",
                "type": "integer",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_region_non_intersectional_hiring_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_region_non_intersectional_hiring_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/region_non_intersectional_hiring.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_region_non_intersectional_hiring",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. hiring_overall: Google’s hiring representation (both tech and non-tech); hiring_tech: Google’s hiring representation for technical positions; hiring_non_tech: Google’s hiring representation for non-technical positions.; hiring_leadership: Google’s hiring representation for leadership positions.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "region",
                "description": "Region",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "gender_female",
                "description": "The percentage of Googlers who are female.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_male",
                "description": "The percentage of Googlers who are male.",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_region_non_intersectional_representation_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_region_non_intersectional_representation_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/region_non_intersectional_representation.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_region_non_intersectional_representation",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. representation_overall: Google’s overall representation (both tech and non-tech); representation_tech: Google’s technical employees representation; representation_non_tech: Google’s non-technical employees representation; representation_leadership: Google’s leadership representation.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "region",
                "description": "Region",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "race_asian",
                "description": "The percentage of Googlers who are Asian.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_black_african",
                "description": "The percentage of Googlers who are Black African.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_hispanic_latino_latinx",
                "description": "The percentage of Googlers who are Hispanic or Latino or Latinx.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_indigenous",
                "description": "The percentage of Googlers who are Indigenous.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_mena",
                "description": "The percentage of Googlers who are Middle Eastern or North African.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "race_white_european",
                "description": "The percentage of Googlers who are White European.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_female",
                "description": "The percentage of Googlers who are female.",
                "type": "float",
                "mode": "nullable",
            },
            {
                "name": "gender_male",
                "description": "The percentage of Googlers who are male.",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_selfid_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_selfid_to_bq",
        bucket="{{ var.json.google_dei.storage_bucket }}",
        source_objects=["DAR/selfid.csv"],
        source_format="CSV",
        destination_project_dataset_table="google_dei.dar_selfid",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "workforce",
                "description": "Overall and broken down data about Google's employee representation, hiring, and attrition. representation_selfid_lgbtq: The percentage of Googlers who self-identified as LGBQ+ and/or Trans+; representation_selfid_disability: The percentage of Googlers who self-identified as having a disability; representation_selfid_military: The percentage of Googlers who self-identified as being or having been members of the military; representation_selfid_nonbinary: The percentage of Googlers who self-identified as non-binary.",
                "type": "string",
                "mode": "required",
            },
            {
                "name": "report_year",
                "description": "The year the report was published.",
                "type": "integer",
                "mode": "required",
            },
            {
                "name": "global",
                "description": "The percentage of Googlers who self-identified globally.",
                "type": "float",
                "mode": "nullable",
            },
        ],
    )

    load_intersectional_attrition_to_bq
    load_intersectional_hiring_to_bq
    load_intersectional_representation_to_bq
    load_non_intersectional_attrition_to_bq
    load_non_intersectional_hiring_to_bq
    load_non_intersectional_representation_to_bq
    load_region_non_intersectional_attrition_to_bq
    load_region_non_intersectional_hiring_to_bq
    load_region_non_intersectional_representation_to_bq
    load_selfid_to_bq
