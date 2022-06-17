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


resource "google_bigquery_table" "mimiciii_demo_admissions" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "admissions"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_admissions-table_id" {
  value = google_bigquery_table.mimiciii_demo_admissions.table_id
}

output "bigquery_table-mimiciii_demo_admissions-id" {
  value = google_bigquery_table.mimiciii_demo_admissions.id
}

resource "google_bigquery_table" "mimiciii_demo_callout" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "callout"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_callout-table_id" {
  value = google_bigquery_table.mimiciii_demo_callout.table_id
}

output "bigquery_table-mimiciii_demo_callout-id" {
  value = google_bigquery_table.mimiciii_demo_callout.id
}

resource "google_bigquery_table" "mimiciii_demo_caregivers" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "caregivers"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_caregivers-table_id" {
  value = google_bigquery_table.mimiciii_demo_caregivers.table_id
}

output "bigquery_table-mimiciii_demo_caregivers-id" {
  value = google_bigquery_table.mimiciii_demo_caregivers.id
}

resource "google_bigquery_table" "mimiciii_demo_chartevents" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "chartevents"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_chartevents-table_id" {
  value = google_bigquery_table.mimiciii_demo_chartevents.table_id
}

output "bigquery_table-mimiciii_demo_chartevents-id" {
  value = google_bigquery_table.mimiciii_demo_chartevents.id
}

resource "google_bigquery_table" "mimiciii_demo_cptevents" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "cptevents"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_cptevents-table_id" {
  value = google_bigquery_table.mimiciii_demo_cptevents.table_id
}

output "bigquery_table-mimiciii_demo_cptevents-id" {
  value = google_bigquery_table.mimiciii_demo_cptevents.id
}

resource "google_bigquery_table" "mimiciii_demo_d_cpt" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "d_cpt"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_d_cpt-table_id" {
  value = google_bigquery_table.mimiciii_demo_d_cpt.table_id
}

output "bigquery_table-mimiciii_demo_d_cpt-id" {
  value = google_bigquery_table.mimiciii_demo_d_cpt.id
}

resource "google_bigquery_table" "mimiciii_demo_d_icd_diagnoses" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "d_icd_diagnoses"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_d_icd_diagnoses-table_id" {
  value = google_bigquery_table.mimiciii_demo_d_icd_diagnoses.table_id
}

output "bigquery_table-mimiciii_demo_d_icd_diagnoses-id" {
  value = google_bigquery_table.mimiciii_demo_d_icd_diagnoses.id
}

resource "google_bigquery_table" "mimiciii_demo_d_icd_procedures" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "d_icd_procedures"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_d_icd_procedures-table_id" {
  value = google_bigquery_table.mimiciii_demo_d_icd_procedures.table_id
}

output "bigquery_table-mimiciii_demo_d_icd_procedures-id" {
  value = google_bigquery_table.mimiciii_demo_d_icd_procedures.id
}

resource "google_bigquery_table" "mimiciii_demo_d_items" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "d_items"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_d_items-table_id" {
  value = google_bigquery_table.mimiciii_demo_d_items.table_id
}

output "bigquery_table-mimiciii_demo_d_items-id" {
  value = google_bigquery_table.mimiciii_demo_d_items.id
}

resource "google_bigquery_table" "mimiciii_demo_d_labitems" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "d_labitems"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_d_labitems-table_id" {
  value = google_bigquery_table.mimiciii_demo_d_labitems.table_id
}

output "bigquery_table-mimiciii_demo_d_labitems-id" {
  value = google_bigquery_table.mimiciii_demo_d_labitems.id
}

resource "google_bigquery_table" "mimiciii_demo_datetimeevents" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "datetimeevents"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_datetimeevents-table_id" {
  value = google_bigquery_table.mimiciii_demo_datetimeevents.table_id
}

output "bigquery_table-mimiciii_demo_datetimeevents-id" {
  value = google_bigquery_table.mimiciii_demo_datetimeevents.id
}

resource "google_bigquery_table" "mimiciii_demo_diagnoses_icd" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "diagnoses_icd"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_diagnoses_icd-table_id" {
  value = google_bigquery_table.mimiciii_demo_diagnoses_icd.table_id
}

output "bigquery_table-mimiciii_demo_diagnoses_icd-id" {
  value = google_bigquery_table.mimiciii_demo_diagnoses_icd.id
}

resource "google_bigquery_table" "mimiciii_demo_drgcodes" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "drgcodes"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_drgcodes-table_id" {
  value = google_bigquery_table.mimiciii_demo_drgcodes.table_id
}

