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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="imdb.reviews",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    reviews_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="reviews_transform_csv",
        startup_timeout_seconds=600,
        name="reviews",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.imdb.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/imdb/reviews/aclImdb_v1.tar.gz",
            "SOURCE_URL": '{"title_link": "https://datasets.imdbws.com/title.basics.tsv.gz"}',
            "SOURCE_FILE": '{"user_review_data": "./files/aclImdb_v1.tar.gz", "title_data": "./files/title_basics.tsv.gz"}',
            "EXTRACT_HERE": "./files",
            "TARGET_CSV_FILE": "./files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/imdb/reviews/data_output.csv",
            "PIPELINE_NAME": "reviews",
            "CSV_HEADERS": '["review", "split", "label", "movie_id", "reviewer_rating", "movie_url", "title"]',
            "RENAME_MAPPINGS": '{"review": "review", "split": "split", "label": "label", "movie_id": "movie_id", "reviewer_rating": "reviewer_rating", "movie_url": "movie_url", "title": "title"}',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_reviews_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_reviews_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/imdb/reviews/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="imdb.reviews",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "review",
                "type": "STRING",
                "description": "User review's in IMDb.",
                "mode": "NULLABLE",
            },
            {
                "name": "split",
                "type": "STRING",
                "description": "It has two categories test and train.",
                "mode": "NULLABLE",
            },
            {
                "name": "label",
                "type": "STRING",
                "description": "It has three categories Negative, Positive and Unsupervised. All Unsupervised label has only split equals-to train.",
                "mode": "NULLABLE",
            },
            {
                "name": "movie_id",
                "type": "STRING",
                "description": "UniqueId for the movie in IMDb.",
                "mode": "NULLABLE",
            },
            {
                "name": "reviewer_rating",
                "type": "INTEGER",
                "description": "Reviewer rating for particular movie in IMDb. For train-unsupervised, reviewer_rating is NULL.",
                "mode": "NULLABLE",
            },
            {
                "name": "movie_url",
                "type": "STRING",
                "description": "Movie url for corresponding movie_id",
                "mode": "NULLABLE",
            },
            {
                "name": "title",
                "type": "STRING",
                "description": "Title of the movie for corresponding movie_id",
                "mode": "NULLABLE",
            },
        ],
    )

    reviews_transform_csv >> load_reviews_to_bq
