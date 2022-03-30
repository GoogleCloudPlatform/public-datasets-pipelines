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
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        startup_timeout_seconds=600,
        name="census_opportunity_atlas_tract_covariates",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://opportunityinsights.org/wp-content/uploads/2018/10/tract_covariates.csv",
            "PIPELINE_NAME": "tract_covariates",
            "SOURCE_FILE": "files/data_tract_covariates.csv",
            "TARGET_FILE": "files/data_output_tract_covariates.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.target_gcs_path }}",
            "CSV_HEADERS": '[\n  "state","county","tract","cz","czname",\n  "hhinc_mean2000","mean_commutetime2000",\n  "frac_coll_plus2000","frac_coll_plus2010",\n  "foreign_share2010","med_hhinc1990",\n  "med_hhinc2016","popdensity2000",\n  "poor_share2010","poor_share2000",\n  "poor_share1990","share_white2010","share_black2010",\n  "share_hisp2010","share_asian2010","share_black2000",\n  "share_white2000","share_hisp2000","share_asian2000",\n  "gsmn_math_g3_2013","rent_twobed2015",\n  "singleparent_share2010","singleparent_share1990",\n  "singleparent_share2000","traveltime15_2010",\n  "emp2000","mail_return_rate2010","ln_wage_growth_hs_grad",\n  obs_total_5mi_2015","jobs_highpay_5mi_2015",\n  "popdensity2010","ann_avg_job_growth_2004_2013",\n  "job_density_2013"\n]',
            "RENAME_MAPPINGS": '{\n  "state": "state",\n  "county": "county",\n  "tract": "tract",\n  "cz": "cz",\n  "czname": "czname",\n  "hhinc_mean2000": "hhinc_mean2000",\n  "mean_commutetime2000": "mean_commutetime2000",\n  "frac_coll_plus2000": "frac_coll_plus2000",\n  "frac_coll_plus2010": "frac_coll_plus2010",\n  "foreign_share2010": "foreign_share2010",\n  "med_hhinc1990": "med_hhinc1990",\n  "med_hhinc2016": "med_hhinc2016",\n  "popdensity2000": "popdensity2000",\n  "poor_share2010": "poor_share2010",\n  "poor_share2000": "poor_share2000",\n  "poor_share1990": "poor_share1990",\n  "share_white2010": "share_white2010",\n  "share_black2010": "share_black2010",\n  "share_hisp2010": "share_hisp2010",\n  "share_asian2010": "share_asian2010",\n  "share_black2000": "share_black2000",\n  "share_white2000": "share_white2000",\n  "share_hisp2000": "share_hisp2000",\n  "share_asian2000": "share_asian2000",\n  "gsmn_math_g3_2013": "gsmn_math_g3_2013",\n  "rent_twobed2015": "rent_twobed2015",\n  "singleparent_share2010": "singleparent_share2010",\n  "singleparent_share1990": "singleparent_share1990",\n  "singleparent_share2000": "singleparent_share2000",\n  "traveltime15_2010": "traveltime15_2010",\n  "emp2000": "emp2000",\n  "mail_return_rate2010": "mail_return_rate2010",\n  "ln_wage_growth_hs_grad": "ln_wage_growth_hs_grad",\n  "jobs_total_5mi_2015": "jobs_total_5mi_2015",\n  "jobs_highpay_5mi_2015": "jobs_highpay_5mi_2015",\n  "popdensity2010": "popdensity2010",\n  "ann_avg_job_growth_2004_2013": "ann_avg_job_growth_2004_2013",\n  "job_density_2013": "job_density_2013"\n}',
        },
        resources={"request_ephemeral_storage": "8G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.target_gcs_path }}"
        ],
        source_format="CSV",
        destination_project_dataset_table="{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.destination_table }}",
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

    transform_csv >> load_to_bq
