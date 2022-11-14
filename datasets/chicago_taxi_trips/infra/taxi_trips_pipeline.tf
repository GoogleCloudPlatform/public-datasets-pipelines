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


resource "google_bigquery_table" "chicago_taxi_trips_taxi_trips" {
  project     = var.project_id
  dataset_id  = "chicago_taxi_trips"
  table_id    = "taxi_trips"
  description = "This table consists of Taxi trips reported to the City of Chicago in its role as a regulatory agency."
  depends_on = [
    google_bigquery_dataset.chicago_taxi_trips
  ]
}

output "bigquery_table-chicago_taxi_trips_taxi_trips-table_id" {
  value = google_bigquery_table.chicago_taxi_trips_taxi_trips.table_id
}

output "bigquery_table-chicago_taxi_trips_taxi_trips-id" {
  value = google_bigquery_table.chicago_taxi_trips_taxi_trips.id
}
