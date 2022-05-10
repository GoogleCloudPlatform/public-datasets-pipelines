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


resource "google_bigquery_dataset" "covid19_google_mobility_eu" {
  dataset_id  = "covid19_google_mobility_eu"
  project     = var.project_id
  description = "Terms of use\nIn order to download or use the data or reports, you must agree to the Google Terms of Service: https://policies.google.com/terms\nDescription\nThis dataset aims to provide insights into what has changed in response to policies aimed at combating COVID-19. It reports movement trends over time by geography, across different categories of places such as retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential.\nThis dataset is intended to help remediate the impact of COVID-19. It shouldn\u2019t be used for medical diagnostic, prognostic, or treatment purposes. It also isn\u2019t intended to be used for guidance on personal travel plans.\nTo learn more about the dataset, the place categories, and how we calculate these trends and preserve privacy, do the following:\n\u2022 Visit the help center: https://support.google.com/covid19-mobility.\n\u2022 Or, read the dataset documentation: https://www.google.com/covid19/mobility/data_documentation.html."
  location    = "US"
}

output "bigquery_dataset-covid19_google_mobility_eu-dataset_id" {
  value = google_bigquery_dataset.covid19_google_mobility_eu.dataset_id
}

resource "google_storage_bucket" "covid19-mobility-eu" {
  name                        = "${var.bucket_name_prefix}-covid19-mobility-eu"
  force_destroy               = true
  location                    = "EU"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

output "storage_bucket-covid19-mobility-eu-name" {
  value = google_storage_bucket.covid19-mobility-eu.name
}
