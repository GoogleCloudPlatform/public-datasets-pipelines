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


resource "google_bigquery_table" "usa_names_usa_1910_current" {
  project    = var.project_id
  dataset_id = "usa_names"
  table_id   = "usa_1910_current"

  description = "The table contains the number of applicants for a Social Security card by year of birth and sex. The number of such applicants is restricted to U.S. births where the year of birth, sex, State of birth (50 States and District of Columbia) are known, and where the given name is at least 2 characters long.\n\nsource: http://www.ssa.gov/OACT/babynames/limits.html"




  depends_on = [
    google_bigquery_dataset.usa_names
  ]
}

output "bigquery_table-usa_names_usa_1910_current-table_id" {
  value = google_bigquery_table.usa_names_usa_1910_current.table_id
}

output "bigquery_table-usa_names_usa_1910_current-id" {
  value = google_bigquery_table.usa_names_usa_1910_current.id
}
