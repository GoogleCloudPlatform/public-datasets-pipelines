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


resource "google_bigquery_dataset" "covid19_vaccination_search_insights" {
  dataset_id  = "covid19_vaccination_search_insights"
  project     = var.project_id
  description = "Terms of use\nTo download or use the data, you must agree to the Google Terms of Service: https://policies.google.com/terms\n\nDescription\nThe COVID-19 Vaccination Search Insights data shows aggregated, anonymized trends in searches related to COVID-19 vaccination. The dataset provides a weekly time series for each region showing the relative interest of Google searches related to COVID-19 vaccination, across several categories.\n\nThe data is intended to help public health officials design, target, and evaluate public education campaigns.\n\nTo explore and download the data, use our interactive dashboard: http://goo.gle/covid19vaccinationinsights\nTo learn more about the dataset, how we generate it and preserve privacy, read the data documentation:\nhttps://storage.googleapis.com/gcs-public-datasets/COVID-19%20Vaccination%20Search%20Insights%20documentation.pdf"
}

output "bigquery_dataset-covid19_vaccination_search_insights-dataset_id" {
  value = google_bigquery_dataset.covid19_vaccination_search_insights.dataset_id
}
