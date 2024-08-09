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


resource "google_bigquery_dataset" "open_buildings_v2" {
  dataset_id  = "open_buildings_v2"
  project     = var.project_id
  description = "This new version of Open Buildings extends the spatial coverage to include countries in South and Southeast Asia, and use a newer model with better accuracy, and more recent satellite imagery. This is a dataset of building footprints to support social good applications. This large-scale open dataset contains the outlines of buildings derived from high-resolution satellite imagery."
}

output "bigquery_dataset-open_buildings_v2-dataset_id" {
  value = google_bigquery_dataset.open_buildings_v2.dataset_id
}
