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


resource "google_bigquery_table" "nasa_wildfire_past_week" {
  project    = var.project_id
  dataset_id = "nasa_wildfire"
  table_id   = "past_week"

  description = "Past Week table"



  schema = <<EOF
    [
  {
    "name": "latitude",
    "type": "FLOAT",
    "description": "Center of nominal 375 m fire pixel",
    "mode": "NULLABLE"
  },
  {
    "name": "longitude",
    "type": "FLOAT",
    "description": "Center of nominal 375 m fire pixel",
    "mode": "NULLABLE"
  },
  {
    "name": "bright_ti4",
    "type": "FLOAT",
    "description": "Brightness temperature I-4: VIIRS I-4 channel brightness temperature of the fire pixel measured in Kelvin.",
    "mode": "NULLABLE"
  },
  {
    "name": "scan",
    "type": "FLOAT",
    "description": "The algorithm produces approximately 375 m pixels at nadir. Scan and track reflect actual pixel size.",
    "mode": "NULLABLE"
  },
  {
    "name": "track",
    "type": "FLOAT",
    "description": "The algorithm produces approximately 375 m pixels at nadir. Scan and track reflect actual pixel size.",
    "mode": "NULLABLE"
  },
  {
    "name": "acq_date",
    "type": "DATE",
    "description": "Date of VIIRS acquisition.",
    "mode": "NULLABLE"
  },
  {
    "name": "acq_time",
    "type": "TIME",
    "description": "Time of acquisition/overpass of the satellite (in UTC).",
    "mode": "NULLABLE"
  },
  {
    "name": "satellite",
    "type": "STRING",
    "description": "N= Suomi National Polar-orbiting Partnership (Suomi-NPP)",
    "mode": "NULLABLE"
  },
  {
    "name": "confidence",
    "type": "STRING",
    "description": "This value is based on a collection of intermediate algorithm quantities used in the detection process. It is intended to help users gauge the quality of individual hotspot/fire pixels. Confidence values are set to low nominal and high. Low confidence daytime fire pixels are typically associated with areas of sun glint and lower relative temperature anomaly (<15K) in the mid-infrared channel I4. Nominal confidence pixels are those free of potential sun glint contamination during the day and marked by strong (>15K) temperature anomaly in either day or nighttime data. High confidence fire pixels are associated with day or nighttime saturated pixels.",
    "mode": "NULLABLE"
  },
  {
    "name": "version",
    "type": "STRING",
    "description": "Version identifies the collection (e.g. VIIRS Collection 1) and source of data processing: Near Real-Time (NRT suffix added to collection) or Standard Processing (collection only). 1.0NRT - Collection 1 NRT processing. 1.0 - Collection 1 Standard processing",
    "mode": "nullable"
  },
  {
    "name": "bright_ti5",
    "type": "FLOAT",
    "description": "Brightness temperature I-5: I-5 Channel brightness temperature of the fire pixel measured in Kelvin.",
    "mode": "NULLABLE"
  },
  {
    "name": "frp",
    "type": "FLOAT",
    "description": "Fire Radiative Power: FRP depicts the pixel-integrated fire radiative power in MW (megawatts). FRP depicts the pixel-integrated fire radiative power in MW (megawatts). Given the unique spatial and spectral resolution of the data the VIIRS 375 m fire detection algorithm was customized and tuned in order to optimize its response over small fires while balancing the occurrence of false alarms. Frequent saturation of the mid-infrared I4 channel (3.55-3.93 µm) driving the detection of active fires requires additional tests and procedures to avoid pixel classification errors. As a result sub-pixel fire characterization (e.g. fire radiative power [FRP] retrieval) is only viable across small and/or low-intensity fires. Systematic FRP retrievals are based on a hybrid approach combining 375 and 750 m data. In fact starting in 2015 the algorithm incorporated additional VIIRS channel M13 (3.973-4.128 µm) 750 m data in both aggregated and unaggregated format.",
    "mode": "NULLABLE"
  },
  {
    "name": "daynight",
    "type": "STRING",
    "description": "D= Daytime fire N= Nighttime fire",
    "mode": "NULLABLE"
  },
  {
    "name": "acquisition_timestamp",
    "type": "TIMESTAMP",
    "mode": "NULLABLE"
  }
]
    EOF
  depends_on = [
    google_bigquery_dataset.nasa_wildfire
  ]
}

output "bigquery_table-nasa_wildfire_past_week-table_id" {
  value = google_bigquery_table.nasa_wildfire_past_week.table_id
}

output "bigquery_table-nasa_wildfire_past_week-id" {
  value = google_bigquery_table.nasa_wildfire_past_week.id
}
