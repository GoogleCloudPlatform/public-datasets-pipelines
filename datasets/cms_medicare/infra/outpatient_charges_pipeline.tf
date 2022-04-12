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


resource "google_bigquery_table" "cms_medicare_outpatient_charges_2011" {
  project    = var.project_id
  dataset_id = "cms_medicare"
  table_id   = "outpatient_charges_2011"

  description = "CMS Medicare Outpatient Charges 2011"




  depends_on = [
    google_bigquery_dataset.cms_medicare
  ]
}

output "bigquery_table-cms_medicare_outpatient_charges_2011-table_id" {
  value = google_bigquery_table.cms_medicare_outpatient_charges_2011.table_id
}

output "bigquery_table-cms_medicare_outpatient_charges_2011-id" {
  value = google_bigquery_table.cms_medicare_outpatient_charges_2011.id
}

resource "google_bigquery_table" "cms_medicare_outpatient_charges_2012" {
  project    = var.project_id
  dataset_id = "cms_medicare"
  table_id   = "outpatient_charges_2012"

  description = "CMS Medicare Outpatient Charges 2012"




  depends_on = [
    google_bigquery_dataset.cms_medicare
  ]
}

output "bigquery_table-cms_medicare_outpatient_charges_2012-table_id" {
  value = google_bigquery_table.cms_medicare_outpatient_charges_2012.table_id
}

output "bigquery_table-cms_medicare_outpatient_charges_2012-id" {
  value = google_bigquery_table.cms_medicare_outpatient_charges_2012.id
}

resource "google_bigquery_table" "cms_medicare_outpatient_charges_2013" {
  project    = var.project_id
  dataset_id = "cms_medicare"
  table_id   = "outpatient_charges_2013"

  description = "CMS Medicare Outpatient Charges 2013"




  depends_on = [
    google_bigquery_dataset.cms_medicare
  ]
}

output "bigquery_table-cms_medicare_outpatient_charges_2013-table_id" {
  value = google_bigquery_table.cms_medicare_outpatient_charges_2013.table_id
}

output "bigquery_table-cms_medicare_outpatient_charges_2013-id" {
  value = google_bigquery_table.cms_medicare_outpatient_charges_2013.id
}

resource "google_bigquery_table" "cms_medicare_outpatient_charges_2014" {
  project    = var.project_id
  dataset_id = "cms_medicare"
  table_id   = "outpatient_charges_2014"

  description = "CMS Medicare Outpatient Charges 2014"




  depends_on = [
    google_bigquery_dataset.cms_medicare
  ]
}

output "bigquery_table-cms_medicare_outpatient_charges_2014-table_id" {
  value = google_bigquery_table.cms_medicare_outpatient_charges_2014.table_id
}

output "bigquery_table-cms_medicare_outpatient_charges_2014-id" {
  value = google_bigquery_table.cms_medicare_outpatient_charges_2014.id
}
