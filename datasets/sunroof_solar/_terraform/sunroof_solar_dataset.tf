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


resource "google_bigquery_dataset" "sunroof_solar" {
  dataset_id  = "sunroof_solar"
  project     = var.project_id
  description = "Project Sunroof computes how much sunlight hits your roof in a year. Solar viability is determined using a methodology found here: https://www.google.com/get/sunroof/data-explorer/data-explorer-methodology.pdf The use of this data is subject to Google\u0027s Terms of Service. Feel free to include this data from Project Sunroof in other analyses, materials, reports, and communications with the following attribution: Source: Google Project Sunroof data explorer (August 2017)."
}

output "bigquery_dataset-sunroof_solar-dataset_id" {
  value = google_bigquery_dataset.sunroof_solar.dataset_id
}
