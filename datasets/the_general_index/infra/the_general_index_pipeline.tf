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


resource "google_bigquery_table" "the_general_index_the_general_index" {
  project     = var.project_id
  dataset_id  = "the_general_index"
  table_id    = "the_general_index"
  description = "The General Index"
  depends_on = [
    google_bigquery_dataset.the_general_index
  ]
}

output "bigquery_table-the_general_index_the_general_index-table_id" {
  value = google_bigquery_table.the_general_index_the_general_index.table_id
}

output "bigquery_table-the_general_index_the_general_index-id" {
  value = google_bigquery_table.the_general_index_the_general_index.id
}
