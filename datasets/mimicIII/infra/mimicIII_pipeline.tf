/**
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


resource "google_bigquery_table" "mimicIII_admissions" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "admissions"
  description = "This table consists of an individuals\u0027s admission details in a health centre. Few details include admit time, emergency type, the diagnosis etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_admissions-table_id" {
  value = google_bigquery_table.mimicIII_admissions.table_id
}

output "bigquery_table-mimicIII_admissions-id" {
  value = google_bigquery_table.mimicIII_admissions.id
}

resource "google_bigquery_table" "mimicIII_callout" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "callout"
  description = "This table consists of call out details such as call out status, call out outcome, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_callout-table_id" {
  value = google_bigquery_table.mimicIII_callout.table_id
}

output "bigquery_table-mimicIII_callout-id" {
  value = google_bigquery_table.mimicIII_callout.id
}

resource "google_bigquery_table" "mimicIII_caregivers" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "caregivers"
  description = "This table consists of the id of the caregivers respective to the patients."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_caregivers-table_id" {
  value = google_bigquery_table.mimicIII_caregivers.table_id
}

output "bigquery_table-mimicIII_caregivers-id" {
  value = google_bigquery_table.mimicIII_caregivers.id
}

resource "google_bigquery_table" "mimicIII_chartevents" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "chartevents"
  description = "This table consists of details like subject id, chart time, store time, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_chartevents-table_id" {
  value = google_bigquery_table.mimicIII_chartevents.table_id
}

output "bigquery_table-mimicIII_chartevents-id" {
  value = google_bigquery_table.mimicIII_chartevents.id
}

resource "google_bigquery_table" "mimicIII_cptevents" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "cptevents"
  description = "This table consists of current procedural terminology details like cpt number, cost center, cpt suffix etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_cptevents-table_id" {
  value = google_bigquery_table.mimicIII_cptevents.table_id
}

output "bigquery_table-mimicIII_cptevents-id" {
  value = google_bigquery_table.mimicIII_cptevents.id
}

resource "google_bigquery_table" "mimicIII_d_cpt" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "d_cpt"
  description = "This table consists of cpt details like section header, section range, category etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_d_cpt-table_id" {
  value = google_bigquery_table.mimicIII_d_cpt.table_id
}

output "bigquery_table-mimicIII_d_cpt-id" {
  value = google_bigquery_table.mimicIII_d_cpt.id
}

resource "google_bigquery_table" "mimicIII_d_icd_diagnoses" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "d_icd_diagnoses"
  description = "This table consists of details like icd code, title, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_d_icd_diagnoses-table_id" {
  value = google_bigquery_table.mimicIII_d_icd_diagnoses.table_id
}

output "bigquery_table-mimicIII_d_icd_diagnoses-id" {
  value = google_bigquery_table.mimicIII_d_icd_diagnoses.id
}

resource "google_bigquery_table" "mimicIII_d_icd_procedures" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "d_icd_procedures"
  description = "This table consists of details like icd code, title, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_d_icd_procedures-table_id" {
  value = google_bigquery_table.mimicIII_d_icd_procedures.table_id
}

output "bigquery_table-mimicIII_d_icd_procedures-id" {
  value = google_bigquery_table.mimicIII_d_icd_procedures.id
}

resource "google_bigquery_table" "mimicIII_d_items" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "d_items"
  description = "This table consists of details like item id, label, category etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_d_items-table_id" {
  value = google_bigquery_table.mimicIII_d_items.table_id
}

output "bigquery_table-mimicIII_d_items-id" {
  value = google_bigquery_table.mimicIII_d_items.id
}

resource "google_bigquery_table" "mimicIII_d_labitems" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "d_labitems"
  description = "This table consists of specimen details like item id, fluid, label, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_d_labitems-table_id" {
  value = google_bigquery_table.mimicIII_d_labitems.table_id
}

output "bigquery_table-mimicIII_d_labitems-id" {
  value = google_bigquery_table.mimicIII_d_labitems.id
}

resource "google_bigquery_table" "mimicIII_datetimeevents" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "datetimeevents"
  description = "This table consists of details like icu stay details, chart time, store time etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_datetimeevents-table_id" {
  value = google_bigquery_table.mimicIII_datetimeevents.table_id
}

output "bigquery_table-mimicIII_datetimeevents-id" {
  value = google_bigquery_table.mimicIII_datetimeevents.id
}

resource "google_bigquery_table" "mimicIII_diagnoses_icd" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "diagnoses_icd"
  description = "This table consists of details like admission id, icd code etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_diagnoses_icd-table_id" {
  value = google_bigquery_table.mimicIII_diagnoses_icd.table_id
}

output "bigquery_table-mimicIII_diagnoses_icd-id" {
  value = google_bigquery_table.mimicIII_diagnoses_icd.id
}

resource "google_bigquery_table" "mimicIII_drgcodes" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "drgcodes"
  description = "This table consists of diagnosis related group details like drg type, drg code, etc "
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_drgcodes-table_id" {
  value = google_bigquery_table.mimicIII_drgcodes.table_id
}

output "bigquery_table-mimicIII_drgcodes-id" {
  value = google_bigquery_table.mimicIII_drgcodes.id
}

resource "google_bigquery_table" "mimicIII_icustays" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "icustays"
  description = "This table consists of icu details like time of stay, ward id, care unit etc"
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_icustays-table_id" {
  value = google_bigquery_table.mimicIII_icustays.table_id
}

output "bigquery_table-mimicIII_icustays-id" {
  value = google_bigquery_table.mimicIII_icustays.id
}

resource "google_bigquery_table" "mimicIII_inputevents_cv" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "inputevents_cv"
  description = "This table consists of details like chart time, amount, rate, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_inputevents_cv-table_id" {
  value = google_bigquery_table.mimicIII_inputevents_cv.table_id
}

output "bigquery_table-mimicIII_inputevents_cv-id" {
  value = google_bigquery_table.mimicIII_inputevents_cv.id
}

resource "google_bigquery_table" "mimicIII_inputevents_mv" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "inputevents_mv"
  description = "This table consists of details like chart time, amount, rate, order category name, order id, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_inputevents_mv-table_id" {
  value = google_bigquery_table.mimicIII_inputevents_mv.table_id
}

output "bigquery_table-mimicIII_inputevents_mv-id" {
  value = google_bigquery_table.mimicIII_inputevents_mv.id
}

resource "google_bigquery_table" "mimicIII_labevents" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "labevents"
  description = "This table consists of details like chart time, value, flag etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_labevents-table_id" {
  value = google_bigquery_table.mimicIII_labevents.table_id
}

output "bigquery_table-mimicIII_labevents-id" {
  value = google_bigquery_table.mimicIII_labevents.id
}

resource "google_bigquery_table" "mimicIII_microbiologyevents" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "microbiologyevents"
  description = "This table consists of details like dilution value, isolation, interpretation, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_microbiologyevents-table_id" {
  value = google_bigquery_table.mimicIII_microbiologyevents.table_id
}

output "bigquery_table-mimicIII_microbiologyevents-id" {
  value = google_bigquery_table.mimicIII_microbiologyevents.id
}

resource "google_bigquery_table" "mimicIII_outputevents" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "outputevents"
  description = "This table consists of details like icu stay id, admission id, store time, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_outputevents-table_id" {
  value = google_bigquery_table.mimicIII_outputevents.table_id
}

output "bigquery_table-mimicIII_outputevents-id" {
  value = google_bigquery_table.mimicIII_outputevents.id
}

resource "google_bigquery_table" "mimicIII_patients" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "patients"
  description = "This table consists of an individual\u0027s details like date of birth, gender, subject id, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_patients-table_id" {
  value = google_bigquery_table.mimicIII_patients.table_id
}

output "bigquery_table-mimicIII_patients-id" {
  value = google_bigquery_table.mimicIII_patients.id
}

resource "google_bigquery_table" "mimicIII_prescriptions" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "prescriptions"
  description = "This table consists of details like drug name, drug type, formula, drug strength, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_prescriptions-table_id" {
  value = google_bigquery_table.mimicIII_prescriptions.table_id
}

output "bigquery_table-mimicIII_prescriptions-id" {
  value = google_bigquery_table.mimicIII_prescriptions.id
}

resource "google_bigquery_table" "mimicIII_procedureevents_mv" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "procedureevents_mv"
  description = "This table consists of details like order category name, status description, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_procedureevents_mv-table_id" {
  value = google_bigquery_table.mimicIII_procedureevents_mv.table_id
}

output "bigquery_table-mimicIII_procedureevents_mv-id" {
  value = google_bigquery_table.mimicIII_procedureevents_mv.id
}

resource "google_bigquery_table" "mimicIII_procedures_icd" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "procedures_icd"
  description = "This table consists of details like sequence number, icd code, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_procedures_icd-table_id" {
  value = google_bigquery_table.mimicIII_procedures_icd.table_id
}

output "bigquery_table-mimicIII_procedures_icd-id" {
  value = google_bigquery_table.mimicIII_procedures_icd.id
}

resource "google_bigquery_table" "mimicIII_services" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "services"
  description = "This table consists of details like transfer time, previous service, current service"
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_services-table_id" {
  value = google_bigquery_table.mimicIII_services.table_id
}

output "bigquery_table-mimicIII_services-id" {
  value = google_bigquery_table.mimicIII_services.id
}

resource "google_bigquery_table" "mimicIII_transfers" {
  project     = var.project_id
  dataset_id  = "mimicIII"
  table_id    = "transfers"
  description = "This table consists of details like in time, out time, icu stay id, care unit, ward id, etc."
  depends_on = [
    google_bigquery_dataset.mimicIII
  ]
}

output "bigquery_table-mimicIII_transfers-table_id" {
  value = google_bigquery_table.mimicIII_transfers.table_id
}

output "bigquery_table-mimicIII_transfers-id" {
  value = google_bigquery_table.mimicIII_transfers.id
}