output "bigquery_table-mimiciii_demo_drgcodes-id" {
  value = google_bigquery_table.mimiciii_demo_drgcodes.id
}

resource "google_bigquery_table" "mimiciii_demo_icustays" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "icustays"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_icustays-table_id" {
  value = google_bigquery_table.mimiciii_demo_icustays.table_id
}

output "bigquery_table-mimiciii_demo_icustays-id" {
  value = google_bigquery_table.mimiciii_demo_icustays.id
}

resource "google_bigquery_table" "mimiciii_demo_inputevents_cv" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "inputevents_cv"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_inputevents_cv-table_id" {
  value = google_bigquery_table.mimiciii_demo_inputevents_cv.table_id
}

output "bigquery_table-mimiciii_demo_inputevents_cv-id" {
  value = google_bigquery_table.mimiciii_demo_inputevents_cv.id
}

resource "google_bigquery_table" "mimiciii_demo_inputevents_mv" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "inputevents_mv"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_inputevents_mv-table_id" {
  value = google_bigquery_table.mimiciii_demo_inputevents_mv.table_id
}

output "bigquery_table-mimiciii_demo_inputevents_mv-id" {
  value = google_bigquery_table.mimiciii_demo_inputevents_mv.id
}

resource "google_bigquery_table" "mimiciii_demo_labevents" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "labevents"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_labevents-table_id" {
  value = google_bigquery_table.mimiciii_demo_labevents.table_id
}

output "bigquery_table-mimiciii_demo_labevents-id" {
  value = google_bigquery_table.mimiciii_demo_labevents.id
}

resource "google_bigquery_table" "mimiciii_demo_microbiologyevents" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "microbiologyevents"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_microbiologyevents-table_id" {
  value = google_bigquery_table.mimiciii_demo_microbiologyevents.table_id
}

output "bigquery_table-mimiciii_demo_microbiologyevents-id" {
  value = google_bigquery_table.mimiciii_demo_microbiologyevents.id
}

resource "google_bigquery_table" "mimiciii_demo_outputevents" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "outputevents"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_outputevents-table_id" {
  value = google_bigquery_table.mimiciii_demo_outputevents.table_id
}

output "bigquery_table-mimiciii_demo_outputevents-id" {
  value = google_bigquery_table.mimiciii_demo_outputevents.id
}

resource "google_bigquery_table" "mimiciii_demo_patients" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "patients"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_patients-table_id" {
  value = google_bigquery_table.mimiciii_demo_patients.table_id
}

output "bigquery_table-mimiciii_demo_patients-id" {
  value = google_bigquery_table.mimiciii_demo_patients.id
}

resource "google_bigquery_table" "mimiciii_demo_prescriptions" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "prescriptions"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_prescriptions-table_id" {
  value = google_bigquery_table.mimiciii_demo_prescriptions.table_id
}

output "bigquery_table-mimiciii_demo_prescriptions-id" {
  value = google_bigquery_table.mimiciii_demo_prescriptions.id
}

resource "google_bigquery_table" "mimiciii_demo_procedureevents_mv" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "procedureevents_mv"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_procedureevents_mv-table_id" {
  value = google_bigquery_table.mimiciii_demo_procedureevents_mv.table_id
}

output "bigquery_table-mimiciii_demo_procedureevents_mv-id" {
  value = google_bigquery_table.mimiciii_demo_procedureevents_mv.id
}

resource "google_bigquery_table" "mimiciii_demo_procedures_icd" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "procedures_icd"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_procedures_icd-table_id" {
  value = google_bigquery_table.mimiciii_demo_procedures_icd.table_id
}

output "bigquery_table-mimiciii_demo_procedures_icd-id" {
  value = google_bigquery_table.mimiciii_demo_procedures_icd.id
}

resource "google_bigquery_table" "mimiciii_demo_services" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "services"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_services-table_id" {
  value = google_bigquery_table.mimiciii_demo_services.table_id
}

output "bigquery_table-mimiciii_demo_services-id" {
  value = google_bigquery_table.mimiciii_demo_services.id
}

resource "google_bigquery_table" "mimiciii_demo_transfers" {
  project    = var.project_id
  dataset_id = "mimiciii_demo"
  table_id   = "transfers"
  depends_on = [
    google_bigquery_dataset.mimiciii_demo
  ]
}

output "bigquery_table-mimiciii_demo_transfers-table_id" {
  value = google_bigquery_table.mimiciii_demo_transfers.table_id
}

output "bigquery_table-mimiciii_demo_transfers-id" {
  value = google_bigquery_table.mimiciii_demo_transfers.id
}
