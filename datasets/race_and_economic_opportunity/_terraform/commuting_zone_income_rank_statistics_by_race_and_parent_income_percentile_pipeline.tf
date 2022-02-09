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


resource "google_bigquery_table" "race_and_economic_opportunity_commuting_zone_income_rank_statistics_by_race_and_parent_income_percentile" {
  project    = var.project_id
  dataset_id = "race_and_economic_opportunity"
  table_id   = "commuting_zone_income_rank_statistics_by_race_and_parent_income_percentile"

  description = "Commuting Zone Income Rank Statistics by Race and Parent Income Percentile"




  depends_on = [
    google_bigquery_dataset.race_and_economic_opportunity
  ]
}

output "bigquery_table-race_and_economic_opportunity_commuting_zone_income_rank_statistics_by_race_and_parent_income_percentile-table_id" {
  value = google_bigquery_table.race_and_economic_opportunity_commuting_zone_income_rank_statistics_by_race_and_parent_income_percentile.table_id
}

output "bigquery_table-race_and_economic_opportunity_commuting_zone_income_rank_statistics_by_race_and_parent_income_percentile-id" {
  value = google_bigquery_table.race_and_economic_opportunity_commuting_zone_income_rank_statistics_by_race_and_parent_income_percentile.id
}
