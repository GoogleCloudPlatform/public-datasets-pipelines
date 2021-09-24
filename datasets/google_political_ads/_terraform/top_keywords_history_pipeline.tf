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


resource "google_bigquery_table" "top_keywords_history" {
  project    = var.project_id
  dataset_id = "google_political_ads"
  table_id   = "top_keywords_history"

  description = "The \u201cTop Keywords\u201d section of the US report was removed and updates to this table were terminated in December 2019. The table reflects historical data. This table contains the information for the top six keywords on which political advertisers have spent money during an election cycle. This data is only provided for US elections. The primary key is election_cycle, report_date."




  depends_on = [
    google_bigquery_dataset.google_political_ads
  ]
}

output "bigquery_table-top_keywords_history-table_id" {
  value = google_bigquery_table.top_keywords_history.table_id
}

output "bigquery_table-top_keywords_history-id" {
  value = google_bigquery_table.top_keywords_history.id
}
