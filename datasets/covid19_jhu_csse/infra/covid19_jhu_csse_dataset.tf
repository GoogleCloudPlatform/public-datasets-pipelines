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


resource "google_bigquery_dataset" "covid19_jhu_csse" {
  dataset_id  = "covid19_jhu_csse"
  project     = var.project_id
  description = "This is the data repository for the 2019 Novel Coronavirus Visual Dashboard  operated by the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE). This database was created in response to the Coronavirus public health emergency to track reported cases in real-time. The data include the location and number of confirmed COVID-19 cases, deaths and recoveries for all affected countries, aggregated at the appropriate province or state. It was developed to enable researchers, public health authorities and the general public to track the outbreak as it unfolds. Additional information is available in the blog post, Mapping 2019-nCoV (https://systems.jhu.edu/research/public-health/ncov/), and included data sources are listed here:- https://github.com/CSSEGISandData/COVID-19"
}

output "bigquery_dataset-covid19_jhu_csse-dataset_id" {
  value = google_bigquery_dataset.covid19_jhu_csse.dataset_id
}
