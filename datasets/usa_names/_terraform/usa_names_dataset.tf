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


resource "google_bigquery_dataset" "usa_names" {
  dataset_id  = "usa_names"
  project     = var.project_id
  description = "This public dataset was created by the Social Security Administration and contains all names from Social Security card applications for births that occurred in the United States after 1879. Note that many people born before 1937 never applied for a Social Security card, so their names are not included in this data. For others who did apply, records may not show the place of birth, and again their names are not included in the data.\n\nAll data are from a 100% sample of records on Social Security card applications as of the end of February 2015.  To safeguard privacy, the Social Security Administration restricts names to those with at least 5 occurrences."
}

output "bigquery_dataset-usa_names-dataset_id" {
  value = google_bigquery_dataset.usa_names.dataset_id
}
