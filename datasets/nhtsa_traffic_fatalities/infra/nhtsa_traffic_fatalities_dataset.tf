/**
 * Copyright 2022 Google LLC
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


resource "google_bigquery_dataset" "nhtsa_traffic_fatalities" {
  dataset_id = "nhtsa_traffic_fatalities"
  project    = var.project_id
}

output "bigquery_dataset-nhtsa_traffic_fatalities-dataset_id" {
  value = google_bigquery_dataset.nhtsa_traffic_fatalities.dataset_id
}
