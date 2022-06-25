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
from airflow.contrib.operators import bigquery_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-05-15",
}


with DAG(
    dag_id="mimicIII.mimicIII",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@monthly",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy admissions table from one bigquery project to another
    admissions = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="admissions",
        source_project_dataset_tables="physionet-data.mimiciii_demo.admissions",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.admissions",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy callout table from one bigquery project to another
    callout = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="callout",
        source_project_dataset_tables="physionet-data.mimiciii_demo.callout",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.callout",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy caregivers table from one bigquery project to another
    caregivers = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="caregivers",
        source_project_dataset_tables="physionet-data.mimiciii_demo.caregivers",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.caregivers",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy chartevents table from one bigquery project to another
    chartevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="chartevents",
        source_project_dataset_tables="physionet-data.mimiciii_demo.chartevents",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.chartevents",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy cptevents table from one bigquery project to another
    cptevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="cptevents",
        source_project_dataset_tables="physionet-data.mimiciii_demo.cptevents",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.cptevents",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d cpt table from one bigquery project to another
    d_cpt = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_cpt",
        source_project_dataset_tables="physionet-data.mimiciii_demo.d_cpt",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.d_cpt",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d icd diagnoses table from one bigquery project to another
    d_icd_diagnoses = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_icd_diagnoses",
        source_project_dataset_tables="physionet-data.mimiciii_demo.d_icd_diagnoses",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.d_icd_diagnoses",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d icd procedures table from one bigquery project to another
    d_icd_procedures = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_icd_procedures",
        source_project_dataset_tables="physionet-data.mimiciii_demo.d_icd_procedures",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.d_icd_procedures",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d_items table from one bigquery project to another
    d_items = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_items",
        source_project_dataset_tables="physionet-data.mimiciii_demo.d_items",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.d_items",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d_labitems table from one bigquery project to another
    d_labitems = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_labitems",
        source_project_dataset_tables="physionet-data.mimiciii_demo.d_labitems",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.d_labitems",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy datetimeevents table from one bigquery project to another
    datetimeevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="datetimeevents",
        source_project_dataset_tables="physionet-data.mimiciii_demo.datetimeevents",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.datetimeevents",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy diagnoses_icd table from one bigquery project to another
    diagnoses_icd = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="diagnoses_icd",
        source_project_dataset_tables="physionet-data.mimiciii_demo.diagnoses_icd",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.diagnoses_icd",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy drgcodes table from one bigquery project to another
    drgcodes = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="drgcodes",
        source_project_dataset_tables="physionet-data.mimiciii_demo.drgcodes",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.drgcodes",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy icustays table from one bigquery project to another
    icustays = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="icustays",
        source_project_dataset_tables="physionet-data.mimiciii_demo.icustays",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.icustays",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy inputevents_cv table from one bigquery project to another
    inputevents_cv = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="inputevents_cv",
        source_project_dataset_tables="physionet-data.mimiciii_demo.inputevents_cv",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.inputevents_cv",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy inputevents_mv table from one bigquery project to another
    inputevents_mv = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="inputevents_mv",
        source_project_dataset_tables="physionet-data.mimiciii_demo.inputevents_mv",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.inputevents_mv",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy labevents table from one bigquery project to another
    labevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="labevents",
        source_project_dataset_tables="physionet-data.mimiciii_demo.labevents",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.labevents",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy microbiologyevents table from one bigquery project to another
    microbiologyevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="microbiologyevents",
        source_project_dataset_tables="physionet-data.mimiciii_demo.microbiologyevents",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.microbiologyevents",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy outputevents table from one bigquery project to another
    outputevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="outputevents",
        source_project_dataset_tables="physionet-data.mimiciii_demo.outputevents",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.outputevents",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy patients table from one bigquery project to another
    patients = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="patients",
        source_project_dataset_tables="physionet-data.mimiciii_demo.patients",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.patients",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy prescriptions table from one bigquery project to another
    prescriptions = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="prescriptions",
        source_project_dataset_tables="physionet-data.mimiciii_demo.prescriptions",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.prescriptions",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy procedureevents_mv table from one bigquery project to another
    procedureevents_mv = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="procedureevents_mv",
        source_project_dataset_tables="physionet-data.mimiciii_demo.procedureevents_mv",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.procedureevents_mv",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy procedures_icd table from one bigquery project to another
    procedures_icd = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="procedures_icd",
        source_project_dataset_tables="physionet-data.mimiciii_demo.procedures_icd",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.procedures_icd",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy services table from one bigquery project to another
    services = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="services",
        source_project_dataset_tables="physionet-data.mimiciii_demo.services",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.services",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy transfers table from one bigquery project to another
    transfers = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="transfers",
        source_project_dataset_tables="physionet-data.mimiciii_demo.transfers",
        destination_project_dataset_table="bigquery-public-data-dev.mimicIII.transfers",
        write_disposition="WRITE_TRUNCATE",
    )

    admissions, callout, caregivers, chartevents, cptevents, d_cpt, d_icd_diagnoses, d_icd_procedures, d_items, d_labitems, datetimeevents, diagnoses_icd, drgcodes, icustays, inputevents_cv, inputevents_mv, labevents, microbiologyevents, outputevents, patients, prescriptions, procedureevents_mv, procedures_icd, services, transfers
