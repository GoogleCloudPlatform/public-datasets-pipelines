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

import csv
import datetime
import json
import logging
import os
import pathlib
import time
import typing

import pandas as pd
import sqlalchemy
from google.cloud import storage
from google.cloud.sql.connector import Connector

INT_COLS = [
    "cpd_str_alert_id",
    "tid",
    "src_id",
    "actsm_id",
    "priority",
    "assay_tax_id",
    "confidence_score",
    "molsyn_id",
    "isoform",
    "assay_id",
    "related_tid",
    "protein_class_id",
    "alert_id",
    "warnref_id",
    "comp_go_id",
    "frac_class_id",
    "targrel_id",
    "biocomp_id",
    "alert_set_id",
    "pathway_id",
    "substrate_record_id",
    "active_molregno",
    "natural_product",
    "drug_substance_flag",
    "disease_efficacy",
    "result_flag",
    "aromatic_rings",
    "drug_record_id",
    "res_stem_id",
    "toid",
    "start_position",
    "year",
    "ap_id",
    "metabolite_record_id",
    "species_group_flag",
    "heavy_atoms",
    "parent_molregno",
    "domain_id",
    "inorganic_flag",
    "homologue",
    "therapeutic_flag",
    "component_id",
    "hba_lipinski",
    "max_phase_for_ind",
    "activity_id",
    "parent_id",
    "black_box_warning",
    "std_act_id",
    "mecref_id",
    "standard_flag",
    "who_extra",
    "potential_duplicate",
    "availability_type",
    "num_ro5_violations",
    "normal_range_max",
    "dosed_ingredient",
    "drug_product_flag",
    "prodrug",
    "hbd_lipinski",
    "ass_cls_map_id",
    "direct_interaction",
    "tissue_id",
    "usan_stem_id",
    "num_lipinski_ro5_violations",
    "irac_class_id",
    "predbind_id",
    "pubmed_id",
    "end_position",
    "indref_id",
    "standard_upper_value",
    "hba",
    "met_id",
    "mec_id",
    "cell_id",
    "last_active",
    "warning_year",
    "warning_id",
    "delist_flag",
    "assay_param_id",
    "co_stem_id",
    "record_id",
    "ddd_id",
    "enzyme_tid",
    "class_level",
    "first_approval",
    "mol_irac_id",
    "compsyn_id",
    "oral",
    "drugind_id",
    "mol_atc_id",
    "molregno",
    "rtb",
    "targcomp_id",
    "formulation_id",
    "mol_hrac_id",
    "hbd",
    "sitecomp_id",
    "smid",
    "hrac_class_id",
    "chebi_par_id",
    "site_id",
    "rgid",
    "version",
    "tax_id",
    "prod_pat_id",
    "as_id",
    "cell_source_tax_id",
    "withdrawn_flag",
    "innovator_company",
    "topical",
    "protclasssyn_id",
    "assay_class_id",
    "metref_id",
    "first_in_class",
    "max_phase",
    "oc_id",
    "polymer_flag",
    "chirality",
    "usan_year",
    "doc_id",
    "compd_id",
    "molecular_mechanism",
    "comp_class_id",
    "variant_id",
    "withdrawn_year",
    "parenteral",
    "mol_frac_id",
    "entity_id",
]
FLOAT_COLS = [
    "psa",
    "cx_most_bpka",
    "le",
    "normal_range_min",
    "sei",
    "full_mwt",
    "upper_value",
    "mw_monoisotopic",
    "value",
    "bei",
    "standard_value",
    "qed_weighted",
    "pchembl_value",
    "cx_logd",
    "cx_logp",
    "cx_most_apka",
    "alogp",
    "ddd_value",
    "lle",
    "mw_freebase",
]
STR_COLS = [
    "description",
    "domain_name",
    "cell_name",
    "compound_name",
    "l5",
    "assay_cell_type",
    "bao_endpoint",
    "ro3_pass",
    "assay_category",
    "standard_text_value",
    "level2_description",
    "uo_units",
    "first_page",
    "assay_type",
    "patent_id",
    "irac_code",
    "src_short_name",
    "parent_go_id",
    "assay_subcellular_fraction",
    "assay_organism",
    "strength",
    "domain_type",
    "definition",
    "cellosaurus_id",
    "src_assay_id",
    "caloha_id",
    "target_desc",
    "component_synonym",
    "l2",
    "level4",
    "ref_type",
    "pathway_key",
    "standard_inchi",
    "activity_comment",
    "indication_class",
    "major_class",
    "ad_type",
    "chembl_id",
    "stem_class",
    "molecule_type",
    "assay_desc",
    "protein_class_synonym",
    "target_type",
    "annotation",
    "atc_code",
    "dosage_form",
    "doi",
    "standard_units",
    "curated_by",
    "level1",
    "issue",
    "usan_stem",
    "comments",
    "met_comment",
    "src_compound_id",
    "doc_type",
    "l4",
    "product_id",
    "ddd_admr",
    "authors",
    "smarts",
    "confidence",
    "type",
    "ddd_comment",
    "protein_class_desc",
    "title",
    "assay_tissue",
    "ingredient",
    "active_ingredient",
    "nda_type",
    "entity_type",
    "hrac_code",
    "ddd_units",
    "cell_source_tissue",
    "clo_id",
    "helm_notation",
    "company",
    "mesh_id",
    "aidx",
    "ref_url",
    "usan_stem_definition",
    "sequence",
    "selectivity_comment",
    "efo_id",
    "qudt_units",
    "level3_description",
    "warning_class",
    "subgroup",
    "applicant_full_name",
    "assay_strain",
    "withdrawn_country",
    "trade_name",
    "source",
    "level4_description",
    "ref_id",
    "text_value",
    "withdrawn_reason",
    "src_description",
    "action_type",
    "prediction_method",
    "synonyms",
    "country",
    "label",
    "component_type",
    "mechanism_comment",
    "molfile",
    "stem",
    "domain_description",
    "standard_relation",
    "level2",
    "full_molformula",
    "molecular_species",
    "pref_name",
    "accession",
    "syn_type",
    "units",
    "site_residues",
    "bao_id",
    "l1",
    "uberon_id",
    "compound_key",
    "standard_inchi_key",
    "relationship_desc",
    "l7",
    "ridx",
    "patent_no",
    "alert_name",
    "warning_country",
    "relationship",
    "efo_term",
    "relationship_type",
    "standard_type",
    "l3",
    "assay_test_type",
    "level3",
    "cell_description",
    "cell_ontology_id",
    "set_name",
    "bao_format",
    "data_validity_comment",
    "warning_type",
    "relation",
    "cell_source_organism",
    "db_source",
    "site_name",
    "db_version",
    "abstract",
    "source_domain_id",
    "status",
    "path",
    "usan_substem",
    "patent_use_code",
    "bto_id",
    "cl_lincs_id",
    "route",
    "l6",
    "who_name",
    "binding_site_comment",
    "enzyme_name",
    "cidx",
    "sequence_md5sum",
    "organism",
    "frac_code",
    "short_name",
    "canonical_smiles",
    "previous_company",
    "target_mapping",
    "aspect",
    "name",
    "level5",
    "class_type",
    "warning_description",
    "level1_description",
    "mesh_heading",
    "research_stem",
    "mutation",
    "withdrawn_class",
    "last_page",
    "l8",
    "journal",
    "met_conversion",
    "mechanism_of_action",
    "parent_type",
    "volume",
    "go_id",
    "structure_type",
]
DATETIME_COLS = [
    "submission_date",
    "creation_date",
    "approval_date",
    "patent_expire_date",
]
COLUMNS_NL = [
    "molfile",
    "authors",
    "abstract",
    "mechanism_comment",
    "selectivity_comment",
]
COLUMNS_S = ["compound_name"]
COLUMNS_R = ["mechanism_comment"]
COLUMNS_P = ["mechanism_comment"]
COL_DATA_CLN_TABLES = [
    "compound_structures",
    "compound_records",
    "docs",
    "drug_mechanism",
]


