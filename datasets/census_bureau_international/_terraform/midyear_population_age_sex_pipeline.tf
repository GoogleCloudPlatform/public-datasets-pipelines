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


resource "google_bigquery_table" "midyear_population_age_sex" {
  project    = var.project_id
  dataset_id = "census_bureau_international"
  table_id   = "midyear_population_age_sex"

  description = "Midyear_Population_Age_Sex Dataset"




  depends_on = [
    google_bigquery_dataset.census_bureau_international
  ]
}

output "bigquery_table-midyear_population_age_sex-table_id" {
  value = google_bigquery_table.midyear_population_age_sex.table_id
}

output "bigquery_table-midyear_population_age_sex-id" {
  value = google_bigquery_table.midyear_population_age_sex.id
}
