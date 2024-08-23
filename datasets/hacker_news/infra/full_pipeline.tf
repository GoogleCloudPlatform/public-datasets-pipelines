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


resource "google_bigquery_table" "hacker_news_full" {
  project     = var.project_id
  dataset_id  = "hacker_news"
  table_id    = "full"
  description = "This dataset contains all stories and comments from Hacker News from its launch in 2006.  Each story contains a story id, the author that made the post, when it was written, and the number of points the story received."
  depends_on = [
    google_bigquery_dataset.hacker_news
  ]
}

output "bigquery_table-hacker_news_full-table_id" {
  value = google_bigquery_table.hacker_news_full.table_id
}

output "bigquery_table-hacker_news_full-id" {
  value = google_bigquery_table.hacker_news_full.id
}
