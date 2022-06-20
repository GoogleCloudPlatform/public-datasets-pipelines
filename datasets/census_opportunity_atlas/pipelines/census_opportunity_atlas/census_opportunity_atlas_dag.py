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
from airflow.providers.google.cloud.operators import kubernetes_engine

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="census_opportunity_atlas.census_opportunity_atlas",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "census-opportunity-atlas",
            "initial_node_count": 2,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-16",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Run CSV transform within kubernetes pod
    tract_covariates = kubernetes_engine.GKEStartPodOperator(
        task_id="tract_covariates",
        startup_timeout_seconds=600,
        name="tract_covariates",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="census-opportunity-atlas",
        image_pull_policy="Always",
        image="{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://opportunityinsights.org/wp-content/uploads/2018/10/tract_covariates.csv",
            "PIPELINE_NAME": "Census Opportunity Atlas - Tract Covariates",
            "SOURCE_FILE": "files/data_tract_covariates.csv",
            "SOURCE_FILE_UNZIPPED": "",
            "TARGET_FILE": "files/data_output_tract_covariates.csv",
            "CHUNKSIZE": "{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.chunksize }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.dataset_id }}",
            "TABLE_ID": "{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.schema_path }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.census_opportunity_atlas.container_registry.tract_covariates.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[\n  "state",\n  "county",\n  "tract",\n  "cz",\n  "czname",\n  "hhinc_mean2000",\n  "mean_commutetime2000",\n  "frac_coll_plus2000",\n  "frac_coll_plus2010",\n  "foreign_share2010",\n  "med_hhinc1990",\n  "med_hhinc2016",\n  "popdensity2000",\n  "poor_share2010",\n  "poor_share2000",\n  "poor_share1990",\n  "share_white2010",\n  "share_black2010",\n  "share_hisp2010",\n  "share_asian2010",\n  "share_black2000",\n  "share_white2000",\n  "share_hisp2000",\n  "share_asian2000",\n  "gsmn_math_g3_2013",\n  "rent_twobed2015",\n  "singleparent_share2010",\n  "singleparent_share1990",\n  "singleparent_share2000",\n  "traveltime15_2010",\n  "emp2000",\n  "mail_return_rate2010",\n  "ln_wage_growth_hs_grad",\n  "obs_total_5mi_2015",\n  "jobs_highpay_5mi_2015",\n  "popdensity2010",\n  "ann_avg_job_growth_2004_2013",\n  "job_density_2013"\n]',
            "DATA_DTYPES": '{\n  "state": "int",\n  "county": "int",\n  "tract": "int",\n  "cz": "int",\n  "czname": "str",\n  "hhinc_mean2000": "float",\n  "mean_commutetime2000": "float",\n  "frac_coll_plus2000": "float",\n  "frac_coll_plus2010": "float",\n  "foreign_share2010": "float",\n  "med_hhinc1990": "float",\n  "med_hhinc2016": "int",\n  "popdensity2000": "float",\n  "poor_share2010": "float",\n  "poor_share2000": "float",\n  "poor_share1990": "float",\n  "share_white2010": "float",\n  "share_black2010": "float",\n  "share_hisp2010": "float",\n  "share_asian2010": "float",\n  "share_black2000": "float",\n  "share_white2000": "float",\n  "share_hisp2000": "float",\n  "share_asian2000": "float",\n  "gsmn_math_g3_2013": "float",\n  "rent_twobed2015": "int",\n  "singleparent_share2010": "float",\n  "singleparent_share1990": "float",\n  "singleparent_share2000": "float",\n  "traveltime15_2010": "float",\n  "emp2000": "float",\n  "mail_return_rate2010": "float",\n  "ln_wage_growth_hs_grad": "float",\n  "jobs_total_5mi_2015": "int",\n  "jobs_highpay_5mi_2015": "int",\n  "popdensity2010": "float",\n  "ann_avg_job_growth_2004_2013": "float",\n  "job_density_2013": "float"\n}',
            "RENAME_MAPPINGS": '{\n  "state": "state",\n  "county": "county",\n  "tract": "tract",\n  "cz": "cz",\n  "czname": "czname",\n  "hhinc_mean2000": "hhinc_mean2000",\n  "mean_commutetime2000": "mean_commutetime2000",\n  "frac_coll_plus2000": "frac_coll_plus2000",\n  "frac_coll_plus2010": "frac_coll_plus2010",\n  "foreign_share2010": "foreign_share2010",\n  "med_hhinc1990": "med_hhinc1990",\n  "med_hhinc2016": "med_hhinc2016",\n  "popdensity2000": "popdensity2000",\n  "poor_share2010": "poor_share2010",\n  "poor_share2000": "poor_share2000",\n  "poor_share1990": "poor_share1990",\n  "share_white2010": "share_white2010",\n  "share_black2010": "share_black2010",\n  "share_hisp2010": "share_hisp2010",\n  "share_asian2010": "share_asian2010",\n  "share_black2000": "share_black2000",\n  "share_white2000": "share_white2000",\n  "share_hisp2000": "share_hisp2000",\n  "share_asian2000": "share_asian2000",\n  "gsmn_math_g3_2013": "gsmn_math_g3_2013",\n  "rent_twobed2015": "rent_twobed2015",\n  "singleparent_share2010": "singleparent_share2010",\n  "singleparent_share1990": "singleparent_share1990",\n  "singleparent_share2000": "singleparent_share2000",\n  "traveltime15_2010": "traveltime15_2010",\n  "emp2000": "emp2000",\n  "mail_return_rate2010": "mail_return_rate2010",\n  "ln_wage_growth_hs_grad": "ln_wage_growth_hs_grad",\n  "jobs_total_5mi_2015": "jobs_total_5mi_2015",\n  "jobs_highpay_5mi_2015": "jobs_highpay_5mi_2015",\n  "popdensity2010": "popdensity2010",\n  "ann_avg_job_growth_2004_2013": "ann_avg_job_growth_2004_2013",\n  "job_density_2013": "job_density_2013"\n}',
        },
        resources={"request_ephemeral_storage": "8G", "request_cpu": "1"},
    )

    # Run CSV transform within kubernetes pod
    tract_outcomes = kubernetes_engine.GKEStartPodOperator(
        task_id="tract_outcomes",
        name="tract_outcomes",
        namespace="default",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="census-opportunity-atlas",
        image_pull_policy="Always",
        image="{{ var.json.census_opportunity_atlas.container_registry.tract_outcomes.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://opportunityinsights.org/wp-content/uploads/2018/10/tract_outcomes.zip",
            "PIPELINE_NAME": "Census Opportunity Atlas - Tract Outcomes",
            "SOURCE_FILE": "files/data_tract_outcomes.csv",
            "SOURCE_FILE_UNZIPPED": "files/tract_outcomes_early.csv",
            "TARGET_FILE": "files/data_output_tract_outcomes.csv",
            "CHUNKSIZE": "{{ var.json.census_opportunity_atlas.container_registry.tract_outcomes.chunksize }}",
            "PROJECT_ID": "{{ var.value.gcp_project }}",
            "DATASET_ID": "{{ var.json.census_opportunity_atlas.container_registry.tract_outcomes.dataset_id }}",
            "TABLE_ID": "{{ var.json.census_opportunity_atlas.container_registry.tract_outcomes.destination_table }}",
            "SCHEMA_PATH": "{{ var.json.census_opportunity_atlas.container_registry.tract_outcomes.schema_path }}",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "{{ var.json.census_opportunity_atlas.container_registry.tract_outcomes.target_gcs_path }}",
            "INPUT_CSV_HEADERS": '[ "none" ]',
            "DATA_DTYPES": '{ "none": "int" }',
            "RENAME_MAPPINGS": '{ "none": "none" }',
        },
        resources={"request_ephemeral_storage": "8G", "limit_cpu": "1"},
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="census-opportunity-atlas",
    )

    create_cluster >> [tract_covariates, tract_outcomes] >> delete_cluster
