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


resource "google_bigquery_dataset" "google_political_ads" {
  dataset_id  = "google_political_ads"
  project     = var.project_id
  description = "Overview: This dataset contains information on how much money is spent by verified advertisers on political advertising across Google Ad Services. In addition, insights on demographic targeting used in political ad campaigns by these advertisers are also provided. Finally, links to the actual political ad in the Google Transparency Report (https://transparencyreport.google.com/) are provided. Data for an election expires 7 years after the election. After this point, the data are removed from the dataset and are no longer available.\n\nUpdate frequency: Weekly\n\nDataset source: Transparency Report: Political Advertising on Google\n\nTerms of use:\n\nSee the GCP Marketplace listing for more details and sample queries: https://console.cloud.google.com/marketplace/details/transparency-report/google-political-ads\n\nFor more information see:\nThe Political Advertising on Google Transparency Report at\nhttps://transparencyreport.google.com/political-ads/home\n\nThe supporting Frequently Asked Questions at\nhttps://support.google.com/transparencyreport/answer/9575640?hl=en\u0026ref_topic=7295796"
}

output "bigquery_dataset-google_political_ads-dataset_id" {
  value = google_bigquery_dataset.google_political_ads.dataset_id
}