def main(
    instance_connection_name: str,
    user: str,
    password: str,
    database: str,
    tables: list,
    chunksize: int,
    output_folder: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_folder: str,
) -> None:
    logging.info(
        f"ebi_chembl Dataset chembl_30 pipeline process started for table(s) -  {tables} at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    logging.info(f"Creating '{output_folder}' folder.")
    pathlib.Path(f"{output_folder}").mkdir(parents=True, exist_ok=True)
    logging.info(
        "Waiting for 60 seconds to get database instance up and ready to accept connections."
    )
    time.sleep(60)
    logging.info(f"Connecting to db instance {instance_connection_name} ...")
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=lambda: Connector().connect(
            instance_connection_name,
            "pg8000",
            user=user,
            password=password,
            db=database,
        ),
    )
    logging.info(f"Done.. and assigned to variable pool {pool}")
    if "activities" not in tables:
        for table in tables:
            logging.info(f"Process started for table - {table}.")
            df_chunk = get_table_data(pool, table, chunksize)
            table_to_csv(output_folder, table, df_chunk)
    else:
        cursor = pool.connect()
        row_count = cursor.execute(f"select count(*) from {tables[0]}").fetchall()[0][0]
        limit = chunksize
        offset = 0
        for idx, _ in enumerate(range(0, row_count, limit)):
            res = cursor.execute(
                f"select * from {tables[0]} offset {offset} limit {limit}"
            )
            offset += limit
            data = res.fetchall()
            logging.info(f" Writing data to csv {idx*limit} - {row_count}")
            if idx == 0:
                write_to_file(output_folder, tables[0], data, "w")
            elif data:
                write_to_file(output_folder, tables[0], data, "a")
    for file in os.listdir(output_folder):
        source_file = f"{output_folder}/{file}"
        target_gcs_path = f"{target_gcs_folder}/{file}"
        if os.path.exists(source_file):
            upload_file_to_gcs(source_file, target_gcs_bucket, target_gcs_path)
        else:
            raise FileNotFoundError(f"{source_file} not found in {os.getcwd()}")
    logging.info(
        f"ebi_chembl Dataset chembl_30 pipeline process completed for table(s) -  {tables} at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def get_table_data(
    connection: sqlalchemy.engine.base.Engine, table: str, chunksize: int
) -> typing.Generator[pd.core.frame.DataFrame, None, None]:
    logging.info(f"\tReading data for table = {table}")
    df_chunk = pd.read_sql_query(
        f"SELECT * FROM {table};", con=connection, chunksize=chunksize
    )
    return df_chunk


