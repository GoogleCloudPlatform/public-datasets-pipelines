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


resource "google_bigquery_dataset" "iowa_liquor_sales" {
  dataset_id  = "iowa_liquor_sales"
  project     = var.project_id
  description = "\"This dataset contains every wholesale purchase of liquor in the State of Iowa by retailers for sale to individuals since January 1, 2012. The State of Iowa controls the wholesale distribution of liquor intended for retail sale (off-premises consumption), which means this dataset offers a complete view of retail liquor consumption in the entire state. The dataset contains every wholesale order of liquor by all grocery stores, liquor stores, convenience stores, etc., with details about the store and location, the exact liquor brand and size, and the number of bottles ordered.\nYou can find more details, as well as sample queries, in the GCP Marketplace here: https://console.cloud.google.com/marketplace/details/iowa-department-of-commerce/iowa-liquor-sales\""
}

output "bigquery_dataset-iowa_liquor_sales-dataset_id" {
  value = google_bigquery_dataset.iowa_liquor_sales.dataset_id
}
