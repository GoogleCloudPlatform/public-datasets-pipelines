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


resource "google_bigquery_table" "imdb_name_basics" {
  project     = var.project_id
  dataset_id  = "imdb"
  table_id    = "name_basics"
  description = "It consists details about unique identifier of the name/person."
  depends_on = [
    google_bigquery_dataset.imdb
  ]
}

output "bigquery_table-imdb_name_basics-table_id" {
  value = google_bigquery_table.imdb_name_basics.table_id
}

output "bigquery_table-imdb_name_basics-id" {
  value = google_bigquery_table.imdb_name_basics.id
}

resource "google_bigquery_table" "imdb_title_akas" {
  project     = var.project_id
  dataset_id  = "imdb"
  table_id    = "title_akas"
  description = "It consists details about unique identifier of the title_id."
  depends_on = [
    google_bigquery_dataset.imdb
  ]
}

output "bigquery_table-imdb_title_akas-table_id" {
  value = google_bigquery_table.imdb_title_akas.table_id
}

output "bigquery_table-imdb_title_akas-id" {
  value = google_bigquery_table.imdb_title_akas.id
}

resource "google_bigquery_table" "imdb_title_basics" {
  project     = var.project_id
  dataset_id  = "imdb"
  table_id    = "title_basics"
  description = "It consists additional details about unique identifier of the title_id."
  depends_on = [
    google_bigquery_dataset.imdb
  ]
}

output "bigquery_table-imdb_title_basics-table_id" {
  value = google_bigquery_table.imdb_title_basics.table_id
}

output "bigquery_table-imdb_title_basics-id" {
  value = google_bigquery_table.imdb_title_basics.id
}

resource "google_bigquery_table" "imdb_title_crew" {
  project     = var.project_id
  dataset_id  = "imdb"
  table_id    = "title_crew"
  description = "Contains the director and writer information for all the titles in IMDb."
  depends_on = [
    google_bigquery_dataset.imdb
  ]
}

output "bigquery_table-imdb_title_crew-table_id" {
  value = google_bigquery_table.imdb_title_crew.table_id
}

output "bigquery_table-imdb_title_crew-id" {
  value = google_bigquery_table.imdb_title_crew.id
}

resource "google_bigquery_table" "imdb_title_episode" {
  project     = var.project_id
  dataset_id  = "imdb"
  table_id    = "title_episode"
  description = "Contains the tv episode information."
  depends_on = [
    google_bigquery_dataset.imdb
  ]
}

output "bigquery_table-imdb_title_episode-table_id" {
  value = google_bigquery_table.imdb_title_episode.table_id
}

output "bigquery_table-imdb_title_episode-id" {
  value = google_bigquery_table.imdb_title_episode.id
}

resource "google_bigquery_table" "imdb_title_principals" {
  project     = var.project_id
  dataset_id  = "imdb"
  table_id    = "title_principals"
  description = "Contains the principal cast/crew for titles."
  depends_on = [
    google_bigquery_dataset.imdb
  ]
}

output "bigquery_table-imdb_title_principals-table_id" {
  value = google_bigquery_table.imdb_title_principals.table_id
}

output "bigquery_table-imdb_title_principals-id" {
  value = google_bigquery_table.imdb_title_principals.id
}

resource "google_bigquery_table" "imdb_title_ratings" {
  project     = var.project_id
  dataset_id  = "imdb"
  table_id    = "title_ratings"
  description = "Contains the IMDb rating and votes information for titles."
  depends_on = [
    google_bigquery_dataset.imdb
  ]
}

output "bigquery_table-imdb_title_ratings-table_id" {
  value = google_bigquery_table.imdb_title_ratings.table_id
}

output "bigquery_table-imdb_title_ratings-id" {
  value = google_bigquery_table.imdb_title_ratings.id
}
