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


resource "google_bigquery_table" "sunroof_solar_solar_potential_by_postal_code" {
  project    = var.project_id
  dataset_id = "sunroof_solar"
  table_id   = "solar_potential_by_postal_code"

  description = "Sunroof Solar Potential By Postal Code"




  depends_on = [
    google_bigquery_dataset.sunroof_solar
  ]
}

output "bigquery_table-sunroof_solar_solar_potential_by_postal_code-table_id" {
  value = google_bigquery_table.sunroof_solar_solar_potential_by_postal_code.table_id
}

output "bigquery_table-sunroof_solar_solar_potential_by_postal_code-id" {
  value = google_bigquery_table.sunroof_solar_solar_potential_by_postal_code.id
}
