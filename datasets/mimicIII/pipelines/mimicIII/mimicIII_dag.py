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
    "start_date": "2022-05-27",
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
        source_project_dataset_tables="{{ var.json.mimicIII.admissions.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.admissions.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy callout table from one bigquery project to another
    callout = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="callout",
        source_project_dataset_tables="{{ var.json.mimicIII.callout.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.callout.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy caregivers table from one bigquery project to another
    caregivers = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="caregivers",
        source_project_dataset_tables="{{ var.json.mimicIII.caregivers.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.caregivers.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy chartevents table from one bigquery project to another
    chartevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="chartevents",
        source_project_dataset_tables="{{ var.json.mimicIII.chartevents.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.chartevents.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy cptevents table from one bigquery project to another
    cptevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="cptevents",
        source_project_dataset_tables="{{ var.json.mimicIII.cptevents.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.cptevents.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d cpt table from one bigquery project to another
    d_cpt = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_cpt",
        source_project_dataset_tables="{{ var.json.mimicIII.d_cpt.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.d_cpt.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d icd diagnoses table from one bigquery project to another
    d_icd_diagnoses = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_icd_diagnoses",
        source_project_dataset_tables="{{ var.json.mimicIII.d_icd_diagnoses.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.d_icd_diagnoses.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d icd procedures table from one bigquery project to another
    d_icd_procedures = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_icd_procedures",
        source_project_dataset_tables="{{ var.json.mimicIII.d_icd_procedures.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.d_icd_procedures.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d_items table from one bigquery project to another
    d_items = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_items",
        source_project_dataset_tables="{{ var.json.mimicIII.d_items.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.d_items.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy d_labitems table from one bigquery project to another
    d_labitems = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="d_labitems",
        source_project_dataset_tables="{{ var.json.mimicIII.d_labitems.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.d_labitems.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy datetimeevents table from one bigquery project to another
    datetimeevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="datetimeevents",
        source_project_dataset_tables="{{ var.json.mimicIII.datetimeevents.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.datetimeevents.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy diagnoses_icd table from one bigquery project to another
    diagnoses_icd = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="diagnoses_icd",
        source_project_dataset_tables="{{ var.json.mimicIII.diagnoses_icd.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.diagnoses_icd.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy drgcodes table from one bigquery project to another
    drgcodes = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="drgcodes",
        source_project_dataset_tables="{{ var.json.mimicIII.drgcodes.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.drgcodes.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy icustays table from one bigquery project to another
    icustays = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="icustays",
        source_project_dataset_tables="{{ var.json.mimicIII.icustays.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.icustays.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy inputevents_cv table from one bigquery project to another
    inputevents_cv = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="inputevents_cv",
        source_project_dataset_tables="{{ var.json.mimicIII.inputevents_cv.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.inputevents_cv.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy inputevents_mv table from one bigquery project to another
    inputevents_mv = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="inputevents_mv",
        source_project_dataset_tables="{{ var.json.mimicIII.inputevents_mv.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.inputevents_mv.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy labevents table from one bigquery project to another
    labevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="labevents",
        source_project_dataset_tables="{{ var.json.mimicIII.labevents.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.labevents.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy microbiologyevents table from one bigquery project to another
    microbiologyevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="microbiologyevents",
        source_project_dataset_tables="{{ var.json.mimicIII.microbiologyevents.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.microbiologyevents.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy outputevents table from one bigquery project to another
    outputevents = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="outputevents",
        source_project_dataset_tables="{{ var.json.mimicIII.outputevents.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.outputevents.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy patients table from one bigquery project to another
    patients = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="patients",
        source_project_dataset_tables="{{ var.json.mimicIII.patients.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.patients.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy prescriptions table from one bigquery project to another
    prescriptions = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="prescriptions",
        source_project_dataset_tables="{{ var.json.mimicIII.prescriptions.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.prescriptions.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy procedureevents_mv table from one bigquery project to another
    procedureevents_mv = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="procedureevents_mv",
        source_project_dataset_tables="{{ var.json.mimicIII.procedureevents_mv.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.procedureevents_mv.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy procedures_icd table from one bigquery project to another
    procedures_icd = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="procedures_icd",
        source_project_dataset_tables="{{ var.json.mimicIII.procedures_icd.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.procedures_icd.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy services table from one bigquery project to another
    services = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="services",
        source_project_dataset_tables="{{ var.json.mimicIII.services.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.services.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    # Copy transfers table from one bigquery project to another
    transfers = bigquery_to_bigquery.BigQueryToBigQueryOperator(
        task_id="transfers",
        source_project_dataset_tables="{{ var.json.mimicIII.transfers.source_table }}",
        destination_project_dataset_table="{{ var.json.mimicIII.transfers.destination_table }}",
        write_disposition="WRITE_TRUNCATE",
    )

    admissions, callout, caregivers, chartevents, cptevents, d_cpt, d_icd_diagnoses, d_icd_procedures, d_items, d_labitems, datetimeevents, diagnoses_icd, drgcodes, icustays, inputevents_cv, inputevents_mv, labevents, microbiologyevents, outputevents, patients, prescriptions, procedureevents_mv, procedures_icd, services, transfers
