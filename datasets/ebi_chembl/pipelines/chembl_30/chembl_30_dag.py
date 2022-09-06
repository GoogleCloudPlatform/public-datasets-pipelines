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
from airflow.providers.google.cloud.operators import kubernetes_engine
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="ebi_chembl.chembl_30",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:
    create_cluster = kubernetes_engine.GKECreateClusterOperator(
        task_id="create_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        body={
            "name": "ebi-chembl-30",
            "initial_node_count": 2,
            "network": "{{ var.value.vpc_network }}",
            "node_config": {
                "machine_type": "e2-standard-8",
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_write",
                    "https://www.googleapis.com/auth/cloud-platform",
                ],
            },
        },
    )

    # Copy files to GCS on the specified date
    csv_transform = kubernetes_engine.GKEStartPodOperator(
        task_id="csv_transform",
        name="ebi_chembl_30",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        cluster_name="ebi-chembl-30",
        namespace="default",
        image="{{ var.json.ebi_chembl.container_registry.run_csv_transform_kub }}",
        image_pull_policy="Always",
        env_vars={
            "OUTPUT_FOLDER": "./files/output",
            "SOURCE_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "SOURCE_GCS_OBJECT": "data/ebi_chembl/chembl_30/chembl_30_postgresql.dmp",
            "SOURCE_FILE": "./files/chembl_30_postgresql.dmp",
            "TABLES": '["action_type", "activities", "activity_properties", "activity_smid", "activity_stds_lookup", "activity_supp", "activity_supp_map", "assay_class_map", "assay_classification", "assay_parameters", "assay_type", "assays", "atc_classification", "binding_sites", "bio_component_sequences", "bioassay_ontology", "biotherapeutic_components", "biotherapeutics", "cell_dictionary", "chembl_id_lookup", "component_class", "component_domains", "component_go", "component_sequences", "component_synonyms", "compound_properties", "compound_records", "compound_structural_alerts", "compound_structures", "confidence_score_lookup", "curation_lookup", "data_validity_lookup", "defined_daily_dose", "docs", "domains", "drug_indication", "drug_mechanism", "drug_warning", "formulations", "frac_classification", "go_classification", "hrac_classification", "indication_refs", "irac_classification", "ligand_eff", "mechanism_refs", "metabolism", "metabolism_refs", "molecule_atc_classification", "molecule_dictionary", "molecule_frac_classification", "molecule_hierarchy", "molecule_hrac_classification", "molecule_irac_classification", "molecule_synonyms", "organism_class", "patent_use_codes", "predicted_binding_domains", "product_patents", "products", "protein_class_synonyms", "protein_classification", "protein_family_classification", "relationship_type", "research_companies", "research_stem", "site_components", "source", "structural_alert_sets", "structural_alerts", "target_components", "target_dictionary", "target_relations", "target_type", "tissue_dictionary", "usan_stems", "variant_sequences", "version", "warning_refs"]',
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_FOLDER": "data/ebi_chembl/chembl_30/output",
        },
        retries=3,
        retry_delay=300,
        retry_exponential_backoff=True,
        startup_timeout_seconds=600,
    )
    delete_cluster = kubernetes_engine.GKEDeleteClusterOperator(
        task_id="delete_cluster",
        project_id="{{ var.value.gcp_project }}",
        location="us-central1-c",
        name="ebi-chembl-30",
    )

    # Task to load CSV data to a BigQuery table
    load_action_type_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_action_type_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/action_type_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.action_type_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "action_type",
                "type": "string",
                "mode": "required",
                "description": "Primary key. Type of action of the drug e.g., agonist, antagonist.",
            },
            {
                "name": "description",
                "type": "string",
                "mode": "required",
                "description": "Description of how the action type is used",
            },
            {
                "name": "parent_type",
                "type": "string",
                "mode": "nullable",
                "description": "Higher-level grouping of action types e.g., positive vs negative action",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_activities_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_activities_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/activities_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.activities_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "activity_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique ID for the activity row",
            },
            {
                "name": "assay_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the assays table (containing the assay description)",
            },
            {
                "name": "doc_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to documents table (for quick lookup of publication details - can also link to documents through compound_records or assays table)",
            },
            {
                "name": "record_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the compound_records table (containing information on the compound tested)",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to compounds table (for quick lookup of compound structure - can also link to compounds through compound_records table)",
            },
            {
                "name": "standard_relation",
                "type": "string",
                "mode": "nullable",
                "description": "Symbol constraining the activity value (e.g. >, <, =)",
            },
            {
                "name": "standard_value",
                "type": "float",
                "mode": "nullable",
                "description": "Same as PUBLISHED_VALUE but transformed to common units: e.g. mM concentrations converted to nM.",
            },
            {
                "name": "standard_units",
                "type": "string",
                "mode": "nullable",
                "description": " Selected 'Standard' units for data type: e.g. concentrations are in nM.",
            },
            {
                "name": "standard_flag",
                "type": "integer",
                "mode": "nullable",
                "description": "Shows whether the standardised columns have been curated/set (1) or just default to the published data (0).",
            },
            {
                "name": "standard_type",
                "type": "string",
                "mode": "nullable",
                "description": " Standardised version of the published_activity_type (e.g. IC50 rather than Ic-50/Ic50/ic50/ic-50)",
            },
            {
                "name": "activity_comment",
                "type": "string",
                "mode": "nullable",
                "description": "Previously used to report non-numeric activities i.e. 'Slighty active', 'Not determined'. STANDARD_TEXT_VALUE will be used for this in future, and this will be just for additional comments.",
            },
            {
                "name": "data_validity_comment",
                "type": "string",
                "mode": "nullable",
                "description": "Comment reflecting whether the values for this activity measurement are likely to be correct - one of 'Manually validated' (checked original paper and value is correct), 'Potential author error' (value looks incorrect but is as reported in the original paper), 'Outside typical range' (value seems too high/low to be correct e.g., negative IC50 value), 'Non standard unit type' (units look incorrect for this activity type).",
            },
            {
                "name": "potential_duplicate",
                "type": "integer",
                "mode": "nullable",
                "description": "When set to 1, indicates that the value is likely to be a repeat citation of a value reported in a previous ChEMBL paper, rather than a new, independent measurement. Note: value of zero does not guarantee that the measurement is novel/independent though",
            },
            {
                "name": "pchembl_value",
                "type": "float",
                "mode": "nullable",
                "description": "Negative log of selected concentration-response activity values (IC50/EC50/XC50/AC50/Ki/Kd/Potency)",
            },
            {
                "name": "bao_endpoint",
                "type": "string",
                "mode": "nullable",
                "description": "ID for the corresponding result type in BioAssay Ontology (based on standard_type)",
            },
            {
                "name": "uo_units",
                "type": "string",
                "mode": "nullable",
                "description": "ID for the corresponding unit in Unit Ontology (based on standard_units)",
            },
            {
                "name": "qudt_units",
                "type": "string",
                "mode": "nullable",
                "description": "ID for the corresponding unit in QUDT Ontology (based on standard_units)",
            },
            {
                "name": "toid",
                "type": "integer",
                "mode": "nullable",
                "description": " The Test Occasion Identifier, used to group together related activity measurements",
            },
            {
                "name": "upper_value",
                "type": "float",
                "mode": "nullable",
                "description": "Where the activity is a range, this represents the highest value of the range (numerically), while the PUBLISHED_VALUE column represents the lower value",
            },
            {
                "name": "standard_upper_value",
                "type": "integer",
                "mode": "nullable",
                "description": "Where the activity is a range, this represents the standardised version of the highest value of the range (with the lower value represented by STANDARD_VALUE)",
            },
            {
                "name": "src_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to source table, indicating the source of the activity value",
            },
            {
                "name": "type",
                "type": "string",
                "mode": "required",
                "description": "Type of end-point measurement: e.g. IC50, LD50, %inhibition etc, as it appears in the original dataset",
            },
            {
                "name": "relation",
                "type": "string",
                "mode": "nullable",
                "description": "Symbol constraining the activity value (e.g. >, <, =), as it appears in the original dataset",
            },
            {
                "name": "value",
                "type": "float",
                "mode": "nullable",
                "description": "Datapoint value as it appears in the original dataset.",
            },
            {
                "name": "units",
                "type": "string",
                "mode": "nullable",
                "description": " Units of measurement as they appear in the original dataset",
            },
            {
                "name": "text_value",
                "type": "string",
                "mode": "nullable",
                "description": "Non-numeric value for measurement as in original dataset",
            },
            {
                "name": "standard_text_value",
                "type": "string",
                "mode": "nullable",
                "description": "Standardized version of non-numeric measurement",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_activity_properties_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_activity_properties_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/activity_properties_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.activity_properties_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "ap_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique ID for each record.",
            },
            {
                "name": "activity_id",
                "type": "integer",
                "mode": "required",
                "description": "FK to ACTIVITY_ID in ACTIVITIES table.",
            },
            {
                "name": "type",
                "type": "string",
                "mode": "required",
                "description": "The parameter or property type",
            },
            {
                "name": "relation",
                "type": "string",
                "mode": "nullable",
                "description": "Symbol constraining the value (e.g. >, <, =)",
            },
            {
                "name": "value",
                "type": "float",
                "mode": "nullable",
                "description": "Numberical value for the parameter or property",
            },
            {
                "name": "units",
                "type": "string",
                "mode": "nullable",
                "description": " Units of measurement",
            },
            {
                "name": "text_value",
                "type": "string",
                "mode": "nullable",
                "description": "Non-numerical value of the parameter or property",
            },
            {
                "name": "standard_type",
                "type": "string",
                "mode": "nullable",
                "description": " Standardised form of the TYPE",
            },
            {
                "name": "standard_relation",
                "type": "string",
                "mode": "nullable",
                "description": "Standardised form of the RELATION",
            },
            {
                "name": "standard_value",
                "type": "float",
                "mode": "nullable",
                "description": "Standardised form of the VALUE",
            },
            {
                "name": "standard_units",
                "type": "string",
                "mode": "nullable",
                "description": " Standardised form of the UNITS",
            },
            {
                "name": "standard_text_value",
                "type": "string",
                "mode": "nullable",
                "description": "Standardised form of the TEXT_VALUE",
            },
            {
                "name": "comments",
                "type": "string",
                "mode": "nullable",
                "description": "A Comment.",
            },
            {
                "name": "result_flag",
                "type": "integer",
                "mode": "required",
                "description": "A flag to indicate, if set to 1, that this type is a dependent variable/result (e.g., slope) rather than an independent variable/parameter (0, the default).",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_activity_smid_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_activity_smid_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/activity_smid_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.activity_smid_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "smid",
                "type": "integer",
                "mode": "required",
                "description": "FK to SMID in ACTIVITY_SUPP_MAP, and a FK to SMID in ACTIVITY_SUPP",
            }
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_activity_stds_lookup_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_activity_stds_lookup_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/activity_stds_lookup_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.activity_stds_lookup_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "std_act_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "standard_type",
                "type": "string",
                "mode": "required",
                "description": "The standard_type that other published_types in the activities table have been converted to.",
            },
            {
                "name": "definition",
                "type": "string",
                "mode": "nullable",
                "description": " A description/definition of the standard_type.",
            },
            {
                "name": "standard_units",
                "type": "string",
                "mode": "required",
                "description": "The units that are applied to this standard_type and to which other published_units are converted. Note a standard_type may have more than one allowable standard_unit and therefore multiple rows in this table.",
            },
            {
                "name": "normal_range_min",
                "type": "float",
                "mode": "nullable",
                "description": "The lowest value for this activity type that is likely to be genuine. This is only an approximation, so lower genuine values may exist, but it may be desirable to validate these before using them. For a given standard_type/units, values in the activities table below this threshold are flagged with a data_validity_comment of 'Outside typical range'.",
            },
            {
                "name": "normal_range_max",
                "type": "float",
                "mode": "nullable",
                "description": "The highest value for this activity type that is likely to be genuine. This is only an approximation, so higher genuine values may exist, but it may be desirable to validate these before using them. For a given standard_type/units, values in the activities table above this threshold are flagged with a data_validity_comment of 'Outside typical range'.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_activity_supp_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_activity_supp_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/activity_supp_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.activity_supp_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "as_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique ID for each record.",
            },
            {
                "name": "rgid",
                "type": "integer",
                "mode": "required",
                "description": "Record Grouping ID, used to group together related data points in this table",
            },
            {
                "name": "smid",
                "type": "integer",
                "mode": "nullable",
                "description": "FK to SMID in ACTIVITY_SMID.",
            },
            {
                "name": "type",
                "type": "string",
                "mode": "required",
                "description": "Type of end-point measurement: e.g. IC50, LD50, %inhibition etc, as it appears in the original dataset",
            },
            {
                "name": "relation",
                "type": "string",
                "mode": "nullable",
                "description": "Symbol constraining the activity value (e.g. >, <, =), as it appears in the original dataset",
            },
            {
                "name": "value",
                "type": "float",
                "mode": "nullable",
                "description": "Datapoint value as it appears in the original dataset.",
            },
            {
                "name": "units",
                "type": "string",
                "mode": "nullable",
                "description": " Units of measurement as they appear in the original dataset",
            },
            {
                "name": "text_value",
                "type": "string",
                "mode": "nullable",
                "description": "Non-numeric value for measurement as in original dataset",
            },
            {
                "name": "standard_type",
                "type": "string",
                "mode": "nullable",
                "description": " Standardised form of the TYPE",
            },
            {
                "name": "standard_relation",
                "type": "string",
                "mode": "nullable",
                "description": "Standardised form of the RELATION",
            },
            {
                "name": "standard_value",
                "type": "float",
                "mode": "nullable",
                "description": "Standardised form of the VALUE",
            },
            {
                "name": "standard_units",
                "type": "string",
                "mode": "nullable",
                "description": " Standardised form of the UNITS",
            },
            {
                "name": "standard_text_value",
                "type": "string",
                "mode": "nullable",
                "description": "Standardised form of the TEXT_VALUE",
            },
            {
                "name": "comments",
                "type": "string",
                "mode": "nullable",
                "description": "A Comment.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_activity_supp_map_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_activity_supp_map_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/activity_supp_map_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.activity_supp_map_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "actsm_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "activity_id",
                "type": "integer",
                "mode": "required",
                "description": "FK to ACTIVITY_ID in ACTIVITIES table.",
            },
            {
                "name": "smid",
                "type": "integer",
                "mode": "required",
                "description": "FK to SMID in ACTIVITY_SMID.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_assay_class_map_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_assay_class_map_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/assay_class_map_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.assay_class_map_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "ass_cls_map_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "assay_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key that maps to the ASSAYS table",
            },
            {
                "name": "assay_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key that maps to the ASSAY_CLASSIFICATION table",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_assay_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_assay_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/assay_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.assay_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "assay_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "l1",
                "type": "string",
                "mode": "nullable",
                "description": " High level classification e.g., by anatomical/therapeutic area",
            },
            {
                "name": "l2",
                "type": "string",
                "mode": "nullable",
                "description": " Mid-level classification e.g., by phenotype/biological process",
            },
            {
                "name": "l3",
                "type": "string",
                "mode": "nullable",
                "description": "Fine-grained classification e.g., by assay type",
            },
            {
                "name": "class_type",
                "type": "string",
                "mode": "nullable",
                "description": "The type of assay being classified e.g., in vivo efficacy",
            },
            {
                "name": "source",
                "type": "string",
                "mode": "nullable",
                "description": "Source from which the assay class was obtained",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_assay_parameters_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_assay_parameters_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/assay_parameters_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.assay_parameters_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "assay_param_id",
                "type": "integer",
                "mode": "required",
                "description": "Numeric primary key",
            },
            {
                "name": "assay_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to assays table. The assay to which this parameter belongs",
            },
            {
                "name": "type",
                "type": "string",
                "mode": "required",
                "description": "The type of parameter being described, according to the original data source",
            },
            {
                "name": "relation",
                "type": "string",
                "mode": "nullable",
                "description": "The relation symbol for the parameter being described, according to the original data source",
            },
            {
                "name": "value",
                "type": "float",
                "mode": "nullable",
                "description": "The value of the parameter being described, according to the original data source. Used for numeric data",
            },
            {
                "name": "units",
                "type": "string",
                "mode": "nullable",
                "description": " The units for the parameter being described, according to the original data source",
            },
            {
                "name": "text_value",
                "type": "string",
                "mode": "nullable",
                "description": "The text value of the parameter being described, according to the original data source. Used for non-numeric/qualitative data",
            },
            {
                "name": "standard_type",
                "type": "string",
                "mode": "nullable",
                "description": " Standardized form of the TYPE",
            },
            {
                "name": "standard_relation",
                "type": "string",
                "mode": "nullable",
                "description": "Standardized form of the RELATION",
            },
            {
                "name": "standard_value",
                "type": "float",
                "mode": "nullable",
                "description": "Standardized form of the VALUE",
            },
            {
                "name": "standard_units",
                "type": "string",
                "mode": "nullable",
                "description": " Standardized form of the UNITS",
            },
            {
                "name": "standard_text_value",
                "type": "string",
                "mode": "nullable",
                "description": "Standardized form of the TEXT_VALUE",
            },
            {
                "name": "comments",
                "type": "string",
                "mode": "nullable",
                "description": "Additional comments describing the parameter",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_assay_type_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_assay_type_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/assay_type_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.assay_type_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "assay_type",
                "type": "string",
                "mode": "required",
                "description": "Single character representing assay type",
            },
            {
                "name": "assay_desc",
                "type": "string",
                "mode": "nullable",
                "description": " Description of assay type",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_assays_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_assays_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/assays_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.assays_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "assay_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique ID for the assay",
            },
            {
                "name": "doc_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to documents table",
            },
            {
                "name": "description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of the reported assay",
            },
            {
                "name": "assay_type",
                "type": "string",
                "mode": "nullable",
                "description": " Assay classification, e.g. B=Binding assay, A=ADME assay, F=Functional assay",
            },
            {
                "name": "assay_test_type",
                "type": "string",
                "mode": "nullable",
                "description": "Type of assay system (i.e., in vivo or in vitro)",
            },
            {
                "name": "assay_category",
                "type": "string",
                "mode": "nullable",
                "description": "screening, confirmatory (ie: dose-response), summary, panel or other.",
            },
            {
                "name": "assay_organism",
                "type": "string",
                "mode": "nullable",
                "description": " Name of the organism for the assay system (e.g., the organism, tissue or cell line in which an assay was performed). May differ from the target organism (e.g., for a human protein expressed in non-human cells, or pathogen-infected human cells).",
            },
            {
                "name": "assay_tax_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NCBI tax ID for the assay organism.",
            },
            {
                "name": "assay_strain",
                "type": "string",
                "mode": "nullable",
                "description": " Name of specific strain of the assay organism used (where known)",
            },
            {
                "name": "assay_tissue",
                "type": "string",
                "mode": "nullable",
                "description": " Name of tissue used in the assay system (e.g., for tissue-based assays) or from which the assay system was derived (e.g., for cell/subcellular fraction-based assays).",
            },
            {
                "name": "assay_cell_type",
                "type": "string",
                "mode": "nullable",
                "description": " Name of cell type or cell line used in the assay system (e.g., for cell-based assays).",
            },
            {
                "name": "assay_subcellular_fraction",
                "type": "string",
                "mode": "nullable",
                "description": " Name of subcellular fraction used in the assay system (e.g., microsomes, mitochondria).",
            },
            {
                "name": "tid",
                "type": "integer",
                "mode": "nullable",
                "description": "Target identifier to which this assay has been mapped. Foreign key to target_dictionary. From ChEMBL_15 onwards, an assay will have only a single target assigned.",
            },
            {
                "name": "relationship_type",
                "type": "string",
                "mode": "nullable",
                "description": " Flag indicating of the relationship between the reported target in the source document and the assigned target from TARGET_DICTIONARY. Foreign key to RELATIONSHIP_TYPE table.",
            },
            {
                "name": "confidence_score",
                "type": "integer",
                "mode": "nullable",
                "description": "Confidence score, indicating how accurately the assigned target(s) represents the actually assay target. Foreign key to CONFIDENCE_SCORE table. 0 means uncurated/unassigned, 1 = low confidence to 9 = high confidence.",
            },
            {
                "name": "curated_by",
                "type": "string",
                "mode": "nullable",
                "description": "Indicates the level of curation of the target assignment. Foreign key to curation_lookup table.",
            },
            {
                "name": "src_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to source table",
            },
            {
                "name": "src_assay_id",
                "type": "string",
                "mode": "nullable",
                "description": "Identifier for the assay in the source database/deposition (e.g., pubchem AID)",
            },
            {
                "name": "chembl_id",
                "type": "string",
                "mode": "required",
                "description": "ChEMBL identifier for this assay (for use on web interface etc)",
            },
            {
                "name": "cell_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to cell dictionary. The cell type or cell line used in the assay",
            },
            {
                "name": "bao_format",
                "type": "string",
                "mode": "nullable",
                "description": "ID for the corresponding format type in BioAssay Ontology (e.g., cell-based, biochemical, organism-based etc)",
            },
            {
                "name": "tissue_id",
                "type": "integer",
                "mode": "nullable",
                "description": "ID for the corresponding tissue/anatomy in Uberon. Foreign key to tissue_dictionary",
            },
            {
                "name": "variant_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to variant_sequences table. Indicates the mutant/variant version of the target used in the assay (where known/applicable)",
            },
            {
                "name": "aidx",
                "type": "string",
                "mode": "required",
                "description": "The Depositor Defined Assay Identifier",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_atc_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_atc_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/atc_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.atc_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "who_name",
                "type": "string",
                "mode": "nullable",
                "description": "WHO/INN name for the compound",
            },
            {
                "name": "level1",
                "type": "string",
                "mode": "nullable",
                "description": "First level of classification",
            },
            {
                "name": "level2",
                "type": "string",
                "mode": "nullable",
                "description": "Second level of classification",
            },
            {
                "name": "level3",
                "type": "string",
                "mode": "nullable",
                "description": "Third level of classification",
            },
            {
                "name": "level4",
                "type": "string",
                "mode": "nullable",
                "description": "Fourth level of classification",
            },
            {
                "name": "level5",
                "type": "string",
                "mode": "required",
                "description": "Complete ATC code for compound",
            },
            {
                "name": "level1_description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of first level of classification",
            },
            {
                "name": "level2_description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of second level of classification",
            },
            {
                "name": "level3_description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of third level of classification",
            },
            {
                "name": "level4_description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of fourth level of classification",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_binding_sites_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_binding_sites_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/binding_sites_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.binding_sites_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "site_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique identifier for a binding site in a given target.",
            },
            {
                "name": "site_name",
                "type": "string",
                "mode": "nullable",
                "description": " Name/label for the binding site.",
            },
            {
                "name": "tid",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to target_dictionary. Target on which the binding site is found.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_bio_component_sequences_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_bio_component_sequences_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/bio_component_sequences_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.bio_component_sequences_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "component_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique identifier for each of the molecular components of biotherapeutics in ChEMBL (e.g., antibody chains, recombinant proteins, synthetic peptides).",
            },
            {
                "name": "component_type",
                "type": "string",
                "mode": "required",
                "description": "Type of molecular component (e.g., 'PROTEIN','DNA','RNA').",
            },
            {
                "name": "description",
                "type": "string",
                "mode": "nullable",
                "description": " Description/name of molecular component.",
            },
            {
                "name": "sequence",
                "type": "string",
                "mode": "nullable",
                "description": "Sequence of the biotherapeutic component.",
            },
            {
                "name": "sequence_md5sum",
                "type": "string",
                "mode": "nullable",
                "description": "MD5 checksum of the sequence.",
            },
            {
                "name": "tax_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NCBI tax ID for the species from which the sequence is derived. May be null for humanized monoclonal antibodies, synthetic peptides etc.",
            },
            {
                "name": "organism",
                "type": "string",
                "mode": "nullable",
                "description": " Name of the species from which the sequence is derived.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_bioassay_ontology_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_bioassay_ontology_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/bioassay_ontology_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.bioassay_ontology_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "bao_id",
                "type": "string",
                "mode": "required",
                "description": "Bioassay Ontology identifier (BAO version 2.0)",
            },
            {
                "name": "label",
                "type": "string",
                "mode": "required",
                "description": "Bioassay Ontology label for the term (BAO version 2.0)",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_biotherapeutic_components_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_biotherapeutic_components_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/biotherapeutic_components_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.biotherapeutic_components_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "biocomp_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the biotherapeutics table, indicating which biotherapeutic the component is part of.",
            },
            {
                "name": "component_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the bio_component_sequences table, indicating which component is part of the biotherapeutic.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_biotherapeutics_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_biotherapeutics_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/biotherapeutics_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.biotherapeutics_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to molecule_dictionary",
            },
            {
                "name": "description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of the biotherapeutic.",
            },
            {
                "name": "helm_notation",
                "type": "string",
                "mode": "nullable",
                "description": "Sequence notation generated according to the HELM standard (http://www.openhelm.org/home). Currently for peptides only",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_cell_dictionary_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_cell_dictionary_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/cell_dictionary_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.cell_dictionary_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "cell_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique identifier for each cell line in the target_dictionary.",
            },
            {
                "name": "cell_name",
                "type": "string",
                "mode": "required",
                "description": "Name of each cell line (as used in the target_dicitonary pref_name).",
            },
            {
                "name": "cell_description",
                "type": "string",
                "mode": "nullable",
                "description": " Longer description (where available) of the cell line.",
            },
            {
                "name": "cell_source_tissue",
                "type": "string",
                "mode": "nullable",
                "description": "Tissue from which the cell line is derived, where known.",
            },
            {
                "name": "cell_source_organism",
                "type": "string",
                "mode": "nullable",
                "description": " Name of organism from which the cell line is derived.",
            },
            {
                "name": "cell_source_tax_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NCBI tax ID of the organism from which the cell line is derived.",
            },
            {
                "name": "clo_id",
                "type": "string",
                "mode": "nullable",
                "description": "ID for the corresponding cell line in Cell Line Ontology",
            },
            {
                "name": "efo_id",
                "type": "string",
                "mode": "nullable",
                "description": "ID for the corresponding cell line in Experimental Factory Ontology",
            },
            {
                "name": "cellosaurus_id",
                "type": "string",
                "mode": "nullable",
                "description": "ID for the corresponding cell line in Cellosaurus Ontology",
            },
            {
                "name": "cl_lincs_id",
                "type": "string",
                "mode": "nullable",
                "description": " Cell ID used in LINCS (Library of Integrated Network-based Cellular Signatures)",
            },
            {
                "name": "chembl_id",
                "type": "string",
                "mode": "nullable",
                "description": "ChEMBL identifier for the cell (used in web interface etc)",
            },
            {
                "name": "cell_ontology_id",
                "type": "string",
                "mode": "nullable",
                "description": "ID for the corresponding cell type in the Cell Ontology",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_chembl_id_lookup_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_chembl_id_lookup_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/chembl_id_lookup_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.chembl_id_lookup_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "chembl_id",
                "type": "string",
                "mode": "required",
                "description": "ChEMBL identifier",
            },
            {
                "name": "entity_type",
                "type": "string",
                "mode": "required",
                "description": "Type of entity (e.g., COMPOUND, ASSAY, TARGET)",
            },
            {
                "name": "entity_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key for that entity in corresponding table (e.g., molregno for compounds, tid for targets)",
            },
            {
                "name": "status",
                "type": "string",
                "mode": "required",
                "description": "Indicates whether the status of the entity within the database - ACTIVE, INACTIVE (downgraded), OBS (obsolete/removed).",
            },
            {
                "name": "last_active",
                "type": "integer",
                "mode": "nullable",
                "description": "indicates the last ChEMBL version where the CHEMBL_ID was active",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_component_class_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_component_class_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/component_class_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.component_class_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "component_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to component_sequences table.",
            },
            {
                "name": "protein_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the protein_classification table.",
            },
            {
                "name": "comp_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_component_domains_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_component_domains_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/component_domains_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.component_domains_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "compd_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "domain_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to the domains table, indicating the domain that is contained in the associated molecular component.",
            },
            {
                "name": "component_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the component_sequences table, indicating the molecular_component that has the given domain.",
            },
            {
                "name": "start_position",
                "type": "integer",
                "mode": "nullable",
                "description": "Start position of the domain within the sequence given in the component_sequences table.",
            },
            {
                "name": "end_position",
                "type": "integer",
                "mode": "nullable",
                "description": "End position of the domain within the sequence given in the component_sequences table.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_component_go_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_component_go_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/component_go_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.component_go_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "comp_go_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "component_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to COMPONENT_SEQUENCES table. The protein component this GO term applies to",
            },
            {
                "name": "go_id",
                "type": "string",
                "mode": "required",
                "description": "Foreign key to the GO_CLASSIFICATION table. The GO term that this protein is mapped to",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_component_sequences_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_component_sequences_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/component_sequences_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.component_sequences_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "component_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique identifier for the component.",
            },
            {
                "name": "component_type",
                "type": "string",
                "mode": "nullable",
                "description": "Type of molecular component represented (e.g., 'PROTEIN','DNA','RNA').",
            },
            {
                "name": "accession",
                "type": "string",
                "mode": "nullable",
                "description": "Accession for the sequence in the source database from which it was taken (e.g., UniProt accession for proteins).",
            },
            {
                "name": "sequence",
                "type": "string",
                "mode": "nullable",
                "description": "A representative sequence for the molecular component, as given in the source sequence database (not necessarily the exact sequence used in the assay).",
            },
            {
                "name": "sequence_md5sum",
                "type": "string",
                "mode": "nullable",
                "description": "MD5 checksum of the sequence.",
            },
            {
                "name": "description",
                "type": "string",
                "mode": "nullable",
                "description": " Description/name for the molecular component, usually taken from the source sequence database.",
            },
            {
                "name": "tax_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NCBI tax ID for the sequence in the source database (i.e., species that the protein/nucleic acid sequence comes from).",
            },
            {
                "name": "organism",
                "type": "string",
                "mode": "nullable",
                "description": " Name of the organism the sequence comes from.",
            },
            {
                "name": "db_source",
                "type": "string",
                "mode": "nullable",
                "description": "The name of the source sequence database from which sequences/accessions are taken. For UniProt proteins, this field indicates whether the sequence is from SWISS-PROT or TREMBL.",
            },
            {
                "name": "db_version",
                "type": "string",
                "mode": "nullable",
                "description": "The version of the source sequence database from which sequences/accession were last updated.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_component_synonyms_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_component_synonyms_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/component_synonyms_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.component_synonyms_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "compsyn_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "component_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the component_sequences table. The component to which this synonym applies.",
            },
            {
                "name": "component_synonym",
                "type": "string",
                "mode": "nullable",
                "description": " The synonym for the component.",
            },
            {
                "name": "syn_type",
                "type": "string",
                "mode": "nullable",
                "description": "The type or origin of the synonym (e.g., GENE_SYMBOL).",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_compound_properties_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_compound_properties_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/compound_properties_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.compound_properties_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to compounds table (compound structure)",
            },
            {
                "name": "mw_freebase",
                "type": "float",
                "mode": "nullable",
                "description": "Molecular weight of parent compound",
            },
            {
                "name": "alogp",
                "type": "float",
                "mode": "nullable",
                "description": "Calculated ALogP",
            },
            {
                "name": "hba",
                "type": "integer",
                "mode": "nullable",
                "description": "Number hydrogen bond acceptors",
            },
            {
                "name": "hbd",
                "type": "integer",
                "mode": "nullable",
                "description": "Number hydrogen bond donors",
            },
            {
                "name": "psa",
                "type": "float",
                "mode": "nullable",
                "description": "Polar surface area",
            },
            {
                "name": "rtb",
                "type": "integer",
                "mode": "nullable",
                "description": "Number rotatable bonds",
            },
            {
                "name": "ro3_pass",
                "type": "string",
                "mode": "nullable",
                "description": " Indicates whether the compound passes the rule-of-three (mw < 300, logP < 3 etc)",
            },
            {
                "name": "num_ro5_violations",
                "type": "integer",
                "mode": "nullable",
                "description": "Number of violations of Lipinski's rule-of-five, using HBA and HBD definitions",
            },
            {
                "name": "cx_most_apka",
                "type": "float",
                "mode": "nullable",
                "description": "The most acidic pKa calculated using ChemAxon v17.29.0",
            },
            {
                "name": "cx_most_bpka",
                "type": "float",
                "mode": "nullable",
                "description": "The most basic pKa calculated using ChemAxon v17.29.0",
            },
            {
                "name": "cx_logp",
                "type": "float",
                "mode": "nullable",
                "description": "The calculated octanol/water partition coefficient using ChemAxon v17.29.0",
            },
            {
                "name": "cx_logd",
                "type": "float",
                "mode": "nullable",
                "description": "The calculated octanol/water distribution coefficient at pH7.4 using ChemAxon v17.29.0",
            },
            {
                "name": "molecular_species",
                "type": "string",
                "mode": "nullable",
                "description": "Indicates whether the compound is an acid/base/neutral",
            },
            {
                "name": "full_mwt",
                "type": "float",
                "mode": "nullable",
                "description": "Molecular weight of the full compound including any salts",
            },
            {
                "name": "aromatic_rings",
                "type": "integer",
                "mode": "nullable",
                "description": "Number of aromatic rings",
            },
            {
                "name": "heavy_atoms",
                "type": "integer",
                "mode": "nullable",
                "description": "Number of heavy (non-hydrogen) atoms",
            },
            {
                "name": "qed_weighted",
                "type": "float",
                "mode": "nullable",
                "description": "Weighted quantitative estimate of drug likeness (as defined by Bickerton et al., Nature Chem 2012)",
            },
            {
                "name": "mw_monoisotopic",
                "type": "float",
                "mode": "nullable",
                "description": "Monoisotopic parent molecular weight",
            },
            {
                "name": "full_molformula",
                "type": "string",
                "mode": "nullable",
                "description": " Molecular formula for the full compound (including any salt)",
            },
            {
                "name": "hba_lipinski",
                "type": "integer",
                "mode": "nullable",
                "description": "Number of hydrogen bond acceptors calculated according to Lipinski's original rules (i.e., N + O count))",
            },
            {
                "name": "hbd_lipinski",
                "type": "integer",
                "mode": "nullable",
                "description": "Number of hydrogen bond donors calculated according to Lipinski's original rules (i.e., NH + OH count)",
            },
            {
                "name": "num_lipinski_ro5_violations",
                "type": "integer",
                "mode": "nullable",
                "description": "Number of violations of Lipinski's rule of five using HBA_LIPINSKI and HBD_LIPINSKI counts",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_compound_records_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_compound_records_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/compound_records_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.compound_records_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "record_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique ID for a compound/record",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to compounds table (compound structure)",
            },
            {
                "name": "doc_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to documents table",
            },
            {
                "name": "compound_key",
                "type": "string",
                "mode": "nullable",
                "description": " Key text identifying this compound in the scientific document",
            },
            {
                "name": "compound_name",
                "type": "string",
                "mode": "nullable",
                "description": "Name of this compound recorded in the scientific document",
            },
            {
                "name": "src_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to source table",
            },
            {
                "name": "src_compound_id",
                "type": "string",
                "mode": "nullable",
                "description": " Identifier for the compound in the source database (e.g., pubchem SID)",
            },
            {
                "name": "cidx",
                "type": "string",
                "mode": "required",
                "description": "The Depositor Defined Compound Identifier.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_compound_structural_alerts_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_compound_structural_alerts_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/compound_structural_alerts_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.compound_structural_alerts_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "cpd_str_alert_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the molecule_dictionary. The compound for which the structural alert has been found.",
            },
            {
                "name": "alert_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the structural_alerts table. The particular alert that has been identified in this compound.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_compound_structures_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_compound_structures_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/compound_structures_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.compound_structures_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Internal Primary Key for the compound structure and foreign key to molecule_dictionary table",
            },
            {
                "name": "molfile",
                "type": "string",
                "mode": "nullable",
                "description": "MDL Connection table representation of compound",
            },
            {
                "name": "standard_inchi",
                "type": "string",
                "mode": "nullable",
                "description": "IUPAC standard InChI for the compound",
            },
            {
                "name": "standard_inchi_key",
                "type": "string",
                "mode": "required",
                "description": "IUPAC standard InChI key for the compound",
            },
            {
                "name": "canonical_smiles",
                "type": "string",
                "mode": "nullable",
                "description": "Canonical smiles, generated using RDKit",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_confidence_score_lookup_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_confidence_score_lookup_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/confidence_score_lookup_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.confidence_score_lookup_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "confidence_score",
                "type": "integer",
                "mode": "required",
                "description": "0-9 score showing level of confidence in assignment of the precise molecular target of the assay",
            },
            {
                "name": "description",
                "type": "string",
                "mode": "required",
                "description": "Description of the target types assigned with each score",
            },
            {
                "name": "target_mapping",
                "type": "string",
                "mode": "required",
                "description": "Short description of the target types assigned with each score",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_curation_lookup_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_curation_lookup_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/curation_lookup_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.curation_lookup_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "curated_by",
                "type": "string",
                "mode": "required",
                "description": "Short description of the level of curation",
            },
            {
                "name": "description",
                "type": "string",
                "mode": "required",
                "description": "Definition of terms in the curated_by field.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_data_validity_lookup_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_data_validity_lookup_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/data_validity_lookup_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.data_validity_lookup_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "data_validity_comment",
                "type": "string",
                "mode": "required",
                "description": "Primary key. Short description of various types of errors/warnings applied to values in the activities table.",
            },
            {
                "name": "description",
                "type": "string",
                "mode": "nullable",
                "description": " Definition of the terms in the data_validity_comment field.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_defined_daily_dose_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_defined_daily_dose_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/defined_daily_dose_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.defined_daily_dose_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "atc_code",
                "type": "string",
                "mode": "required",
                "description": "ATC code for the compound (foreign key to ATC_CLASSIFICATION table)",
            },
            {
                "name": "ddd_units",
                "type": "string",
                "mode": "nullable",
                "description": " Units of defined daily dose",
            },
            {
                "name": "ddd_admr",
                "type": "string",
                "mode": "nullable",
                "description": "Administration route for dose",
            },
            {
                "name": "ddd_comment",
                "type": "string",
                "mode": "nullable",
                "description": "Comment",
            },
            {
                "name": "ddd_id",
                "type": "integer",
                "mode": "required",
                "description": "Internal primary key",
            },
            {
                "name": "ddd_value",
                "type": "float",
                "mode": "nullable",
                "description": "Value of defined daily dose",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_docs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_docs_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/docs_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.docs_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "doc_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique ID for the document",
            },
            {
                "name": "journal",
                "type": "string",
                "mode": "nullable",
                "description": "Abbreviated journal name for an article",
            },
            {
                "name": "year",
                "type": "integer",
                "mode": "nullable",
                "description": "Year of journal article publication",
            },
            {
                "name": "volume",
                "type": "string",
                "mode": "nullable",
                "description": "Volume of journal article",
            },
            {
                "name": "issue",
                "type": "string",
                "mode": "nullable",
                "description": "Issue of journal article",
            },
            {
                "name": "first_page",
                "type": "string",
                "mode": "nullable",
                "description": "First page number of journal article",
            },
            {
                "name": "last_page",
                "type": "string",
                "mode": "nullable",
                "description": "Last page number of journal article",
            },
            {
                "name": "pubmed_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NIH pubmed record ID, where available",
            },
            {
                "name": "doi",
                "type": "string",
                "mode": "nullable",
                "description": " Digital object identifier for this reference",
            },
            {
                "name": "chembl_id",
                "type": "string",
                "mode": "required",
                "description": "ChEMBL identifier for this document (for use on web interface etc)",
            },
            {
                "name": "title",
                "type": "string",
                "mode": "nullable",
                "description": " Document title (e.g., Publication title or description of dataset)",
            },
            {
                "name": "doc_type",
                "type": "string",
                "mode": "required",
                "description": "Type of the document (e.g., Publication, Deposited dataset)",
            },
            {
                "name": "authors",
                "type": "string",
                "mode": "nullable",
                "description": "For a deposited dataset, the authors carrying out the screening and/or submitting the dataset.",
            },
            {
                "name": "abstract",
                "type": "string",
                "mode": "nullable",
                "description": "For a deposited dataset, a brief description of the dataset.",
            },
            {
                "name": "patent_id",
                "type": "string",
                "mode": "nullable",
                "description": "Patent ID for this document",
            },
            {
                "name": "ridx",
                "type": "string",
                "mode": "required",
                "description": "The Depositor Defined Reference Identifier",
            },
            {
                "name": "src_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to Source table, indicating the source of this document",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_domains_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_domains_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/domains_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.domains_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "domain_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique identifier for each domain.",
            },
            {
                "name": "domain_type",
                "type": "string",
                "mode": "required",
                "description": "Indicates the source of the domain (e.g., Pfam).",
            },
            {
                "name": "source_domain_id",
                "type": "string",
                "mode": "required",
                "description": "Identifier for the domain in the source database (e.g., Pfam ID such as PF00001).",
            },
            {
                "name": "domain_name",
                "type": "string",
                "mode": "nullable",
                "description": "Name given to the domain in the source database (e.g., 7tm_1).",
            },
            {
                "name": "domain_description",
                "type": "string",
                "mode": "nullable",
                "description": " Longer name or description for the domain.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_drug_indication_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_drug_indication_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/drug_indication_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.drug_indication_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "drugind_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "record_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to compound_records table. Links to the drug record to which this indication applies",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "nullable",
                "description": "Molregno corresponding to the record_id in the compound_records table",
            },
            {
                "name": "max_phase_for_ind",
                "type": "integer",
                "mode": "nullable",
                "description": "The maximum phase of development that the drug is known to have reached for this particular indication",
            },
            {
                "name": "mesh_id",
                "type": "string",
                "mode": "required",
                "description": "Medical Subject Headings (MeSH) disease identifier corresponding to the indication",
            },
            {
                "name": "mesh_heading",
                "type": "string",
                "mode": "required",
                "description": "Medical Subject Heading term for the MeSH disease ID",
            },
            {
                "name": "efo_id",
                "type": "string",
                "mode": "nullable",
                "description": "Experimental Factor Ontology (EFO) disease identifier corresponding to the indication",
            },
            {
                "name": "efo_term",
                "type": "string",
                "mode": "nullable",
                "description": " Experimental Factor Ontology term for the EFO ID",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_drug_mechanism_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_drug_mechanism_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/drug_mechanism_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.drug_mechanism_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "mec_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key for each drug mechanism of action",
            },
            {
                "name": "record_id",
                "type": "integer",
                "mode": "required",
                "description": "Record_id for the drug (foreign key to compound_records table)",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "nullable",
                "description": "Molregno for the drug (foreign key to molecule_dictionary table)",
            },
            {
                "name": "mechanism_of_action",
                "type": "string",
                "mode": "nullable",
                "description": " Description of the mechanism of action e.g., 'Phosphodiesterase 5 inhibitor'",
            },
            {
                "name": "tid",
                "type": "integer",
                "mode": "nullable",
                "description": "Target associated with this mechanism of action (foreign key to target_dictionary table)",
            },
            {
                "name": "site_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Binding site for the drug within the target (where known) - foreign key to binding_sites table",
            },
            {
                "name": "action_type",
                "type": "string",
                "mode": "nullable",
                "description": "Type of action of the drug on the target e.g., agonist/antagonist etc (foreign key to action_type table)",
            },
            {
                "name": "direct_interaction",
                "type": "integer",
                "mode": "nullable",
                "description": "Flag to show whether the molecule is believed to interact directly with the target (1 = yes, 0 = no)",
            },
            {
                "name": "molecular_mechanism",
                "type": "integer",
                "mode": "nullable",
                "description": "Flag to show whether the mechanism of action describes the molecular target of the drug, rather than a higher-level physiological mechanism e.g., vasodilator (1 = yes, 0 = no)",
            },
            {
                "name": "disease_efficacy",
                "type": "integer",
                "mode": "nullable",
                "description": "Flag to show whether the target assigned is believed to play a role in the efficacy of the drug in the indication(s) for which it is approved (1 = yes, 0 = no)",
            },
            {
                "name": "mechanism_comment",
                "type": "string",
                "mode": "nullable",
                "description": "Additional comments regarding the mechanism of action",
            },
            {
                "name": "selectivity_comment",
                "type": "string",
                "mode": "nullable",
                "description": "Additional comments regarding the selectivity of the drug",
            },
            {
                "name": "binding_site_comment",
                "type": "string",
                "mode": "nullable",
                "description": "Additional comments regarding the binding site of the drug",
            },
            {
                "name": "variant_id",
                "type": "integer",
                "mode": "nullable",
                "description": "None",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_drug_warning_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_drug_warning_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/drug_warning_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.drug_warning_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "warning_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key for the drug warning",
            },
            {
                "name": "record_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to the compound_records table",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to molecule_dictionary table",
            },
            {
                "name": "warning_type",
                "type": "string",
                "mode": "nullable",
                "description": "Description of the drug warning type (e.g., withdrawn vs black box warning)",
            },
            {
                "name": "warning_class",
                "type": "string",
                "mode": "nullable",
                "description": " High-level class of the drug warning",
            },
            {
                "name": "warning_description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of the drug warning",
            },
            {
                "name": "warning_country",
                "type": "string",
                "mode": "nullable",
                "description": "List of countries/regions associated with the drug warning",
            },
            {
                "name": "warning_year",
                "type": "integer",
                "mode": "nullable",
                "description": "Year the drug was first shown the warning",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_formulations_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_formulations_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/formulations_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.formulations_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "product_id",
                "type": "string",
                "mode": "required",
                "description": "Unique identifier of the product. FK to PRODUCTS",
            },
            {
                "name": "ingredient",
                "type": "string",
                "mode": "nullable",
                "description": " Name of the approved ingredient within the product",
            },
            {
                "name": "strength",
                "type": "string",
                "mode": "nullable",
                "description": " Dose strength",
            },
            {
                "name": "record_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the compound_records table.",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "nullable",
                "description": "Unique identifier of the ingredient FK to MOLECULE_DICTIONARY",
            },
            {
                "name": "formulation_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_frac_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_frac_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/frac_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.frac_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "frac_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique numeric primary key for each level5 code",
            },
            {
                "name": "active_ingredient",
                "type": "string",
                "mode": "required",
                "description": "Name of active ingredient (fungicide) classified by FRAC",
            },
            {
                "name": "level1",
                "type": "string",
                "mode": "required",
                "description": "Mechanism of action code assigned by FRAC",
            },
            {
                "name": "level1_description",
                "type": "string",
                "mode": "required",
                "description": "Description of mechanism of action",
            },
            {
                "name": "level2",
                "type": "string",
                "mode": "required",
                "description": "Target site code assigned by FRAC",
            },
            {
                "name": "level2_description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of target provided by FRAC",
            },
            {
                "name": "level3",
                "type": "string",
                "mode": "required",
                "description": "Group number assigned by FRAC",
            },
            {
                "name": "level3_description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of group provided by FRAC",
            },
            {
                "name": "level4",
                "type": "string",
                "mode": "required",
                "description": "Number denoting the chemical group (number not assigned by FRAC)",
            },
            {
                "name": "level4_description",
                "type": "string",
                "mode": "nullable",
                "description": "Chemical group name provided by FRAC",
            },
            {
                "name": "level5",
                "type": "string",
                "mode": "required",
                "description": "A unique code assigned to each ingredient (based on the level 1-4 FRAC classification, but not assigned by IRAC)",
            },
            {
                "name": "frac_code",
                "type": "string",
                "mode": "required",
                "description": "The official FRAC classification code for the ingredient",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_go_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_go_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/go_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.go_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "go_id",
                "type": "string",
                "mode": "required",
                "description": "Primary key. Gene Ontology identifier for the GO slim term",
            },
            {
                "name": "parent_go_id",
                "type": "string",
                "mode": "nullable",
                "description": "Gene Ontology identifier for the parent of this GO term in the ChEMBL Drug Target GO slim",
            },
            {
                "name": "pref_name",
                "type": "string",
                "mode": "nullable",
                "description": " Gene Ontology name",
            },
            {
                "name": "class_level",
                "type": "integer",
                "mode": "nullable",
                "description": "Indicates the level of the term in the slim (L1 = highest)",
            },
            {
                "name": "aspect",
                "type": "string",
                "mode": "nullable",
                "description": " Indicates which aspect of the Gene Ontology the term belongs to (F = molecular function, P = biological process, C = cellular component)",
            },
            {
                "name": "path",
                "type": "string",
                "mode": "nullable",
                "description": "Indicates the full path to this term in the GO slim",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_hrac_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_hrac_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/hrac_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.hrac_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "hrac_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique numeric primary key for each level3 code",
            },
            {
                "name": "active_ingredient",
                "type": "string",
                "mode": "required",
                "description": "Name of active ingredient (herbicide) classified by HRAC",
            },
            {
                "name": "level1",
                "type": "string",
                "mode": "required",
                "description": "HRAC group code - denoting mechanism of action of herbicide",
            },
            {
                "name": "level1_description",
                "type": "string",
                "mode": "required",
                "description": "Description of mechanism of action provided by HRAC",
            },
            {
                "name": "level2",
                "type": "string",
                "mode": "required",
                "description": "Indicates a chemical family within a particular HRAC group (number not assigned by HRAC)",
            },
            {
                "name": "level2_description",
                "type": "string",
                "mode": "nullable",
                "description": "Description of chemical family provided by HRAC",
            },
            {
                "name": "level3",
                "type": "string",
                "mode": "required",
                "description": "A unique code assigned to each ingredient (based on the level 1 and 2 HRAC classification, but not assigned by HRAC)",
            },
            {
                "name": "hrac_code",
                "type": "string",
                "mode": "required",
                "description": "The official HRAC classification code for the ingredient",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_indication_refs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_indication_refs_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/indication_refs_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.indication_refs_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "indref_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "drugind_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the DRUG_INDICATION table, indicating the drug-indication link that this reference applies to",
            },
            {
                "name": "ref_type",
                "type": "string",
                "mode": "required",
                "description": "Type/source of reference",
            },
            {
                "name": "ref_id",
                "type": "string",
                "mode": "required",
                "description": "Identifier for the reference in the source",
            },
            {
                "name": "ref_url",
                "type": "string",
                "mode": "required",
                "description": "Full URL linking to the reference",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_irac_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_irac_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/irac_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.irac_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "irac_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique numeric primary key for each level4 code",
            },
            {
                "name": "active_ingredient",
                "type": "string",
                "mode": "required",
                "description": "Name of active ingredient (insecticide) classified by IRAC",
            },
            {
                "name": "level1",
                "type": "string",
                "mode": "required",
                "description": "Class of action e.g., nerve action, energy metabolism (code not assigned by IRAC)",
            },
            {
                "name": "level1_description",
                "type": "string",
                "mode": "required",
                "description": "Description of class of action, as provided by IRAC",
            },
            {
                "name": "level2",
                "type": "string",
                "mode": "required",
                "description": "IRAC main group code denoting primary site/mechanism of action",
            },
            {
                "name": "level2_description",
                "type": "string",
                "mode": "required",
                "description": "Description of site/mechanism of action provided by IRAC",
            },
            {
                "name": "level3",
                "type": "string",
                "mode": "required",
                "description": "IRAC sub-group code denoting chemical class of insecticide",
            },
            {
                "name": "level3_description",
                "type": "string",
                "mode": "required",
                "description": "Description of chemical class or exemplifying ingredient provided by IRAC",
            },
            {
                "name": "level4",
                "type": "string",
                "mode": "required",
                "description": "A unique code assigned to each ingredient (based on the level 1, 2 and 3 IRAC classification, but not assigned by IRAC)",
            },
            {
                "name": "irac_code",
                "type": "string",
                "mode": "required",
                "description": "The official IRAC classification code for the ingredient",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_ligand_eff_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_ligand_eff_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/ligand_eff_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.ligand_eff_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "activity_id",
                "type": "integer",
                "mode": "required",
                "description": "Link key to activities table",
            },
            {
                "name": "bei",
                "type": "float",
                "mode": "nullable",
                "description": "Binding Efficiency Index = p(XC50) *1000/MW_freebase",
            },
            {
                "name": "sei",
                "type": "float",
                "mode": "nullable",
                "description": "Surface Efficiency Index = p(XC50)*100/PSA",
            },
            {
                "name": "le",
                "type": "float",
                "mode": "nullable",
                "description": "[from the Hopkins DDT paper 2004]",
            },
            {
                "name": "lle",
                "type": "float",
                "mode": "nullable",
                "description": "Lipophilic Ligand Efficiency = -logKi-ALogP. [from Leeson NRDD 2007]",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_mechanism_refs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_mechanism_refs_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/mechanism_refs_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.mechanism_refs_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "mecref_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "mec_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to drug_mechanism table - indicating the mechanism to which the references refer",
            },
            {
                "name": "ref_type",
                "type": "string",
                "mode": "required",
                "description": "Type/source of reference (e.g., 'PubMed','DailyMed')",
            },
            {
                "name": "ref_id",
                "type": "string",
                "mode": "nullable",
                "description": " Identifier for the reference in the source (e.g., PubMed ID or DailyMed setid)",
            },
            {
                "name": "ref_url",
                "type": "string",
                "mode": "nullable",
                "description": " Full URL linking to the reference",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_metabolism_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_metabolism_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/metabolism_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.metabolism_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "met_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "drug_record_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to compound_records. Record representing the drug or other compound for which metabolism is being studied (may not be the same as the substrate being measured)",
            },
            {
                "name": "substrate_record_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to compound_records. Record representing the compound that is the subject of metabolism",
            },
            {
                "name": "metabolite_record_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to compound_records. Record representing the compound that is the result of metabolism",
            },
            {
                "name": "pathway_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Identifier for the metabolic scheme/pathway (may be multiple pathways from one source document)",
            },
            {
                "name": "pathway_key",
                "type": "string",
                "mode": "nullable",
                "description": "Link to original source indicating where the pathway information was found (e.g., Figure 1, page 23)",
            },
            {
                "name": "enzyme_name",
                "type": "string",
                "mode": "nullable",
                "description": " Name of the enzyme responsible for the metabolic conversion",
            },
            {
                "name": "enzyme_tid",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to target_dictionary. TID for the enzyme responsible for the metabolic conversion",
            },
            {
                "name": "met_conversion",
                "type": "string",
                "mode": "nullable",
                "description": " Description of the metabolic conversion",
            },
            {
                "name": "organism",
                "type": "string",
                "mode": "nullable",
                "description": " Organism in which this metabolic reaction occurs",
            },
            {
                "name": "tax_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NCBI Tax ID for the organism in which this metabolic reaction occurs",
            },
            {
                "name": "met_comment",
                "type": "string",
                "mode": "nullable",
                "description": "Additional information regarding the metabolism (e.g., organ system, conditions under which observed, activity of metabolites)",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_metabolism_refs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_metabolism_refs_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/metabolism_refs_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.metabolism_refs_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "metref_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "met_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to record_metabolism table - indicating the metabolism information to which the references refer",
            },
            {
                "name": "ref_type",
                "type": "string",
                "mode": "required",
                "description": "Type/source of reference (e.g., 'PubMed','DailyMed')",
            },
            {
                "name": "ref_id",
                "type": "string",
                "mode": "nullable",
                "description": " Identifier for the reference in the source (e.g., PubMed ID or DailyMed setid)",
            },
            {
                "name": "ref_url",
                "type": "string",
                "mode": "nullable",
                "description": " Full URL linking to the reference",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_molecule_atc_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_molecule_atc_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/molecule_atc_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.molecule_atc_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "mol_atc_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "level5",
                "type": "string",
                "mode": "required",
                "description": "ATC code (foreign key to atc_classification table)",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Drug to which the ATC code applies (foreign key to molecule_dictionary table)",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_molecule_dictionary_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_molecule_dictionary_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/molecule_dictionary_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.molecule_dictionary_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Internal Primary Key for the molecule",
            },
            {
                "name": "pref_name",
                "type": "string",
                "mode": "nullable",
                "description": " Preferred name for the molecule",
            },
            {
                "name": "chembl_id",
                "type": "string",
                "mode": "required",
                "description": "ChEMBL identifier for this compound (for use on web interface etc)",
            },
            {
                "name": "max_phase",
                "type": "integer",
                "mode": "required",
                "description": "Maximum phase of development reached for the compound (4 = approved). Null where max phase has not yet been assigned.",
            },
            {
                "name": "therapeutic_flag",
                "type": "integer",
                "mode": "required",
                "description": "Indicates that a drug has a therapeutic application (as opposed to e.g., an imaging agent, additive etc).",
            },
            {
                "name": "dosed_ingredient",
                "type": "integer",
                "mode": "required",
                "description": "Indicates that the drug is dosed in this form (e.g., a particular salt)",
            },
            {
                "name": "structure_type",
                "type": "string",
                "mode": "required",
                "description": "Indications whether the molecule has a small molecule structure or a protein sequence (MOL indicates an entry in the compound_structures table, SEQ indications an entry in the protein_therapeutics table, NONE indicates an entry in neither table, e.g., structure unknown)",
            },
            {
                "name": "chebi_par_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Preferred ChEBI ID for the compound (where different from assigned)",
            },
            {
                "name": "molecule_type",
                "type": "string",
                "mode": "nullable",
                "description": "Type of molecule (Small molecule, Protein, Antibody, Oligosaccharide, Oligonucleotide, Cell, Unknown)",
            },
            {
                "name": "first_approval",
                "type": "integer",
                "mode": "nullable",
                "description": "Earliest known approval year for the molecule",
            },
            {
                "name": "oral",
                "type": "integer",
                "mode": "required",
                "description": "Indicates whether the drug is known to be administered orally.",
            },
            {
                "name": "parenteral",
                "type": "integer",
                "mode": "required",
                "description": "Indicates whether the drug is known to be administered parenterally",
            },
            {
                "name": "topical",
                "type": "integer",
                "mode": "required",
                "description": "Indicates whether the drug is known to be administered topically.",
            },
            {
                "name": "black_box_warning",
                "type": "integer",
                "mode": "required",
                "description": "Indicates that the drug has a black box warning",
            },
            {
                "name": "natural_product",
                "type": "integer",
                "mode": "required",
                "description": "Indicates whether the compound is natural product-derived (currently curated only for drugs)",
            },
            {
                "name": "first_in_class",
                "type": "integer",
                "mode": "required",
                "description": "Indicates whether this is known to be the first compound of its class (e.g., acting on a particular target).",
            },
            {
                "name": "chirality",
                "type": "integer",
                "mode": "required",
                "description": "Shows whether a drug is dosed as a racemic mixture (0), single stereoisomer (1) or is an achiral molecule (2)",
            },
            {
                "name": "prodrug",
                "type": "integer",
                "mode": "required",
                "description": "Indicates that the molecule is a pro-drug (see molecule hierarchy for active component, where known)",
            },
            {
                "name": "inorganic_flag",
                "type": "integer",
                "mode": "required",
                "description": "Indicates whether the molecule is inorganic (i.e., containing only metal atoms and <2 carbon atoms)",
            },
            {
                "name": "usan_year",
                "type": "integer",
                "mode": "nullable",
                "description": "The year in which the application for a USAN/INN name was made",
            },
            {
                "name": "availability_type",
                "type": "integer",
                "mode": "nullable",
                "description": "The availability type for the drug (0 = discontinued, 1 = prescription only, 2 = over the counter)",
            },
            {
                "name": "usan_stem",
                "type": "string",
                "mode": "nullable",
                "description": "Where the compound has been assigned a USAN name, this indicates the stem, as described in the USAN_STEM table.",
            },
            {
                "name": "polymer_flag",
                "type": "integer",
                "mode": "nullable",
                "description": "Indicates whether a molecule is a small molecule polymer (e.g., polistyrex)",
            },
            {
                "name": "usan_substem",
                "type": "string",
                "mode": "nullable",
                "description": "Where the compound has been assigned a USAN name, this indicates the substem",
            },
            {
                "name": "usan_stem_definition",
                "type": "string",
                "mode": "nullable",
                "description": "Definition of the USAN stem",
            },
            {
                "name": "indication_class",
                "type": "string",
                "mode": "nullable",
                "description": "Indication class(es) assigned to a drug in the USP dictionary",
            },
            {
                "name": "withdrawn_flag",
                "type": "integer",
                "mode": "required",
                "description": "Flag indicating whether the drug has been withdrawn in at least one country (not necessarily in the US)",
            },
            {
                "name": "withdrawn_year",
                "type": "integer",
                "mode": "nullable",
                "description": "Year the drug was first withdrawn in any country",
            },
            {
                "name": "withdrawn_country",
                "type": "string",
                "mode": "nullable",
                "description": "List of countries/regions where the drug has been withdrawn",
            },
            {
                "name": "withdrawn_reason",
                "type": "string",
                "mode": "nullable",
                "description": "Reasons for withdrawl (e.g., safety)",
            },
            {
                "name": "withdrawn_class",
                "type": "string",
                "mode": "nullable",
                "description": " High level categories for the withdrawn reason (e.g., Cardiotoxicity, Hepatotoxicity)",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_molecule_frac_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_molecule_frac_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/molecule_frac_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.molecule_frac_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "mol_frac_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "frac_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to frac_classification table showing the mechanism of action classification of the compound.",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to molecule_dictionary, showing the compound to which the classification applies.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_molecule_hierarchy_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_molecule_hierarchy_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/molecule_hierarchy_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.molecule_hierarchy_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to compounds table. This field holds a list of all of the ChEMBL compounds with associated data (e.g., activity information, approved drugs). Parent compounds that are generated only by removing salts, and which do not themselves have any associated data will not appear here.",
            },
            {
                "name": "parent_molregno",
                "type": "integer",
                "mode": "nullable",
                "description": "Represents parent compound of molregno in first field (i.e., generated by removing salts). Where molregno and parent_molregno are same, the initial ChEMBL compound did not contain a salt component, or else could not be further processed for various reasons (e.g., inorganic mixture). Compounds which are only generated by removing salts will appear in this field only. Those which, themselves, have any associated data (e.g., activity data) or are launched drugs will also appear in the molregno field.",
            },
            {
                "name": "active_molregno",
                "type": "integer",
                "mode": "nullable",
                "description": "Where a compound is a pro-drug, this represents the active metabolite of the 'dosed' compound given by parent_molregno. Where parent_molregno and active_molregno are the same, the compound is not currently known to be a pro-drug. ",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_molecule_hrac_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_molecule_hrac_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/molecule_hrac_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.molecule_hrac_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "mol_hrac_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "hrac_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to hrac_classification table showing the classification for the compound.",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to molecule_dictionary, showing the compound to which this classification applies.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_molecule_irac_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_molecule_irac_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/molecule_irac_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.molecule_irac_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "mol_irac_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "irac_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the irac_classification table showing the mechanism of action classification for the compound.",
            },
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the molecule_dictionary table, showing the compound to which the classification applies.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_molecule_synonyms_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_molecule_synonyms_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/molecule_synonyms_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.molecule_synonyms_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "molregno",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to molecule_dictionary",
            },
            {
                "name": "syn_type",
                "type": "string",
                "mode": "required",
                "description": "Type of name/synonym (e.g., TRADE_NAME, RESEARCH_CODE, USAN)",
            },
            {
                "name": "molsyn_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "res_stem_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to the research_stem table. Where a synonym is a research code, this links to further information about the company associated with that code.",
            },
            {
                "name": "synonyms",
                "type": "string",
                "mode": "nullable",
                "description": " Synonym for the compound",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_organism_class_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_organism_class_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/organism_class_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.organism_class_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "oc_id",
                "type": "integer",
                "mode": "required",
                "description": "Internal primary key",
            },
            {
                "name": "tax_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NCBI taxonomy ID for the organism (corresponding to tax_ids in assay2target and target_dictionary tables)",
            },
            {
                "name": "l1",
                "type": "string",
                "mode": "nullable",
                "description": " Highest level classification (e.g., Eukaryotes, Bacteria, Fungi etc)",
            },
            {
                "name": "l2",
                "type": "string",
                "mode": "nullable",
                "description": " Second level classification",
            },
            {
                "name": "l3",
                "type": "string",
                "mode": "nullable",
                "description": " Third level classification",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_patent_use_codes_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_patent_use_codes_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/patent_use_codes_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.patent_use_codes_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "patent_use_code",
                "type": "string",
                "mode": "required",
                "description": "Primary key. Patent use code from FDA Orange Book",
            },
            {
                "name": "definition",
                "type": "string",
                "mode": "required",
                "description": "Definition for the patent use code, from FDA Orange Book.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_predicted_binding_domains_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_predicted_binding_domains_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/predicted_binding_domains_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.predicted_binding_domains_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "predbind_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "activity_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to the activities table, indicating the compound/assay(+target) combination for which this prediction is made.",
            },
            {
                "name": "site_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to the binding_sites table, indicating the binding site (domain) that the compound is predicted to bind to.",
            },
            {
                "name": "prediction_method",
                "type": "string",
                "mode": "nullable",
                "description": "The method used to assign the binding domain (e.g., 'Single domain' where the protein has only 1 domain, 'Multi domain' where the protein has multiple domains, but only 1 is known to bind small molecules in other proteins).",
            },
            {
                "name": "confidence",
                "type": "string",
                "mode": "nullable",
                "description": "The level of confidence assigned to the prediction (high where the protein has only 1 domain, medium where the compound has multiple domains, but only 1 known small molecule-binding domain).",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_product_patents_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_product_patents_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/product_patents_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.product_patents_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "prod_pat_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
            {
                "name": "product_id",
                "type": "string",
                "mode": "required",
                "description": "Foreign key to products table - FDA application number for the product",
            },
            {
                "name": "patent_no",
                "type": "string",
                "mode": "required",
                "description": "Patent numbers as submitted by the applicant holder for patents covered by the statutory provisions",
            },
            {
                "name": "patent_expire_date",
                "type": "datetime",
                "mode": "required",
                "description": "Date the patent expires as submitted by the applicant holder including applicable extensions",
            },
            {
                "name": "drug_substance_flag",
                "type": "integer",
                "mode": "required",
                "description": "Patents submitted on FDA Form 3542 and listed after August 18, 2003 may have a drug substance flag set to 1, indicating the sponsor submitted the patent as claiming the drug substance",
            },
            {
                "name": "drug_product_flag",
                "type": "integer",
                "mode": "required",
                "description": "Patents submitted on FDA Form 3542 and listed after August 18, 2003 may have a drug product flag set to 1, indicating the sponsor submitted the patent as claiming the drug product",
            },
            {
                "name": "patent_use_code",
                "type": "string",
                "mode": "nullable",
                "description": "Code to designate a use patent that covers the approved indication or use of a drug product",
            },
            {
                "name": "delist_flag",
                "type": "integer",
                "mode": "required",
                "description": "Applicants under Section 505(b)(2) are not required to certify to patents where this flag is set to 1",
            },
            {
                "name": "submission_date",
                "type": "datetime",
                "mode": "nullable",
                "description": "The date on which the FDA receives patent information from the new drug application (NDA) holder. Format is Mmm d, yyyy",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_products_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_products_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/products_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.products_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "dosage_form",
                "type": "string",
                "mode": "nullable",
                "description": " The dosage form of the product (e.g., tablet, capsule etc)",
            },
            {
                "name": "route",
                "type": "string",
                "mode": "nullable",
                "description": " The administration route of the product (e.g., oral, injection etc)",
            },
            {
                "name": "trade_name",
                "type": "string",
                "mode": "nullable",
                "description": " The trade name for the product",
            },
            {
                "name": "approval_date",
                "type": "datetime",
                "mode": "nullable",
                "description": "The FDA approval date for the product (not necessarily first approval of the active ingredient)",
            },
            {
                "name": "ad_type",
                "type": "string",
                "mode": "nullable",
                "description": " RX = prescription, OTC = over the counter, DISCN = discontinued",
            },
            {
                "name": "oral",
                "type": "integer",
                "mode": "nullable",
                "description": "Flag to show whether product is orally delivered",
            },
            {
                "name": "topical",
                "type": "integer",
                "mode": "nullable",
                "description": "Flag to show whether product is topically delivered",
            },
            {
                "name": "parenteral",
                "type": "integer",
                "mode": "nullable",
                "description": "Flag to show whether product is parenterally delivered",
            },
            {
                "name": "black_box_warning",
                "type": "integer",
                "mode": "nullable",
                "description": "Flag to show whether the product label has a black box warning",
            },
            {
                "name": "applicant_full_name",
                "type": "string",
                "mode": "nullable",
                "description": " Name of the company applying for FDA approval",
            },
            {
                "name": "innovator_company",
                "type": "integer",
                "mode": "nullable",
                "description": "Flag to show whether the applicant is the innovator of the product",
            },
            {
                "name": "product_id",
                "type": "string",
                "mode": "required",
                "description": "FDA application number for the product",
            },
            {
                "name": "nda_type",
                "type": "string",
                "mode": "nullable",
                "description": " Abbreviated New Drug Applications (ANDA or generic) are “A”.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_protein_class_synonyms_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_protein_class_synonyms_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/protein_class_synonyms_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.protein_class_synonyms_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "protclasssyn_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "protein_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the PROTEIN_CLASSIFICATION table. The protein_class to which this synonym applies.",
            },
            {
                "name": "protein_class_synonym",
                "type": "string",
                "mode": "nullable",
                "description": "The synonym for the protein class.",
            },
            {
                "name": "syn_type",
                "type": "string",
                "mode": "nullable",
                "description": "The type or origin of the synonym (e.g., ChEMBL, Concept Wiki, UMLS).",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_protein_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_protein_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/protein_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.protein_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "protein_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique identifier for each protein family classification.",
            },
            {
                "name": "parent_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Protein_class_id for the parent of this protein family.",
            },
            {
                "name": "pref_name",
                "type": "string",
                "mode": "nullable",
                "description": " Preferred/full name for this protein family.",
            },
            {
                "name": "short_name",
                "type": "string",
                "mode": "nullable",
                "description": "Short/abbreviated name for this protein family (not necessarily unique).",
            },
            {
                "name": "protein_class_desc",
                "type": "string",
                "mode": "required",
                "description": "Concatenated description of each classification for searching purposes etc.",
            },
            {
                "name": "definition",
                "type": "string",
                "mode": "nullable",
                "description": "Definition of the protein family.",
            },
            {
                "name": "class_level",
                "type": "integer",
                "mode": "required",
                "description": "Level of the class within the hierarchy (level 1 = top level classification)",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_protein_family_classification_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_protein_family_classification_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/protein_family_classification_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.protein_family_classification_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "protein_class_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique identifier for each classification.",
            },
            {
                "name": "protein_class_desc",
                "type": "string",
                "mode": "required",
                "description": "Concatenated description of each classification for searching purposes etc.",
            },
            {
                "name": "l1",
                "type": "string",
                "mode": "required",
                "description": "First level classification (e.g., Enzyme, Transporter, Ion Channel).",
            },
            {
                "name": "l2",
                "type": "string",
                "mode": "nullable",
                "description": " Second level classification.",
            },
            {
                "name": "l3",
                "type": "string",
                "mode": "nullable",
                "description": " Third level classification.",
            },
            {
                "name": "l4",
                "type": "string",
                "mode": "nullable",
                "description": " Fourth level classification.",
            },
            {
                "name": "l5",
                "type": "string",
                "mode": "nullable",
                "description": " Fifth level classification.",
            },
            {
                "name": "l6",
                "type": "string",
                "mode": "nullable",
                "description": " Sixth level classification.",
            },
            {
                "name": "l7",
                "type": "string",
                "mode": "nullable",
                "description": " Seventh level classification.",
            },
            {
                "name": "l8",
                "type": "string",
                "mode": "nullable",
                "description": " Eighth level classification.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_relationship_type_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_relationship_type_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/relationship_type_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.relationship_type_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "relationship_type",
                "type": "string",
                "mode": "required",
                "description": "Relationship_type flag used in the assay2target table",
            },
            {
                "name": "relationship_desc",
                "type": "string",
                "mode": "nullable",
                "description": " Description of relationship_type flags",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_research_companies_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_research_companies_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/research_companies_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.research_companies_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "co_stem_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "res_stem_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to research_stem table.",
            },
            {
                "name": "company",
                "type": "string",
                "mode": "nullable",
                "description": " Name of current company associated with this research code stem.",
            },
            {
                "name": "country",
                "type": "string",
                "mode": "nullable",
                "description": "Country in which the company uses this research code stem.",
            },
            {
                "name": "previous_company",
                "type": "string",
                "mode": "nullable",
                "description": " Previous name of the company associated with this research code stem (e.g., if the company has undergone acquisitions/mergers).",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_research_stem_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_research_stem_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/research_stem_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.research_stem_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "res_stem_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique ID for each research code stem.",
            },
            {
                "name": "research_stem",
                "type": "string",
                "mode": "nullable",
                "description": "The actual stem/prefix used in the research code.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_site_components_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_site_components_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/site_components_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.site_components_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "sitecomp_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "site_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to binding_sites table.",
            },
            {
                "name": "component_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to the component_sequences table, indicating which molecular component of the target is involved in the binding site.",
            },
            {
                "name": "domain_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to the domains table, indicating which domain of the given molecular component is involved in the binding site (where not known, the domain_id may be null).",
            },
            {
                "name": "site_residues",
                "type": "string",
                "mode": "nullable",
                "description": "List of residues from the given molecular component that make up the binding site (where not know, will be null).",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_source_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_source_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/source_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.source_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "src_id",
                "type": "integer",
                "mode": "required",
                "description": "Identifier for each source (used in compound_records and assays tables)",
            },
            {
                "name": "src_description",
                "type": "string",
                "mode": "nullable",
                "description": " Description of the data source",
            },
            {
                "name": "src_short_name",
                "type": "string",
                "mode": "nullable",
                "description": "A short name for each data source, for display purposes",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_structural_alert_sets_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_structural_alert_sets_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/structural_alert_sets_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.structural_alert_sets_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "alert_set_id",
                "type": "integer",
                "mode": "required",
                "description": "Unique ID for the structural alert set",
            },
            {
                "name": "set_name",
                "type": "string",
                "mode": "required",
                "description": "Name (or origin) of the structural alert set",
            },
            {
                "name": "priority",
                "type": "integer",
                "mode": "required",
                "description": "Priority assigned to the structural alert set for display on the ChEMBL interface (priorities >=4 are shown by default).",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_structural_alerts_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_structural_alerts_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/structural_alerts_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.structural_alerts_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "alert_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key. Unique identifier for the structural alert",
            },
            {
                "name": "alert_set_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to structural_alert_sets table indicating which set this particular alert comes from",
            },
            {
                "name": "alert_name",
                "type": "string",
                "mode": "required",
                "description": "A name for the structural alert",
            },
            {
                "name": "smarts",
                "type": "string",
                "mode": "required",
                "description": "SMARTS defining the structural feature that is considered to be an alert",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_target_components_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_target_components_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/target_components_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.target_components_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tid",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the target_dictionary, indicating the target to which the components belong.",
            },
            {
                "name": "component_id",
                "type": "integer",
                "mode": "required",
                "description": "Foreign key to the component_sequences table, indicating which components belong to the target.",
            },
            {
                "name": "targcomp_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key.",
            },
            {
                "name": "homologue",
                "type": "integer",
                "mode": "required",
                "description": "Indicates that the given component is a homologue of the correct component (e.g., from a different species) when set to 1. This may be the case if the sequence for the correct protein/nucleic acid cannot be found in sequence databases. A value of 2 indicates that the sequence given is a representative of a species group, e.g., an E. coli protein to represent the target of a broad-spectrum antibiotic.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_target_dictionary_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_target_dictionary_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/target_dictionary_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.target_dictionary_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tid",
                "type": "integer",
                "mode": "required",
                "description": "Unique ID for the target",
            },
            {
                "name": "target_type",
                "type": "string",
                "mode": "nullable",
                "description": "Describes whether target is a protein, an organism, a tissue etc. Foreign key to TARGET_TYPE table.",
            },
            {
                "name": "pref_name",
                "type": "string",
                "mode": "required",
                "description": "Preferred target name: manually curated",
            },
            {
                "name": "tax_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NCBI taxonomy id of target",
            },
            {
                "name": "organism",
                "type": "string",
                "mode": "nullable",
                "description": " Source organism of molecuar target or tissue, or the target organism if compound activity is reported in an organism rather than a protein or tissue",
            },
            {
                "name": "chembl_id",
                "type": "string",
                "mode": "required",
                "description": "ChEMBL identifier for this target (for use on web interface etc)",
            },
            {
                "name": "species_group_flag",
                "type": "integer",
                "mode": "required",
                "description": "Flag to indicate whether the target represents a group of species, rather than an individual species (e.g., 'Bacterial DHFR'). Where set to 1, indicates that any associated target components will be a representative, rather than a comprehensive set.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_target_relations_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_target_relations_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/target_relations_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.target_relations_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tid",
                "type": "integer",
                "mode": "required",
                "description": "Identifier for target of interest (foreign key to target_dictionary table)",
            },
            {
                "name": "relationship",
                "type": "string",
                "mode": "required",
                "description": "Relationship between two targets (e.g., SUBSET OF, SUPERSET OF, OVERLAPS WITH)",
            },
            {
                "name": "related_tid",
                "type": "integer",
                "mode": "required",
                "description": "Identifier for the target that is related to the target of interest (foreign key to target_dicitionary table)",
            },
            {
                "name": "targrel_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_target_type_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_target_type_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/target_type_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.target_type_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "target_type",
                "type": "string",
                "mode": "required",
                "description": "Target type (as used in target dictionary)",
            },
            {
                "name": "target_desc",
                "type": "string",
                "mode": "nullable",
                "description": " Description of target type",
            },
            {
                "name": "parent_type",
                "type": "string",
                "mode": "nullable",
                "description": "Higher level classification of target_type, allowing grouping of e.g., all 'PROTEIN' targets, all 'NON-MOLECULAR' targets etc.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_tissue_dictionary_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_tissue_dictionary_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/tissue_dictionary_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.tissue_dictionary_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "tissue_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key, numeric ID for each tissue.",
            },
            {
                "name": "uberon_id",
                "type": "string",
                "mode": "nullable",
                "description": "Uberon ontology identifier for this tissue.",
            },
            {
                "name": "pref_name",
                "type": "string",
                "mode": "required",
                "description": "Name for the tissue (in most cases Uberon name).",
            },
            {
                "name": "efo_id",
                "type": "string",
                "mode": "nullable",
                "description": "Experimental Factor Ontology identifier for the tissue.",
            },
            {
                "name": "chembl_id",
                "type": "string",
                "mode": "required",
                "description": "ChEMBL identifier for this tissue (for use on web interface etc)",
            },
            {
                "name": "bto_id",
                "type": "string",
                "mode": "nullable",
                "description": "BRENDA Tissue Ontology identifier for the tissue.",
            },
            {
                "name": "caloha_id",
                "type": "string",
                "mode": "nullable",
                "description": " Swiss Institute for Bioinformatics CALOHA Ontology identifier for the tissue.",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_usan_stems_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_usan_stems_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/usan_stems_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.usan_stems_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "usan_stem_id",
                "type": "integer",
                "mode": "required",
                "description": "Numeric primary key.",
            },
            {
                "name": "stem",
                "type": "string",
                "mode": "required",
                "description": "Stem defined for use in United States Adopted Names.",
            },
            {
                "name": "subgroup",
                "type": "string",
                "mode": "required",
                "description": "More specific subgroup of the stem defined for use in United States Adopted Names.",
            },
            {
                "name": "annotation",
                "type": "string",
                "mode": "nullable",
                "description": "Meaning of the stem (e.g., the class of compound it applies to).",
            },
            {
                "name": "stem_class",
                "type": "string",
                "mode": "nullable",
                "description": " Indicates whether stem is used as a Prefix/Infix/Suffix.",
            },
            {
                "name": "major_class",
                "type": "string",
                "mode": "nullable",
                "description": " Protein family targeted by compounds of this class (e.g., GPCR/Ion channel/Protease) where known/applicable.",
            },
            {
                "name": "who_extra",
                "type": "integer",
                "mode": "nullable",
                "description": "Stem not represented in USAN list, but added from WHO INN stem list (where set to 1).",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_variant_sequences_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_variant_sequences_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/variant_sequences_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.variant_sequences_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "variant_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key, numeric ID for each sequence variant.",
            },
            {
                "name": "mutation",
                "type": "string",
                "mode": "nullable",
                "description": "Details of variant(s) used, with residue positions adjusted to match provided sequence.",
            },
            {
                "name": "accession",
                "type": "string",
                "mode": "nullable",
                "description": "UniProt accesion for the representative sequence used as the base sequence (without variation).",
            },
            {
                "name": "version",
                "type": "integer",
                "mode": "nullable",
                "description": "Version of the UniProt sequence used as the base sequence.",
            },
            {
                "name": "isoform",
                "type": "integer",
                "mode": "nullable",
                "description": "Details of the UniProt isoform used as the base sequence where relevant.",
            },
            {
                "name": "sequence",
                "type": "string",
                "mode": "nullable",
                "description": "Variant sequence formed by adjusting the UniProt base sequence with the specified mutations/variations.",
            },
            {
                "name": "organism",
                "type": "string",
                "mode": "nullable",
                "description": " Organism from which the sequence was obtained.",
            },
            {
                "name": "tax_id",
                "type": "integer",
                "mode": "nullable",
                "description": "NCBI Tax ID for the organism from which the sequence was obtained",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_version_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_version_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/ebi_chembl/chembl_30/output/version_data_output.csv"],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.version_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "name",
                "type": "string",
                "mode": "required",
                "description": "Name of release version",
            },
            {
                "name": "creation_date",
                "type": "datetime",
                "mode": "nullable",
                "description": "Date database created",
            },
            {
                "name": "comments",
                "type": "string",
                "mode": "nullable",
                "description": "Description of release version",
            },
        ],
    )

    # Task to load CSV data to a BigQuery table
    load_warning_refs_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_warning_refs_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/ebi_chembl/chembl_30/output/warning_refs_data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="ebi_chembl.warning_refs_30",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "warnref_id",
                "type": "integer",
                "mode": "required",
                "description": "Primary key for the warning reference",
            },
            {
                "name": "warning_id",
                "type": "integer",
                "mode": "nullable",
                "description": "Foreign key to the drug_warning table",
            },
            {
                "name": "ref_type",
                "type": "string",
                "mode": "nullable",
                "description": "Type/source of reference",
            },
            {
                "name": "ref_id",
                "type": "string",
                "mode": "nullable",
                "description": "Identifier for the reference in the source",
            },
            {
                "name": "ref_url",
                "type": "string",
                "mode": "nullable",
                "description": "Full URL linking to the reference",
            },
        ],
    )

    (
        create_cluster
        >> csv_transform
        >> delete_cluster
        >> [
            load_activities_to_bq,
            load_compound_structures_to_bq,
            load_action_type_to_bq,
            load_activity_properties_to_bq,
            load_activity_smid_to_bq,
            load_activity_stds_lookup_to_bq,
            load_activity_supp_to_bq,
            load_activity_supp_map_to_bq,
            load_assay_class_map_to_bq,
            load_assay_classification_to_bq,
            load_assay_parameters_to_bq,
            load_assay_type_to_bq,
            load_assays_to_bq,
            load_atc_classification_to_bq,
            load_binding_sites_to_bq,
            load_bio_component_sequences_to_bq,
            load_bioassay_ontology_to_bq,
            load_biotherapeutic_components_to_bq,
            load_biotherapeutics_to_bq,
            load_cell_dictionary_to_bq,
            load_chembl_id_lookup_to_bq,
            load_component_class_to_bq,
            load_component_domains_to_bq,
            load_component_go_to_bq,
            load_component_sequences_to_bq,
            load_component_synonyms_to_bq,
            load_compound_properties_to_bq,
            load_compound_records_to_bq,
            load_compound_structural_alerts_to_bq,
            load_confidence_score_lookup_to_bq,
            load_curation_lookup_to_bq,
            load_data_validity_lookup_to_bq,
            load_defined_daily_dose_to_bq,
            load_docs_to_bq,
            load_domains_to_bq,
            load_drug_indication_to_bq,
            load_drug_mechanism_to_bq,
            load_drug_warning_to_bq,
            load_formulations_to_bq,
            load_frac_classification_to_bq,
            load_go_classification_to_bq,
            load_hrac_classification_to_bq,
            load_indication_refs_to_bq,
            load_irac_classification_to_bq,
            load_ligand_eff_to_bq,
            load_mechanism_refs_to_bq,
            load_metabolism_to_bq,
            load_metabolism_refs_to_bq,
            load_molecule_atc_classification_to_bq,
            load_molecule_dictionary_to_bq,
            load_molecule_frac_classification_to_bq,
            load_molecule_hierarchy_to_bq,
            load_molecule_hrac_classification_to_bq,
            load_molecule_irac_classification_to_bq,
            load_molecule_synonyms_to_bq,
            load_organism_class_to_bq,
            load_patent_use_codes_to_bq,
            load_predicted_binding_domains_to_bq,
            load_product_patents_to_bq,
            load_products_to_bq,
            load_protein_class_synonyms_to_bq,
            load_protein_classification_to_bq,
            load_protein_family_classification_to_bq,
            load_relationship_type_to_bq,
            load_research_companies_to_bq,
            load_research_stem_to_bq,
            load_site_components_to_bq,
            load_source_to_bq,
            load_structural_alert_sets_to_bq,
            load_structural_alerts_to_bq,
            load_target_components_to_bq,
            load_target_dictionary_to_bq,
            load_target_relations_to_bq,
            load_target_type_to_bq,
            load_tissue_dictionary_to_bq,
            load_usan_stems_to_bq,
            load_variant_sequences_to_bq,
            load_version_to_bq,
            load_warning_refs_to_bq,
        ]
    )
