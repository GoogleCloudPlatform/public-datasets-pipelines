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


resource "google_bigquery_dataset" "noaa_passive_bioacoustic" {
  dataset_id  = "noaa_passive_bioacoustic"
  project     = var.project_id
  description = "This dataset basically contains the metadata corresponding to the audio data files present in google cloud storage bucket gs://noaa-passive-bioacoustic/big_query_metadata/"
}

output "bigquery_dataset-noaa_passive_bioacoustic-dataset_id" {
  value = google_bigquery_dataset.noaa_passive_bioacoustic.dataset_id
}
