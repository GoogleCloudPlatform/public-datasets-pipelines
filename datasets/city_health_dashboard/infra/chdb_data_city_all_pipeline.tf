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


resource "google_bigquery_table" "city_health_dashboard_chdb_data_city_all" {
  project    = var.project_id
  dataset_id = "city_health_dashboard"
  table_id   = "chdb_data_city_all"

  description = "City Health Dashboard Data Tract"
  depends_on = [
    google_bigquery_dataset.city_health_dashboard
  ]
}

output "bigquery_table-city_health_dashboard_chdb_data_city_all-table_id" {
  value = google_bigquery_table.city_health_dashboard_chdb_data_city_all.table_id
}

output "bigquery_table-city_health_dashboard_chdb_data_city_all-id" {
  value = google_bigquery_table.city_health_dashboard_chdb_data_city_all.id
}
