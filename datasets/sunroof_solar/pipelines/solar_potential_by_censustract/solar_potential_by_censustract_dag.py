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
    dag_id="sunroof_solar.solar_potential_by_censustract",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="transform_csv",
        name="solar_potential_by_censustract",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.sunroof_solar.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "gs://project-sunroof/csv/latest/project-sunroof-census_tract.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "CHUNKSIZE": "750000",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/sunroof/solar_potential_by_censustract/data_output.csv",
        },
        resources={"limit_memory": "8G", "limit_cpu": "3"},
    )

    # Load CSV data to a BigQuery table
    load_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/sunroof/solar_potential_by_censustract/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="sunroof.solar_potential_by_censustract",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "region_name",
                "type": "STRING",
                "description": "Census Tract",
                "mode": "NULLABLE",
            },
            {
                "name": "state_name",
                "type": "STRING",
                "description": "Name of the state containing that region",
                "mode": "NULLABLE",
            },
            {
                "name": "lat_max",
                "type": "FLOAT",
                "description": "maximum latitude for that region",
                "mode": "NULLABLE",
            },
            {
                "name": "lat_min",
                "type": "FLOAT",
                "description": "minimum latitude for that region",
                "mode": "NULLABLE",
            },
            {
                "name": "lng_max",
                "type": "FLOAT",
                "description": "maximum longitude for that region",
                "mode": "NULLABLE",
            },
            {
                "name": "lng_min",
                "type": "FLOAT",
                "description": "minimum longitude for that region",
                "mode": "NULLABLE",
            },
            {
                "name": "lat_avg",
                "type": "FLOAT",
                "description": "average latitude for that region",
                "mode": "NULLABLE",
            },
            {
                "name": "lng_avg",
                "type": "FLOAT",
                "description": "average longitude for that region",
                "mode": "NULLABLE",
            },
            {
                "name": "yearly_sunlight_kwh_kw_threshold_avg",
                "type": "FLOAT",
                "description": "75% of the optimimum sunlight in the county containing that zip code",
                "mode": "NULLABLE",
            },
            {
                "name": "count_qualified",
                "type": "INTEGER",
                "description": "# of buildings in Google Maps that are suitable for solar",
                "mode": "NULLABLE",
            },
            {
                "name": "percent_covered",
                "type": "FLOAT",
                "description": "% of buildings in Google Maps covered by Project Sunroof",
                "mode": "NULLABLE",
            },
            {
                "name": "percent_qualified",
                "type": "FLOAT",
                "description": "% of buildings covered by Project Sunroof that are suitable for solar",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_panels_n",
                "type": "INTEGER",
                "description": "# of solar panels potential for north-facing roof space in that region, assuming 1.650m x 0.992m panels",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_panels_s",
                "type": "INTEGER",
                "description": "# of solar panels potential for south-facing roof space in that region, assuming 1.650m x 0.992m panels",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_panels_e",
                "type": "INTEGER",
                "description": "# of solar panels potential for east-facing roof space in that region, assuming 1.650m x 0.992m panels",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_panels_w",
                "type": "INTEGER",
                "description": "# of solar panels potential for west-facing roof space in that region, assuming 1.650m x 0.992m panels",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_panels_f",
                "type": "INTEGER",
                "description": "# of solar panels potential for flat roof space in that region, assuming 1.650m x 0.992m panels",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_panels_median",
                "type": "INTEGER",
                "description": "# of panels that fit on the median roof",
                "mode": "NULLABLE",
            },
            {
                "name": "number_of_panels_total",
                "type": "INTEGER",
                "description": "# of solar panels potential for all roof space in that region, assuming 1.650m 0.992m panels",
                "mode": "NULLABLE",
            },
            {
                "name": "kw_median",
                "type": "FLOAT",
                "description": "kW of solar potential for the median building in that region (assuming 250 watts per panel)",
                "mode": "NULLABLE",
            },
            {
                "name": "kw_total",
                "type": "FLOAT",
                "description": "# of kW of solar potential for all roof types in that region (assuming 250 watts per panel)",
                "mode": "NULLABLE",
            },
            {
                "name": "yearly_sunlight_kwh_n",
                "type": "FLOAT",
                "description": "total solar energy generation potential for north-facing roof space in that region",
                "mode": "NULLABLE",
            },
            {
                "name": "yearly_sunlight_kwh_s",
                "type": "FLOAT",
                "description": "total solar energy generation potential for south-facing roof space in that region",
                "mode": "NULLABLE",
            },
            {
                "name": "yearly_sunlight_kwh_e",
                "type": "FLOAT",
                "description": "total solar energy generation potential for east-facing roof space in that region",
                "mode": "NULLABLE",
            },
            {
                "name": "yearly_sunlight_kwh_w",
                "type": "FLOAT",
                "description": "total solar energy generation potential for west-facing roof space in that region",
                "mode": "NULLABLE",
            },
            {
                "name": "yearly_sunlight_kwh_f",
                "type": "FLOAT",
                "description": "total solar energy generation potential for flat roof space in that region",
                "mode": "NULLABLE",
            },
            {
                "name": "yearly_sunlight_kwh_median",
                "type": "FLOAT",
                "description": "kWh/kw/yr for the median roof, in DC (not AC) terms",
                "mode": "NULLABLE",
            },
            {
                "name": "yearly_sunlight_kwh_total",
                "type": "FLOAT",
                "description": "total solar energy generation potential for all roof space in that region",
                "mode": "NULLABLE",
            },
            {
                "name": "install_size_kw_buckets",
                "type": "STRING",
                "description": "# of buildings with potential for various installation size buckets. Format is a JSON array, where each element is a tuple containing (1) lower bound of bucket, in kW, and (2) number of buildings in that bucket.",
                "mode": "NULLABLE",
            },
            {
                "name": "carbon_offset_metric_tons",
                "type": "FLOAT",
                "description": "The potential carbon dioxide abatement of the solar capacity that meets the technical potential criteria. The calculation uses eGRID subregion CO2 equivalent non-baseload output emission rates. https://www.epa.gov/sites/production/files/2015-10/documents/egrid2012_summarytables_0.pdf",
                "mode": "NULLABLE",
            },
            {
                "name": "existing_installs_count",
                "type": "INTEGER",
                "description": "# of buildings estimated to have a solar installation, at time of data collection",
                "mode": "NULLABLE",
            },
            {
                "name": "center_point",
                "type": "GEOGRAPHY",
                "description": "",
                "mode": "NULLABLE",
            },
        ],
    )

    transform_csv >> load_to_bq
