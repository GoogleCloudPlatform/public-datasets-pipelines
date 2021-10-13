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


resource "google_bigquery_table" "covid19_google_mobility_mobility_report" {
  project    = var.project_id
  dataset_id = "covid19_google_mobility"
  table_id   = "mobility_report"

  description = "Terms of use By downloading or using the data, you agree to Google\u0027s Terms of Service: https://policies.google.com/terms Description This dataset aims to provide insights into what has changed in response to policies aimed at combating COVID-19. It reports movement trends over time by geography, across different categories of places such as retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential. This dataset is intended to help remediate the impact of COVID-19. It shouldn\u2019t be used for medical diagnostic, prognostic, or treatment purposes. It also isn\u2019t intended to be used for guidance on personal travel plans. To learn more about the dataset, the place categories and how we calculate these trends and preserve privacy, read the data documentation: https://www.google.com/covid19/mobility/data_documentation.html"




  depends_on = [
    google_bigquery_dataset.covid19_google_mobility
  ]
}

output "bigquery_table-covid19_google_mobility_mobility_report-table_id" {
  value = google_bigquery_table.covid19_google_mobility_mobility_report.table_id
}

output "bigquery_table-covid19_google_mobility_mobility_report-id" {
  value = google_bigquery_table.covid19_google_mobility_mobility_report.id
}
