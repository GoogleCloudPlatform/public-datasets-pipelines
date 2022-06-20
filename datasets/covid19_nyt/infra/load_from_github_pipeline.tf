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


resource "google_bigquery_table" "covid19_nyt_us_counties" {
  project     = var.project_id
  dataset_id  = "covid19_nyt"
  table_id    = "us_counties"
  description = "County-level data for the number of cases and deaths from The New York Times. Sourced from https://github.com/nytimes/covid-19-data."
  depends_on = [
    google_bigquery_dataset.covid19_nyt
  ]
}

output "bigquery_table-covid19_nyt_us_counties-table_id" {
  value = google_bigquery_table.covid19_nyt_us_counties.table_id
}

output "bigquery_table-covid19_nyt_us_counties-id" {
  value = google_bigquery_table.covid19_nyt_us_counties.id
}

resource "google_bigquery_table" "covid19_nyt_us_states" {
  project     = var.project_id
  dataset_id  = "covid19_nyt"
  table_id    = "us_states"
  description = "State-level data for the number of cases and deaths from The New York Times. Sourced from https://github.com/nytimes/covid-19-data."
  depends_on = [
    google_bigquery_dataset.covid19_nyt
  ]
}

output "bigquery_table-covid19_nyt_us_states-table_id" {
  value = google_bigquery_table.covid19_nyt_us_states.table_id
}

output "bigquery_table-covid19_nyt_us_states-id" {
  value = google_bigquery_table.covid19_nyt_us_states.id
}

resource "google_bigquery_table" "covid19_nyt_excess_deaths" {
  project     = var.project_id
  dataset_id  = "covid19_nyt"
  table_id    = "excess_deaths"
  description = "Last update: As of Jan. 18, 2021, The New York Times are no longer updating this excess deaths dataset. We have updated data through the end of 2020 or as far as available.\n\nThe New York Times is releasing data that documents the number of deaths from all causes that have occurred during the coronavirus pandemic for 32 countries. We are compiling this time series data from national and municipal health departments, vital statistics offices and other official sources in order to better understand the true toll of the pandemic and provide a record for researchers and the public.\n\nOfficial Covid-19 death tolls offer a limited view of the impact of the outbreak because they often exclude people who have not been tested and those who died at home. All-cause mortality is widely used by demographers and other researchers to understand the full impact of deadly events, including epidemics, wars and natural disasters. The totals in this data include deaths from Covid-19 as well as those from other causes, likely including people who could not be treated or did not seek treatment for other conditions.\n\nWe have used this data to produce graphics tracking the oubreak\u0027s toll and stories about the United States, Ecuador, Russia, Turkey, Sweden and other countries. We would like to thank a number of demographers and other researchers, listed at the end, who have provided data or helped interpret it.\n\nSourced from https://github.com/nytimes/covid-19-data/tree/master/excess-deaths."
  depends_on = [
    google_bigquery_dataset.covid19_nyt
  ]
}

output "bigquery_table-covid19_nyt_excess_deaths-table_id" {
  value = google_bigquery_table.covid19_nyt_excess_deaths.table_id
}

output "bigquery_table-covid19_nyt_excess_deaths-id" {
  value = google_bigquery_table.covid19_nyt_excess_deaths.id
}

resource "google_bigquery_table" "covid19_nyt_mask_use_by_county" {
  project     = var.project_id
  dataset_id  = "covid19_nyt"
  table_id    = "mask_use_by_county"
  description = "This data comes from a large number of interviews conducted online by the global data and survey firm Dynata at the request of The New York Times. The firm asked a question about mask use to obtain 250,000 survey responses between July 2 and July 14, enough data to provide estimates more detailed than the state level. (Several states have imposed new mask requirements since the completion of these interviews.)\n\nSpecifically, each participant was asked: How often do you wear a mask in public when you expect to be within six feet of another person?\n\nThis survey was conducted a single time, and at this point we have no plans to update the data or conduct the survey again.\n\nSourced from https://github.com/nytimes/covid-19-data/tree/master/mask-use."
  depends_on = [
    google_bigquery_dataset.covid19_nyt
  ]
}

output "bigquery_table-covid19_nyt_mask_use_by_county-table_id" {
  value = google_bigquery_table.covid19_nyt_mask_use_by_county.table_id
}

output "bigquery_table-covid19_nyt_mask_use_by_county-id" {
  value = google_bigquery_table.covid19_nyt_mask_use_by_county.id
}
