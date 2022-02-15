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
    dag_id="census_opportunity_atlas.tract_covariates",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    tract_covariates_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="tract_covariates_transform_csv",
        startup_timeout_seconds=600,
        name="census_opportunity_atlas_tract_covariates",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.census_opportunity_atlas.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://opportunityinsights.org/wp-content/uploads/2018/10/tract_covariates.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/census_opportunity_atlas/tract_covariates/data_output.csv",
            "CSV_HEADERS": '["state","county","tract","cz","czname","hhinc_mean2000","mean_commutetime2000","frac_coll_plus2000","frac_coll_plus2010","foreign_share2010","med_hhinc1990","med_hhinc2016","popdensity2000","poor_share2010","poor_share2000","poor_share1990","share_white2010","share_black2010","share_hisp2010","share_asian2010","share_black2000","share_white2000","share_hisp2000","share_asian2000","gsmn_math_g3_2013","rent_twobed2015","singleparent_share2010","singleparent_share1990","singleparent_share2000","traveltime15_2010","emp2000","mail_return_rate2010","ln_wage_growth_hs_grad","jobs_total_5mi_2015","jobs_highpay_5mi_2015","popdensity2010","ann_avg_job_growth_2004_2013","job_density_2013"]',
            "RENAME_MAPPINGS": '{"state": "state","county": "county","tract": "tract","cz": "cz","czname": "czname","hhinc_mean2000": "hhinc_mean2000","mean_commutetime2000": "mean_commutetime2000","frac_coll_plus2000": "frac_coll_plus2000","frac_coll_plus2010": "frac_coll_plus2010","foreign_share2010": "foreign_share2010","med_hhinc1990": "med_hhinc1990","med_hhinc2016": "med_hhinc2016","popdensity2000": "popdensity2000","poor_share2010": "poor_share2010","poor_share2000": "poor_share2000","poor_share1990": "poor_share1990","share_white2010": "share_white2010","share_black2010": "share_black2010","share_hisp2010": "share_hisp2010","share_asian2010": "share_asian2010","share_black2000": "share_black2000","share_white2000": "share_white2000","share_hisp2000": "share_hisp2000","share_asian2000": "share_asian2000","gsmn_math_g3_2013": "gsmn_math_g3_2013","rent_twobed2015": "rent_twobed2015","singleparent_share2010": "singleparent_share2010","singleparent_share1990": "singleparent_share1990","singleparent_share2000": "singleparent_share2000","traveltime15_2010": "traveltime15_2010","emp2000": "emp2000","mail_return_rate2010": "mail_return_rate2010","ln_wage_growth_hs_grad": "ln_wage_growth_hs_grad","jobs_total_5mi_2015": "jobs_total_5mi_2015","jobs_highpay_5mi_2015": "jobs_highpay_5mi_2015","popdensity2010": "popdensity2010","ann_avg_job_growth_2004_2013": "ann_avg_job_growth_2004_2013","job_density_2013": "job_density_2013"}',
            "PIPELINE_NAME": "tract_covariates",
        },
        resources={
            "request_memory": "2G",
            "request_cpu": "1",
            "request_ephemeral_storage": "10G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_tract_covariates_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_tract_covariates_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/census_opportunity_atlas/tract_covariates/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="census_opportunity_atlas.tract_covariates",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {"name": "state", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "county", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tract", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cz", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "czname", "type": "STRING", "mode": "NULLABLE"},
            {"name": "hhinc_mean2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "mean_commutetime2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "frac_coll_plus2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "frac_coll_plus2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "foreign_share2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "med_hhinc1990", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "med_hhinc2016", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "popdensity2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "poor_share2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "poor_share2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "poor_share1990", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "share_white2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "share_black2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "share_hisp2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "share_asian2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "share_black2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "share_white2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "share_hisp2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "share_asian2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "gsmn_math_g3_2013", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "rent_twobed2015", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "singleparent_share2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "singleparent_share1990", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "singleparent_share2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "traveltime15_2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "emp2000", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "mail_return_rate2010", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "ln_wage_growth_hs_grad", "type": "STRING", "mode": "NULLABLE"},
            {"name": "jobs_total_5mi_2015", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "jobs_highpay_5mi_2015", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "popdensity2010", "type": "FLOAT", "mode": "NULLABLE"},
            {
                "name": "ann_avg_job_growth_2004_2013",
                "type": "FLOAT",
                "mode": "NULLABLE",
            },
            {"name": "job_density_2013", "type": "FLOAT", "mode": "NULLABLE"},
        ],
    )

    tract_covariates_transform_csv >> load_tract_covariates_to_bq