def table_to_csv(
    output_folder: pathlib.Path,
    table: str,
    df_chunk: pd.io.parsers.readers.TextFileReader,
) -> None:
    for idx, chunk in enumerate(df_chunk):
        if table in COL_DATA_CLN_TABLES:
            logging.info(f"\tCleaning column data for {table}.")
            chunk = coldata_clean(chunk)
        logging.info(f"\tHandling datatypes for {table}")
        chunk = dtype_clean(chunk)
        if not idx:
            logging.info(f"\tWriting data to '{output_folder}/{table}_data_output.csv'")
            chunk.to_csv(f"{output_folder}/{table}_data_output.csv", index=False)
        else:
            logging.info(
                f"\tAppending data to '{output_folder}/{table}_data_output.csv'"
            )
            chunk.to_csv(
                f"{output_folder}/{table}_data_output.csv",
                index=False,
                mode="a",
                header=False,
            )


def coldata_clean(chunk: pd.DataFrame) -> pd.DataFrame:
    for col in chunk.columns:
        if col in COLUMNS_NL:
            chunk = replace_data(chunk, col, "\n", "\\n")
        if col in COLUMNS_P:
            chunk = replace_data(chunk, col, '"', "'")
        if col in COLUMNS_R:
            chunk = replace_data(chunk, col, "\r", "\\n")
        if col in COLUMNS_S:
            chunk = replace_data(chunk, col, "\n", "")
    return chunk


def replace_data(
    chunk: pd.DataFrame, col: str, match: str, replace: str
) -> pd.DataFrame:
    logging.info(
        f"Replacing unicode char in '{col}' replacing '{match}' with '{replace}'."
    )
    chunk[col] = chunk[col].apply(lambda x: str(x).replace(match, replace))
    return chunk


def dtype_clean(chunk: pd.DataFrame) -> pd.DataFrame:
    cols = list(chunk.columns)
    for col in cols:
        if col in INT_COLS:
            chunk[col] = chunk[col].astype("Int64")
        elif col in FLOAT_COLS:
            chunk[col] = chunk[col].astype("float64")
        elif col in STR_COLS:
            chunk[col] = chunk[col].astype("object")
        elif col in DATETIME_COLS:
            chunk[col] = chunk[col].astype("datetime64[ns]")
    return chunk


def write_to_file(
    output_folder: pathlib.Path, table: str, data: list, mode: str
) -> None:
    file = f"{output_folder}/{table}_data_output.csv"
    with open(file, mode=mode) as fb:
        writer = csv.writer(fb, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)


def upload_file_to_gcs(
    source_file: pathlib.Path, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(
        f"Uploading output file {source_file} to gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(source_file)
    logging.info("Successfully uploaded file to gcs bucket.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        instance_connection_name=os.environ.get("INSTANCE_CONNECTION_NAME", ""),
        user=os.environ.get("USER", ""),
        password=os.environ.get("PASSWORD", ""),
        database=os.environ.get("DATABASE", ""),
        tables=json.loads(os.environ.get("TABLES", "[]")),
        chunksize=int(os.environ.get("CHUNKSIZE", "100000")),
        output_folder=os.environ.get("OUTPUT_FOLDER", ""),
        target_gcs_bucket=os.environ.get("TARGET_GCS_BUCKET", ""),
        target_gcs_folder=os.environ.get("TARGET_GCS_FOLDER", ""),
    )
