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


resource "google_bigquery_table" "epa_historical_air_quality_annual_summaries" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "annual_summaries"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_annual_summaries-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_annual_summaries.table_id
}

output "bigquery_table-epa_historical_air_quality_annual_summaries-id" {
  value = google_bigquery_table.epa_historical_air_quality_annual_summaries.id
}

resource "google_bigquery_table" "epa_historical_air_quality_co_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "co_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_co_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_co_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_co_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_co_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_co_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "co_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_co_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_co_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_co_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_co_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_hap_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "hap_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_hap_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_hap_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_hap_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_hap_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_hap_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "hap_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_hap_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_hap_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_hap_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_hap_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_lead_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "lead_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_lead_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_lead_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_lead_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_lead_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_no2_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "no2_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_no2_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_no2_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_no2_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_no2_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_no2_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "no2_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_no2_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_no2_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_no2_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_no2_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_nonoxnoy_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "nonoxnoy_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_nonoxnoy_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_nonoxnoy_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_nonoxnoy_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_nonoxnoy_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_nonoxnoy_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "nonoxnoy_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_nonoxnoy_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_nonoxnoy_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_nonoxnoy_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_nonoxnoy_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_ozone_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "ozone_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_ozone_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_ozone_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_ozone_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_ozone_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_ozone_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "ozone_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_ozone_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_ozone_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_ozone_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_ozone_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pm10_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pm10_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pm10_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pm10_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pm10_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pm10_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pm10_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pm10_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pm10_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pm10_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pm10_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pm10_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pm25_frm_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pm25_frm_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pm25_frm_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_frm_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pm25_frm_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_frm_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pm25_nonfrm_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pm25_nonfrm_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pm25_nonfrm_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_nonfrm_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pm25_nonfrm_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_nonfrm_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pm25_nonfrm_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pm25_nonfrm_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pm25_nonfrm_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_nonfrm_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pm25_nonfrm_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_nonfrm_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pm25_speciation_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pm25_speciation_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pm25_speciation_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_speciation_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pm25_speciation_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_speciation_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pm25_speciation_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pm25_speciation_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pm25_speciation_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_speciation_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pm25_speciation_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pm25_speciation_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pressure_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pressure_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pressure_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pressure_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pressure_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pressure_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_pressure_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "pressure_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_pressure_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_pressure_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_pressure_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_pressure_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_rh_and_dp_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "rh_and_dp_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_rh_and_dp_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_rh_and_dp_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_rh_and_dp_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_rh_and_dp_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_rh_and_dp_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "rh_and_dp_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_rh_and_dp_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_rh_and_dp_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_rh_and_dp_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_rh_and_dp_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_so2_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "so2_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_so2_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_so2_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_so2_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_so2_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_so2_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "so2_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_so2_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_so2_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_so2_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_so2_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_temperature_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "temperature_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_temperature_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_temperature_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_temperature_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_temperature_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_temperature_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "temperature_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_temperature_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_temperature_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_temperature_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_temperature_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_voc_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "voc_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_voc_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_voc_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_voc_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_voc_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_voc_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "voc_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_voc_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_voc_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_voc_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_voc_hourly_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_wind_daily_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "wind_daily_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_wind_daily_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_wind_daily_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_wind_daily_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_wind_daily_summary.id
}

resource "google_bigquery_table" "epa_historical_air_quality_wind_hourly_summary" {
  project     = var.project_id
  dataset_id  = "epa_historical_air_quality"
  table_id    = "wind_hourly_summary"
  description = "epaspc"
  depends_on = [
    google_bigquery_dataset.epa_historical_air_quality
  ]
}

output "bigquery_table-epa_historical_air_quality_wind_hourly_summary-table_id" {
  value = google_bigquery_table.epa_historical_air_quality_wind_hourly_summary.table_id
}

output "bigquery_table-epa_historical_air_quality_wind_hourly_summary-id" {
  value = google_bigquery_table.epa_historical_air_quality_wind_hourly_summary.id
}
