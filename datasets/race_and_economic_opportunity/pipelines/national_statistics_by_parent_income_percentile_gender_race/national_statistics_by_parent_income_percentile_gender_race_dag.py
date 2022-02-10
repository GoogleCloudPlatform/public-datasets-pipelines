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
from airflow.contrib.operators import gcs_to_bq, kubernetes_pod_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="race_and_economic_opportunity.national_statistics_by_parent_income_percentile_gender_race",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    national_statistics_transform_csv = kubernetes_pod_operator.KubernetesPodOperator(
        task_id="national_statistics_transform_csv",
        startup_timeout_seconds=600,
        name="race_and_economic_opportunity_national_statistics_by_parent_income_percentile_gender_race",
        namespace="default",
        affinity={
            "nodeAffinity": {
                "requiredDuringSchedulingIgnoredDuringExecution": {
                    "nodeSelectorTerms": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "cloud.google.com/gke-nodepool",
                                    "operator": "In",
                                    "values": ["pool-e2-standard-4"],
                                }
                            ]
                        }
                    ]
                }
            }
        },
        image_pull_policy="Always",
        image="{{ var.json.race_and_economic_opportunity.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://www2.census.gov/ces/opportunity/table_1.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/race_and_economic_opportunity/national_statistics_by_parent_income_percentile_gender_race/data_output.csv",
            "CSV_HEADERS": '["par_pctile","count_pooled","count_aian_pooled","count_asian_pooled","count_black_pooled","count_hisp_pooled","count_white_pooled","density_aian_pooled","density_asian_pooled","density_black_pooled","density_hisp_pooled","density_white_pooled","kfr_aian_pooled","kfr_asian_pooled","kfr_black_female","kfr_black_male","kfr_black_pooled","kfr_hisp_pooled","kfr_nativemom_aian_pooled","kfr_nativemom_asian_pooled","kfr_nativemom_black_pooled","kfr_nativemom_hisp_pooled","kfr_nativemom_white_pooled","kfr_pooled","kfr_white_female","kfr_white_male","kfr_white_pooled","kid_college_black_female","kid_college_black_male","kid_college_white_female","kid_college_white_male","kid_hours_black_female","kid_hours_black_male","kid_hours_white_female","kid_hours_white_male","kid_jail_black_female","kid_jail_black_male","kid_jail_white_female","kid_jail_white_male","kid_married_black_pooled","kid_married_white_pooled","kid_no_hs_black_female","kid_no_hs_black_male","kid_no_hs_white_female","kid_no_hs_white_male","kid_pos_hours_black_female","kid_pos_hours_black_male","kid_pos_hours_white_female","kid_pos_hours_white_male","kid_wage_rank_black_female","kid_wage_rank_black_male","kid_wage_rank_white_female","kid_wage_rank_white_male","kir_black_female","kir_black_male","kir_black_pooled","kir_white_female","kir_white_male","kir_white_pooled","kir_1par_black_male","kir_1par_white_male","kir_2par_black_male","kir_2par_white_male","kir_par_nohome_black_male","kir_par_nohome_white_male","spouse_rank_black_female","spouse_rank_black_male","spouse_rank_white_female","spouse_rank_white_male"]',
            "RENAME_MAPPINGS": '{"par_pctile": "par_pctile","count_pooled": "count_pooled","count_aian_pooled": "count_aian_pooled","count_asian_pooled": "count_asian_pooled","count_black_pooled": "count_black_pooled","count_hisp_pooled": "count_hisp_pooled","count_white_pooled": "count_white_pooled","density_aian_pooled": "density_aian_pooled","density_asian_pooled": "density_asian_pooled","density_black_pooled": "density_black_pooled","density_hisp_pooled": "density_hisp_pooled","density_white_pooled": "density_white_pooled","kfr_aian_pooled": "kfr_aian_pooled","kfr_asian_pooled": "kfr_asian_pooled","kfr_black_female": "kfr_black_female","kfr_black_male": "kfr_black_male","kfr_black_pooled": "kfr_black_pooled","kfr_hisp_pooled": "kfr_hisp_pooled","kfr_nativemom_aian_pooled": "kfr_nativemom_aian_pooled","kfr_nativemom_asian_pooled": "kfr_nativemom_asian_pooled","kfr_nativemom_black_pooled": "kfr_nativemom_black_pooled","kfr_nativemom_hisp_pooled": "kfr_nativemom_hisp_pooled","kfr_nativemom_white_pooled": "kfr_nativemom_white_pooled","kfr_pooled": "kfr_pooled","kfr_white_female": "kfr_white_female","kfr_white_male": "kfr_white_male","kfr_white_pooled": "kfr_white_pooled","kid_college_black_female": "kid_college_black_female","kid_college_black_male": "kid_college_black_male","kid_college_white_female": "kid_college_white_female","kid_college_white_male": "kid_college_white_male","kid_hours_black_female": "kid_hours_black_female","kid_hours_black_male": "kid_hours_black_male","kid_hours_white_female": "kid_hours_white_female","kid_hours_white_male": "kid_hours_white_male","kid_jail_black_female": "kid_jail_black_female","kid_jail_black_male": "kid_jail_black_male","kid_jail_white_female": "kid_jail_white_female","kid_jail_white_male": "kid_jail_white_male","kid_married_black_pooled": "kid_married_black_pooled","kid_married_white_pooled": "kid_married_white_pooled","kid_no_hs_black_female": "kid_no_hs_black_female","kid_no_hs_black_male": "kid_no_hs_black_male","kid_no_hs_white_female": "kid_no_hs_white_female","kid_no_hs_white_male": "kid_no_hs_white_male","kid_pos_hours_black_female": "kid_pos_hours_black_female","kid_pos_hours_black_male": "kid_pos_hours_black_male","kid_pos_hours_white_female": "kid_pos_hours_white_female","kid_pos_hours_white_male": "kid_pos_hours_white_male","kid_wage_rank_black_female": "kid_wage_rank_black_female","kid_wage_rank_black_male": "kid_wage_rank_black_male","kid_wage_rank_white_female": "kid_wage_rank_white_female","kid_wage_rank_white_male": "kid_wage_rank_white_male","kir_black_female": "kir_black_female","kir_black_male": "kir_black_male","kir_black_pooled": "kir_black_pooled","kir_white_female": "kir_white_female","kir_white_male": "kir_white_male","kir_white_pooled ": "kir_white_pooled","kir_1par_black_male": "kir_1par_black_male","kir_1par_white_male": "kir_1par_white_male","kir_2par_black_male": "kir_2par_black_male","kir_2par_white_male": "kir_2par_white_male","kir_par_nohome_black_male": "kir_par_nohome_black_male","kir_par_nohome_white_male": "kir_par_nohome_white_male","spouse_rank_black_female": "spouse_rank_black_female","spouse_rank_black_male": "spouse_rank_black_male","spouse_rank_white_female": "spouse_rank_white_female","spouse_rank_white_male": "spouse_rank_white_male"}',
            "PIPELINE_NAME": "national_statistics_by_parent_income_percentile_gender_race",
        },
        resources={"limit_memory": "2G", "limit_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_national_statistics_to_bq = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="load_national_statistics_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/race_and_economic_opportunity/national_statistics_by_parent_income_percentile_gender_race/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="race_and_economic_opportunity.national_statistics_by_parent_income_percentile_gender_race",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "par_pctile", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "count_pooled", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "count_aian_pooled", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "count_asian_pooled", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "count_black_pooled", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "count_hisp_pooled", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "count_white_pooled", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "density_aian_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "density_asian_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "density_black_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "density_hisp_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "density_white_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_aian_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_asian_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_black_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_hisp_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_nativemom_aian_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_nativemom_asian_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_nativemom_black_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_nativemom_hisp_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_nativemom_white_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kfr_white_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_college_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_college_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_college_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_college_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_hours_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_hours_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_hours_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_hours_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_jail_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_jail_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_jail_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_jail_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_married_black_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_married_white_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_no_hs_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_no_hs_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_no_hs_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_no_hs_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_pos_hours_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_pos_hours_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_pos_hours_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_pos_hours_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_wage_rank_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_wage_rank_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_wage_rank_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kid_wage_rank_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_black_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_white_pooled", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_1par_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_1par_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_2par_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_2par_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_par_nohome_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "kir_par_nohome_white_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "spouse_rank_black_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "spouse_rank_black_male", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "spouse_rank_white_female", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "spouse_rank_white_male", "type": "FLOAT", "mode": "NULLABLE"},
        ],
    )

    national_statistics_transform_csv >> load_national_statistics_to_bq
