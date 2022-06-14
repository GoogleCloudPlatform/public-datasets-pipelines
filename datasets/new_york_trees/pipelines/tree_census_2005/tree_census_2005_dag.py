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
    dag_id="new_york_trees.tree_census_2005",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    tree_census_2005_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="tree_census_2005_transform_csv",
        startup_timeout_seconds=600,
        name="tree_census_2005",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.new_york_trees.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://data.cityofnewyork.us/api/views/29bw-z7pj/rows.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/new_york_trees/tree_census_2005/data_output.csv",
            "PIPELINE_NAME": "tree_census_2005",
            "CSV_HEADERS": '["objectid","cen_year","tree_dbh","tree_loc","pit_type","soil_lvl","status","spc_latin", "spc_common","vert_other","vert_pgrd","vert_tgrd","vert_wall","horz_blck","horz_grate", "horz_plant","horz_other","sidw_crack","sidw_raise","wire_htap","wire_prime", "wire_2nd","wire_other","inf_canopy","inf_guard","inf_wires","inf_paving","inf_outlet", "inf_shoes","inf_lights","inf_other","trunk_dmg","zipcode","zip_city","cb_num","borocode", "boroname","cncldist","st_assem","st_senate","nta","nta_name","boro_ct","x_sp","y_sp", "objectid_1","location_1","state","latitude","longitude","census_tract","bin","bbl","address"]',
            "RENAME_MAPPINGS": '{"OBJECTID":"objectid","Location 1":"location_1","census tract":"census_tract"}',
            "INTEGER_STRING_COL": '["cb_num", "borocode", "cncldist", "st_assem", "st_senate", "boro_ct","x_sp","y_sp", "objectid_1","census_tract","bin","bbl"]',
        },
        resources={
            "request_memory": "3G",
            "request_cpu": "1",
            "request_ephemeral_storage": "5G",
        },
    )

    # Task to load CSV data to a BigQuery table
    load_tree_census_2005_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_tree_census_2005_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/new_york_trees/tree_census_2005/data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="new_york_trees.tree_census_2005",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "objectid",
                "type": "integer",
                "description": "",
                "mode": "required",
            },
            {
                "name": "cen_year",
                "type": "integer",
                "description": "This is the year the tree was inventoried in. Data collection for the 2005 census spanned multiple seasons. Data is in YYYY format.",
                "mode": "nullable",
            },
            {
                "name": "tree_dbh",
                "type": "integer",
                "description": "The diameter of the tree in whole inches, measured at breast height. (4.5 feet from the ground.)",
                "mode": "nullable",
            },
            {
                "name": "tree_loc",
                "type": "string",
                "description": "Establishes the location of the tree in relation to the address provided",
                "mode": "nullable",
            },
            {
                "name": "pit_type",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "soil_lvl",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "status",
                "type": "string",
                "description": "Excellent: full, well balanced crown and limb structure; leaves normal size color; no dead or broken branches; trunk solid; bark intact. Good: crown uneven or misshapen; some mechanical damage to bark or trunk; some signs of insects or disease; leaves somewhat below normal size and quantity; some dead or broken branches (less than half of the tree). Poor: large dead limbs with over one- half of the tree already dead or removed; large cavities; drastic deformities; leaves significantly below normal size and quantity; severe insect or disease damage. Dead: dead tree; leaves absent; twigs brittle. Shaft: all branches removed; trunk left standing; sprouts may or may not be evident. Stump: stump shorter than breast height; leaves entirely absent or present only on stump sprouts Empty pit: Pit contains exposed soil and no tree",
                "mode": "nullable",
            },
            {
                "name": "spc_latin",
                "type": "string",
                "description": "The scientific name of the species.",
                "mode": "nullable",
            },
            {
                "name": "spc_common",
                "type": "string",
                "description": "The common name of the species.",
                "mode": "nullable",
            },
            {
                "name": "vert_other",
                "type": "boolean",
                "description": "Other Vertical Treatment Present",
                "mode": "nullable",
            },
            {
                "name": "vert_pgrd",
                "type": "boolean",
                "description": "Perimeter guard present",
                "mode": "nullable",
            },
            {
                "name": "vert_tgrd",
                "type": "boolean",
                "description": "Tall guard present",
                "mode": "nullable",
            },
            {
                "name": "vert_wall",
                "type": "boolean",
                "description": "Walled tree well present",
                "mode": "nullable",
            },
            {
                "name": "horz_blck",
                "type": "boolean",
                "description": "Block pavers present",
                "mode": "nullable",
            },
            {
                "name": "horz_grate",
                "type": "boolean",
                "description": "Tree grates present",
                "mode": "nullable",
            },
            {
                "name": "horz_plant",
                "type": "boolean",
                "description": "Plantings present",
                "mode": "nullable",
            },
            {
                "name": "horz_other",
                "type": "boolean",
                "description": "Other horizontal treatment present",
                "mode": "nullable",
            },
            {
                "name": "sidw_crack",
                "type": "boolean",
                "description": "Cracked sidewalk present",
                "mode": "nullable",
            },
            {
                "name": "sidw_raise",
                "type": "boolean",
                "description": "Raised sidewalk present",
                "mode": "nullable",
            },
            {
                "name": "wire_htap",
                "type": "boolean",
                "description": "Indicates the presence of house tap wires",
                "mode": "nullable",
            },
            {
                "name": "wire_prime",
                "type": "boolean",
                "description": "Indicates the presence of primary wires",
                "mode": "nullable",
            },
            {
                "name": "wire_2nd",
                "type": "boolean",
                "description": "Indicates the presence of secondary wires",
                "mode": "nullable",
            },
            {
                "name": "wire_other",
                "type": "boolean",
                "description": "Indicates the presence of other wires",
                "mode": "nullable",
            },
            {
                "name": "inf_canopy",
                "type": "boolean",
                "description": "Canopy debris present",
                "mode": "nullable",
            },
            {
                "name": "inf_guard",
                "type": "boolean",
                "description": "Choking guard or grate present",
                "mode": "nullable",
            },
            {
                "name": "inf_wires",
                "type": "boolean",
                "description": "Choking wires present",
                "mode": "nullable",
            },
            {
                "name": "inf_paving",
                "type": "boolean",
                "description": "Close paving present",
                "mode": "nullable",
            },
            {
                "name": "inf_outlet",
                "type": "boolean",
                "description": "Electrical outlet present",
                "mode": "nullable",
            },
            {
                "name": "inf_shoes",
                "type": "boolean",
                "description": "Sneakers present",
                "mode": "nullable",
            },
            {
                "name": "inf_lights",
                "type": "boolean",
                "description": "Tree lights present",
                "mode": "nullable",
            },
            {
                "name": "inf_other",
                "type": "boolean",
                "description": "Other infrastructure conflicts present",
                "mode": "nullable",
            },
            {
                "name": "trunk_dmg",
                "type": "string",
                "description": "Describes specific damage or wounds found on the trunk",
                "mode": "nullable",
            },
            {
                "name": "zipcode",
                "type": "string",
                "description": "2005 zipcode that the tree falls in.",
                "mode": "nullable",
            },
            {
                "name": "zip_city",
                "type": "string",
                "description": "City, as derived from the zipcode",
                "mode": "nullable",
            },
            {
                "name": "cb_num",
                "type": "integer",
                "description": "Community Board that the tree falls in.",
                "mode": "nullable",
            },
            {
                "name": "borocode",
                "type": "integer",
                "description": "Borough tree is in, using a one-digit borough code: 1 – Manhattan, 2 – Bronx, 3 – Brooklyn, 4 – Queens, 5 – Staten Island",
                "mode": "nullable",
            },
            {
                "name": "boroname",
                "type": "string",
                "description": "Borough tree is in, full text",
                "mode": "nullable",
            },
            {
                "name": "cncldist",
                "type": "integer",
                "description": "New York City Council District tree point is in.",
                "mode": "nullable",
            },
            {
                "name": "st_assem",
                "type": "integer",
                "description": "State Assembly District tree point is in.",
                "mode": "nullable",
            },
            {
                "name": "st_senate",
                "type": "integer",
                "description": "State Senate District tree point is in.",
                "mode": "nullable",
            },
            {
                "name": "nta",
                "type": "string",
                "description": "nta code for the neighborhood tabulation area the tree point is in, from the 2010 census",
                "mode": "nullable",
            },
            {
                "name": "nta_name",
                "type": "string",
                "description": "Nta name for the neighborhood tabulation area the tree point is in",
                "mode": "nullable",
            },
            {
                "name": "boro_ct",
                "type": "integer",
                "description": "This is the boro_ct identifier for the census tract that the tree point falls into.",
                "mode": "nullable",
            },
            {
                "name": "x_sp",
                "type": "integer",
                "description": "X field",
                "mode": "nullable",
            },
            {
                "name": "y_sp",
                "type": "integer",
                "description": "y field",
                "mode": "nullable",
            },
            {
                "name": "objectid_1",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "location_1",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
            {"name": "state", "type": "string", "description": "", "mode": "nullable"},
            {
                "name": "latitude",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "longitude",
                "type": "float",
                "description": "",
                "mode": "nullable",
            },
            {
                "name": "census_tract",
                "type": "integer",
                "description": "",
                "mode": "nullable",
            },
            {"name": "bin", "type": "integer", "description": "", "mode": "nullable"},
            {"name": "bbl", "type": "integer", "description": "", "mode": "nullable"},
            {
                "name": "address",
                "type": "string",
                "description": "",
                "mode": "nullable",
            },
        ],
    )

    tree_census_2005_transform_csv >> load_tree_census_2005_to_bq
