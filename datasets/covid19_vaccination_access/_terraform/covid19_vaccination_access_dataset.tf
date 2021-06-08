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


resource "google_bigquery_dataset" "covid19_vaccination_access" {
  dataset_id  = "covid19_vaccination_access"
  project     = var.project_id
  description = "The dataset contains catchment areas surrounding COVID-19 vaccination sites (sometimes called facilities). A catchment area represents the area within which a site can be reached within a designated period of time. Each vaccination site has a number of catchment areas, each representing a combination of a typical traveling time (for example, 15 minutes or less) and mode of transport (such as, walking, driving, or public transport)."
}

output "bigquery_dataset-covid19_vaccination_access-dataset_id" {
  value = google_bigquery_dataset.covid19_vaccination_access.dataset_id
}
