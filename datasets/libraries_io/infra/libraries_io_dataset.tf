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


resource "google_bigquery_dataset" "libraries_io" {
  dataset_id  = "libraries_io"
  project     = var.project_id
  description = "Libraries.io gathers data on open source software from 33 package managers and 3 source code repositories. We track over 2.4m unique open source projects, 25m repositories and 121m interdependencies between them. This gives Libraries.io a unique understanding of open source software. In this release you will find data about software distributed and/or crafted publicly on the Internet. You will find information about its development, its distribution and its relationship with other software included as a dependency. You will not find any information about the individuals who create and maintain these projects. https://libraries.io/data Attribution: Includes data from Libraries.io Digital Object identifier: 10.5281/zenodo.1196312."
}

output "bigquery_dataset-libraries_io-dataset_id" {
  value = google_bigquery_dataset.libraries_io.dataset_id
}

resource "google_storage_bucket" "libraries-io" {
  name                        = "${var.bucket_name_prefix}-libraries-io"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

output "storage_bucket-libraries-io-name" {
  value = google_storage_bucket.libraries-io.name
}
