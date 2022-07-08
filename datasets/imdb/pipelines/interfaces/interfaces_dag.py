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
    dag_id="imdb.interfaces",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    name_basics_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="name_basics_transform_csv",
        startup_timeout_seconds=600,
        name="name_basics",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.imdb.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{"url": "https://datasets.imdbws.com/name.basics.tsv.gz"}',
            "SOURCE_FILE": '{"url_data": "./files/name_basics.tsv.gz"}',
            "TARGET_CSV_FILE": "./files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/imdb/interfaces/name_basics_data_output.csv",
            "TABLE_NAME": "name_basics",
            "PIPELINE_NAME": "interfaces",
            "CSV_HEADERS": '["nconst", "primary_name", "birth_year", "death_year", "primary_profession", "known_for_titles"]',
            "RENAME_MAPPINGS": '{"nconst": "nconst", "primaryName": "primary_name", "birthYear": "birth_year", "deathYear": "death_year",\n "primaryProfession": "primary_profession", "knownForTitles": "known_for_titles"}',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_name_basics_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_name_basics_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/imdb/interfaces/name_basics_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="imdb.name_basics",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "nconst",
                "type": "string",
                "description": "Alphanumeric unique identifier of the name/person.",
                "mode": "nullable",
            },
            {
                "name": "primary_name",
                "type": "string",
                "description": "Name by which the person is most often credited.",
                "mode": "nullable",
            },
            {
                "name": "birth_year",
                "type": "integer",
                "description": "Birth year in YYYY format.",
                "mode": "nullable",
            },
            {
                "name": "death_year",
                "type": "integer",
                "description": "Death year in YYYY format if applicable.",
                "mode": "nullable",
            },
            {
                "name": "primary_profession",
                "type": "string",
                "description": "The top-3 professions of the person.",
                "mode": "nullable",
            },
            {
                "name": "known_for_titles",
                "type": "string",
                "description": "Titles the person is known for.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    title_akas_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="title_akas_transform_csv",
        startup_timeout_seconds=900,
        name="title_akas",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.imdb.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{"url": "https://datasets.imdbws.com/title.akas.tsv.gz"}',
            "SOURCE_FILE": '{"url_data": "./files/title_akas.tsv.gz"}',
            "CHUNK_SIZE": "300000",
            "TARGET_CSV_FILE": "./files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/imdb/interfaces/title_akas_data_output.csv",
            "TABLE_NAME": "title_akas",
            "PIPELINE_NAME": "interfaces",
            "CSV_HEADERS": '["title_id", "ordering", "title", "region", "language", "types", "attributes", "is_original_title"]',
            "RENAME_MAPPINGS": '{"titleId": "title_id", "ordering": "ordering", "title": "title", "region": "region", "language": "language", "types": "types", "attributes": "attributes", "isOriginalTitle": "is_original_title"}',
        },
        resources={
            "request_memory": "8G",
            "request_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_title_akas_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_title_akas_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/imdb/interfaces/title_akas_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="imdb.title_akas",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "title_id",
                "type": "string",
                "description": "A tconst, an alphanumeric unique identifier of the title.",
                "mode": "nullable",
            },
            {
                "name": "ordering",
                "type": "integer",
                "description": "A number to uniquely identify rows for a given title_id.",
                "mode": "nullable",
            },
            {
                "name": "title",
                "type": "string",
                "description": "The localized title.",
                "mode": "nullable",
            },
            {
                "name": "region",
                "type": "string",
                "description": "The region for this version of the title.",
                "mode": "nullable",
            },
            {
                "name": "language",
                "type": "string",
                "description": "The language of the title.",
                "mode": "nullable",
            },
            {
                "name": "types",
                "type": "string",
                "description": "Enumerated set of attributes for this alternative title. One or more of the following: 'alternative', 'dvd', 'festival', 'tv', 'video', 'working', 'original', 'imdbDisplay'. New values may be added in the future without warning.",
                "mode": "nullable",
            },
            {
                "name": "attributes",
                "type": "string",
                "description": "Additional terms to describe this alternative title, not enumerated",
                "mode": "nullable",
            },
            {
                "name": "is_original_title",
                "type": "boolean",
                "description": "False: not original title; True: original title.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    title_basics_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="title_basics_transform_csv",
        startup_timeout_seconds=600,
        name="title_basics",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.imdb.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{"url": "https://datasets.imdbws.com/title.basics.tsv.gz"}',
            "SOURCE_FILE": '{"url_data": "./files/title_basics.tsv.gz"}',
            "TARGET_CSV_FILE": "./files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/imdb/interfaces/title_basics_data_output.csv",
            "TABLE_NAME": "title_basics",
            "PIPELINE_NAME": "interfaces",
            "CSV_HEADERS": '["tconst", "title_type", "primary_title", "original_title", "is_adult", "start_year", "end_year", "runtime_minutes", "genres"]',
            "RENAME_MAPPINGS": '{"tconst": "tconst", "titleType": "title_type", "primaryTitle": "primary_title", "originalTitle": "original_title",\n "isAdult": "is_adult", "startYear": "start_year", "endYear": "end_year", "runtimeMinutes": "runtime_minutes", "genres": "genres"}',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_title_basics_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_title_basics_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/imdb/interfaces/title_basics_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="imdb.title_basics",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tconst",
                "type": "string",
                "description": "Alphanumeric unique identifier of the title.",
                "mode": "nullable",
            },
            {
                "name": "title_type",
                "type": "string",
                "description": "The type/format of the title (e.g. movie, short, tvseries, tvepisode, video, etc).",
                "mode": "nullable",
            },
            {
                "name": "primary_title",
                "type": "string",
                "description": "The more popular title / the title used by the filmmakers on promotional materials at the point of release.",
                "mode": "nullable",
            },
            {
                "name": "original_title",
                "type": "string",
                "description": "Original title, in the original language.",
                "mode": "nullable",
            },
            {
                "name": "is_adult",
                "type": "integer",
                "description": "0: non-adult title; 1: adult title.",
                "mode": "nullable",
            },
            {
                "name": "start_year",
                "type": "integer",
                "description": "Represents the release year of a title. In the case of TV Series, it is the series start year.",
                "mode": "nullable",
            },
            {
                "name": "end_year",
                "type": "integer",
                "description": "TV Series end year.",
                "mode": "nullable",
            },
            {
                "name": "runtime_minutes",
                "type": "integer",
                "description": "Primary runtime of the title, in minutes.",
                "mode": "nullable",
            },
            {
                "name": "genres",
                "type": "string",
                "description": "Includes up to three genres associated with the title.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    title_crew_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="title_crew_transform_csv",
        startup_timeout_seconds=600,
        name="title_crew",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.imdb.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{"url": "https://datasets.imdbws.com/title.crew.tsv.gz"}',
            "SOURCE_FILE": '{"url_data": "./files/title_crew.tsv.gz"}',
            "TARGET_CSV_FILE": "./files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/imdb/interfaces/title_crew_data_output.csv",
            "TABLE_NAME": "title_crew",
            "PIPELINE_NAME": "interfaces",
            "CSV_HEADERS": '["tconst", "directors", "writers"]',
            "RENAME_MAPPINGS": '{"tconst": "tconst", "directors": "directors", "writers": "writers"}',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_title_crew_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_title_crew_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/imdb/interfaces/title_crew_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="imdb.title_crew",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tconst",
                "type": "string",
                "description": "Alphanumeric unique identifier of the title.",
                "mode": "nullable",
            },
            {
                "name": "directors",
                "type": "string",
                "description": "Strinng of nconsts - director(s) of the given title.",
                "mode": "nullable",
            },
            {
                "name": "writers",
                "type": "string",
                "description": "String of nconsts - writer(s) of the given title.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    title_episode_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="title_episode_transform_csv",
        startup_timeout_seconds=600,
        name="title_episode",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.imdb.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{"url": "https://datasets.imdbws.com/title.episode.tsv.gz"}',
            "SOURCE_FILE": '{"url_data": "./files/title_episode.tsv.gz"}',
            "TARGET_CSV_FILE": "./files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/imdb/interfaces/title_episode_data_output.csv",
            "TABLE_NAME": "title_episode",
            "PIPELINE_NAME": "interfaces",
            "CSV_HEADERS": '["tconst", "parent_tconst", "season_number", "episode_number"]',
            "RENAME_MAPPINGS": '{"tconst": "tconst", "parentTconst": "parent_tconst", "seasonNumber": "season_number", "episodeNumber": "episode_number"}',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_title_episode_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_title_episode_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/imdb/interfaces/title_episode_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="imdb.title_episode",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tconst",
                "type": "string",
                "description": "Alphanumeric identifier of episode.",
                "mode": "nullable",
            },
            {
                "name": "parent_tconst",
                "type": "string",
                "description": "Alphanumeric identifier of the parent TV Series.",
                "mode": "nullable",
            },
            {
                "name": "season_number",
                "type": "integer",
                "description": "Season number the episode belongs to.",
                "mode": "nullable",
            },
            {
                "name": "episode_number",
                "type": "integer",
                "description": "Episode number of the tconst in the TV series.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    title_principals_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="title_principals_transform_csv",
        startup_timeout_seconds=900,
        name="title_principals",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.imdb.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{"url": "https://datasets.imdbws.com/title.principals.tsv.gz"}',
            "SOURCE_FILE": '{"url_data": "./files/title_principals.tsv.gz"}',
            "CHUNK_SIZE": "300000",
            "TARGET_CSV_FILE": "./files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/imdb/interfaces/title_principals_data_output.csv",
            "TABLE_NAME": "title_principals",
            "PIPELINE_NAME": "interfaces",
            "CSV_HEADERS": '["tconst", "ordering", "nconst", "category", "job", "characters"]',
            "RENAME_MAPPINGS": '{"tconst": "tconst", "ordering": "ordering", "nconst": "nconst", "category": "category",\n "job": "job", "characters": "characters"}',
        },
        resources={
            "request_memory": "8G",
            "request_cpu": "3",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_title_principals_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_title_principals_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/imdb/interfaces/title_principals_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="imdb.title_principals",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tconst",
                "type": "string",
                "description": "Alphanumeric unique identifier of the title.",
                "mode": "nullable",
            },
            {
                "name": "ordering",
                "type": "integer",
                "description": "a number to uniquely identify rows for a given title_id.",
                "mode": "nullable",
            },
            {
                "name": "nconst",
                "type": "string",
                "description": "Alphanumeric unique identifier of the name/person.",
                "mode": "nullable",
            },
            {
                "name": "category",
                "type": "string",
                "description": "The category of job that person was in.",
                "mode": "nullable",
            },
            {
                "name": "job",
                "type": "string",
                "description": "The specific job title if applicable.",
                "mode": "nullable",
            },
            {
                "name": "characters",
                "type": "string",
                "description": "The name of the character played if applicable.",
                "mode": "nullable",
            },
        ],
    )

    # Run CSV transform within kubernetes pod
    title_ratings_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="title_ratings_transform_csv",
        startup_timeout_seconds=600,
        name="title_ratings",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.imdb.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": '{"url": "https://datasets.imdbws.com/title.ratings.tsv.gz"}',
            "SOURCE_FILE": '{"url_data": "./files/title_ratings.tsv.gz"}',
            "TARGET_CSV_FILE": "./files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/imdb/interfaces/title_ratings_data_output.csv",
            "TABLE_NAME": "title_ratings",
            "PIPELINE_NAME": "interfaces",
            "CSV_HEADERS": '["tconst", "average_rating", "num_votes"]',
            "RENAME_MAPPINGS": '{"tconst": "tconst", "averageRating": "average_rating", "numVotes": "num_votes"}',
        },
        resources={"request_memory": "4G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_title_ratings_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_title_ratings_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/imdb/interfaces/title_ratings_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="imdb.title_ratings",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tconst",
                "type": "string",
                "description": "Alphanumeric unique identifier for title.",
                "mode": "nullable",
            },
            {
                "name": "average_rating",
                "type": "float",
                "description": "Weighted average of all the individual user ratings.",
                "mode": "nullable",
            },
            {
                "name": "num_votes",
                "type": "integer",
                "description": "Number of votes the title has received.",
                "mode": "nullable",
            },
        ],
    )

    name_basics_transform_csv >> load_name_basics_to_bq
    title_akas_transform_csv >> load_title_akas_to_bq
    title_basics_transform_csv >> load_title_basics_to_bq
    title_crew_transform_csv >> load_title_crew_to_bq
    title_episode_transform_csv >> load_title_episode_to_bq
    title_principals_transform_csv >> load_title_principals_to_bq
    title_ratings_transform_csv >> load_title_ratings_to_bq
