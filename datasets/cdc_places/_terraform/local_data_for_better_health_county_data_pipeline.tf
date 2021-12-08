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


resource "google_bigquery_table" "cdc_places_local_data_for_better_health_county_data" {
  project    = var.project_id
  dataset_id = "cdc_places"
  table_id   = "local_data_for_better_health_county_data"

  description = "Local Data for Better Health, County Data"




  depends_on = [
    google_bigquery_dataset.cdc_places
  ]
}

output "bigquery_table-cdc_places_local_data_for_better_health_county_data-table_id" {
  value = google_bigquery_table.cdc_places_local_data_for_better_health_county_data.table_id
}

output "bigquery_table-cdc_places_local_data_for_better_health_county_data-id" {
  value = google_bigquery_table.cdc_places_local_data_for_better_health_county_data.id
}
