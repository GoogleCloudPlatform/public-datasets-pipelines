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


resource "google_bigquery_table" "covid19_vaccination_search_insights_covid19_vaccination_search_insights" {
  project    = var.project_id
  dataset_id = "covid19_vaccination_search_insights"
  table_id   = "covid19_vaccination_search_insights"

  description = "Terms of use\nTo download or use the data, you must agree to the Google Terms of Service: https://policies.google.com/terms\n\nDescription\nThe COVID-19 Vaccination Search Insights data shows aggregated, anonymized trends in searches related to COVID-19 vaccination. The dataset provides a weekly time series for each region showing the relative interest of Google searches related to COVID-19 vaccination, across several categories.\n\nThe data is intended to help public health officials design, target, and evaluate public education campaigns.\n\nTo explore and download the data, use our interactive dashboard: http://goo.gle/covid19vaccinationinsights\n\nTo learn more about the dataset, how we generate it and preserve privacy, read the data documentation:\nhttps://storage.googleapis.com/gcs-public-datasets/COVID-19%20Vaccination%20Search%20Insights%20documentation.pdf"
  time_partitioning {
    type = "DAY"

    require_partition_filter = false
  }
  clustering = ["sub_region_1_code", "sub_region_2_code", "sub_region_3_code", "place_id"]

  schema = <<EOF
    [
  {
      "name": "date",
      "description": "The first day of the week (starting on Monday) on which the searches took place. For example, in the weekly data the row labeled 2021-04-19 represents the search activity for the week of April 19 to April 25, 2021, inclusive. Calendar days start and end at midnight Pacific Standard Time.",
      "type": "DATE",
      "mode": "NULLABLE"
  },
  {
      "name": "country_region",
      "description": "The name of the country in English. For example, United States.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "country_region_code",
      "description": "The ISO 3166-1 code for the country. For example, US.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "sub_region_1",
      "description": "The name of a region in the country. For example, California.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "sub_region_1_code",
      "description": "A country-specific ISO 3166-2 code for the region. For example, US-CA.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "sub_region_2",
      "description": "The name (or type) of a region in the country. Typically a subdivision of sub_region_1. For example, Santa Clara County or municipal_borough.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "sub_region_2_code",
      "description": "In the US, the FIPS code for a US county (or equivalent). For example, 06085.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "sub_region_3",
      "description": "The name (or type) of a region in the country. Typically a subdivision of sub_region_2. For example, Downtown or postal_code.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "sub_region_3_code",
      "description": "In the US, the ZIP code. For example 94303.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "place_id",
      "description": "The Google place ID for the most-specific subregion. Used in the Google Places API and on Google Maps. For example, ChIJd_Y0eVIvkIARuQyDN0F1LBA.",
      "type": "STRING",
      "mode": "NULLABLE"
  },
  {
      "name": "sni_covid19_vaccination",
      "description": "The scaled normalized interest related to all COVID-19 vaccination for the region and date. For example, 87.02. Empty when data isn't available.",
      "type": "FLOAT",
      "mode": "NULLABLE"
  },
  {
      "name": "sni_vaccination_intent",
      "description": "The scaled normalized interest related to vaccination intent for the region and date. For example, 22.69. Empty when data isn't available.",
      "type": "FLOAT",
      "mode": "NULLABLE"
  },
  {
      "name": "sni_safety_side_effects",
      "description": "The scaled normalized interest related to safety and side effects of the vaccines for the region and date. For example, 17.96. Empty when data isn't available.",
      "type": "FLOAT",
      "mode": "NULLABLE"
  }
]
    EOF
  depends_on = [
    google_bigquery_dataset.covid19_vaccination_search_insights
  ]
}

output "bigquery_table-covid19_vaccination_search_insights_covid19_vaccination_search_insights-table_id" {
  value = google_bigquery_table.covid19_vaccination_search_insights_covid19_vaccination_search_insights.table_id
}

output "bigquery_table-covid19_vaccination_search_insights_covid19_vaccination_search_insights-id" {
  value = google_bigquery_table.covid19_vaccination_search_insights_covid19_vaccination_search_insights.id
}
