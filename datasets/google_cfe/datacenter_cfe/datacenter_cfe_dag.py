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
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-08-23",
}


with DAG(
    dag_id="google_cfe.datacenter_cfe",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV data to a BigQuery table
    cfe_gcs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="cfe_gcs_to_bq",
        bucket="{{ var.json.google_cfe.source_bucket }}",
        source_objects=[
            "data/2019-to-{{ macros.ds_format(macros.ds_add(ds, -366), '%Y-%m-%d', '%Y') }}.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="google_cfe.datacenter_cfe",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "year",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "The year for which the Google CFE metric has been aggregated. We will continue to add new data for each year as we make progress. Note that the Google CFE metric will only be included for the years that the Cloud Region or Data Center was operational. For example, the Data Center in Denmark came online in 2020, so the Google CFE data for that region starts in 2020 (and there is no data for Denmark for 2019).",
            },
            {
                "name": "cfe_region",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The regional boundary of the electric grid we consider when calculating the Google CFE score. For most of the world, the CFE region is defined as the country. However, for countries that have distinct grids, such as the US, there are multiple CFE regions, which are defined by the balancing authority.",
            },
            {
                "name": "zone_id",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "This is the ID associated with the CFE Region based on Tomorrow's ElectricityMap API definition. (http://static.electricitymap.org/api/docs/index.html#zones)",
            },
            {
                "name": "cloud_region",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The Google Cloud Region that is mapped to the CFE region. For Google Data Centers that are not Cloud Regions, the region will be labeled 'non-cloud-data-center'.",
            },
            {
                "name": "location",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": 'This is the "friendly name" of the Cloud Region. For Google Data Centers that are not Cloud regions, the location will be the country (non-US) or the state (US) that the Data Center is located in.',
            },
            {
                "name": "google_cfe",
                "type": "FLOAT",
                "mode": "NULLABLE",
                "description": "This metric is calculated for every hour in every region and tells us what percentage of the energy we consumed during an hour that is carbon-free. We take into account the carbon-free energy that's already supplied by the grid, in addition to the investments we have made in renewable energy in that location to reach our 24/7 carbon-free objective (https://www.gstatic.com/gumdrop/sustainability/247-carbon-free-energy.pdf). We then aggregate the available average hourly CFE percentage for each region for the year. We do not currently have the hourly energy information available for calculating the metrics for all regions. We anticipate rolling out the calculated metrics using hourly data to regions as the data becomes available.",
            },
        ],
    )

    cfe_gcs_to_bq
