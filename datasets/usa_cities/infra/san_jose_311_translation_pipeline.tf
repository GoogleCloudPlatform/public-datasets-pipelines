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


resource "google_bigquery_table" "usa_cities_san_jose_311_english_spanish" {
  project     = var.project_id
  dataset_id  = "usa_cities"
  table_id    = "san_jose_311_english_spanish"
  description = "Translation pairs of English to Spanish phrases."
  depends_on = [
    google_bigquery_dataset.usa_cities
  ]
}

output "bigquery_table-usa_cities_san_jose_311_english_spanish-table_id" {
  value = google_bigquery_table.usa_cities_san_jose_311_english_spanish.table_id
}

output "bigquery_table-usa_cities_san_jose_311_english_spanish-id" {
  value = google_bigquery_table.usa_cities_san_jose_311_english_spanish.id
}

resource "google_bigquery_table" "usa_cities_san_jose_311_vietnamese_english" {
  project     = var.project_id
  dataset_id  = "usa_cities"
  table_id    = "san_jose_311_vietnamese_english"
  description = "Translation pairs of Vietnamese to English phrases."
  depends_on = [
    google_bigquery_dataset.usa_cities
  ]
}

output "bigquery_table-usa_cities_san_jose_311_vietnamese_english-table_id" {
  value = google_bigquery_table.usa_cities_san_jose_311_vietnamese_english.table_id
}

output "bigquery_table-usa_cities_san_jose_311_vietnamese_english-id" {
  value = google_bigquery_table.usa_cities_san_jose_311_vietnamese_english.id
}
