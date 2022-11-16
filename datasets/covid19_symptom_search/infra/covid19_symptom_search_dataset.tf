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


resource "google_bigquery_dataset" "covid19_symptom_search" {
  dataset_id  = "covid19_symptom_search"
  project     = var.project_id
  description = "The COVID-19 Search Trends symptoms dataset shows aggregated, anonymized trends in Google searches for a broad set of health symptoms, signs, and conditions. The dataset provides a daily or weekly time series for each region showing the relative volume of searches for each symptom.\nThis dataset is intended to help researchers to better understand the impact of COVID-19. It shouldn\u2019t be used for medical diagnostic, prognostic, or treatment purposes. It also isn\u2019t intended to be used for guidance on personal travel plans.\nAs of Dec. 15, 2020, the dataset was expanded to include trends for Australia, Ireland, New Zealand, Singapore, and the United Kingdom. This expanded data is available in new tables that provide data at country and two subregional levels.  We are now producing aggregate weekly values computed from the individual daily values. To account for the newly available weekly-from-daily data, we adopted a new scaling factor for all US symptoms reported in the weekly time series.  The method is described in the updated documentation linked below. We will not be updating existing state/county tables going forward.\nTo learn more about the dataset, how we generate it and preserve privacy, read the dataset documentation:-  https://storage.googleapis.com/gcp-public-data-symptom-search/COVID-19%20Search%20Trends%20symptoms%20dataset%20documentation%20.pdf\nTo visualize the data, try exploring these interactive charts and map of symptom search trends:- https://pair-code.github.io/covid19_symptom_dataset"
}

output "bigquery_dataset-covid19_symptom_search-dataset_id" {
  value = google_bigquery_dataset.covid19_symptom_search.dataset_id
}
