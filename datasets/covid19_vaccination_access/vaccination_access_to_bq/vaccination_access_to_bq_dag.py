# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from airflow import DAG
from airflow.contrib.operators import gcs_to_bq

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-05-01",
}


with DAG(
    dag_id="covid19_vaccination_access.vaccination_access_to_bq",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to load CSV file from covid19-open-data bucket to facility_boundary_us_all
    gcs_to_bq_table_us_all = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bq_table_us_all",
        bucket="{{ var.json.covid19_vaccination_access.source_bucket }}",
        source_objects=[
            "{{ var.json.covid19_vaccination_access.source_prefix }}/facility-boundary-us-all.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_vaccination_access.facility_boundary_us_all",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "facility_place_id",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The Google Place ID of the vaccination site. For example, ChIJV3woGFkSK4cRWP9s3-kIFGk.",
            },
            {
                "name": "facility_provider_id",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "An identifier imported from the provider of the vaccination site information. In the US, we use the ID provided by VaccineFinder when available. For example, 7ede5bd5-44da-4a59-b4d9-b3a49c53472c.",
            },
            {
                "name": "facility_name",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of the vaccination site. For example, St. Joseph's Hospital.",
            },
            {
                "name": "facility_latitude",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "The latitude of the vaccination site. For example, 36.0507",
            },
            {
                "name": "facility_longitude",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "The longitude of the vaccination site. For example, 41.4356",
            },
            {
                "name": "facility_country_region",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of the country or region in English. For example, United States.",
            },
            {
                "name": "facility_country_region_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The ISO 3166-1 code for the country or region. For example, US.",
            },
            {
                "name": "facility_sub_region_1",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of a region in the country. For example, California.",
            },
            {
                "name": "facility_sub_region_1_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "A country-specific ISO 3166-2 code for the region. For example, US-CA.",
            },
            {
                "name": "facility_sub_region_2",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name (or type) of a region in the country. Typically a subdivision of sub_region_1. For example, Santa Clara County or municipal_borough.",
            },
            {
                "name": "facility_sub_region_2_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "In the US, the FIPS code for a US county (or equivalent). For example, 06085.",
            },
            {
                "name": "facility_region_place_id",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The Google place ID for the most-specific region, used in Google Places API and on Google Maps. For example, ChIJd_Y0eVIvkIARuQyDN0F1LBA.",
            },
            {
                "name": "mode_of_transportation",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The mode of transport used to calculate the catchment boundary. For example, driving.",
            },
            {
                "name": "travel_time_threshold_minutes",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "The maximum travel time, in minutes, used to calculate the catchment boundary. For example, 30.",
            },
            {
                "name": "facility_catchment_boundary",
                "type": "GEOGRAPHY",
                "mode": "NULLABLE",
                "description": "A GeoJSON representation of the catchment area boundary of the site, for a particular mode of transportation and travel time threshold. Consists of multiple latitude and longitude points.",
            },
        ],
    )

    # Task to load CSV file from covid19-open-data bucket to facility_boundary_us_drive
    gcs_to_bq_table_us_drive = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bq_table_us_drive",
        bucket="{{ var.json.covid19_vaccination_access.source_bucket }}",
        source_objects=[
            "{{ var.json.covid19_vaccination_access.source_prefix }}/facility-boundary-us-drive.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_vaccination_access.facility_boundary_us_drive",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "facility_place_id",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The Google Place ID of the vaccination site. For example, ChIJV3woGFkSK4cRWP9s3-kIFGk.",
            },
            {
                "name": "facility_provider_id",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "An identifier imported from the provider of the vaccination site information. In the US, we use the ID provided by VaccineFinder when available. For example, 7ede5bd5-44da-4a59-b4d9-b3a49c53472c.",
            },
            {
                "name": "facility_name",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of the vaccination site. For example, St. Joseph's Hospital.",
            },
            {
                "name": "facility_latitude",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "The latitude of the vaccination site. For example, 36.0507",
            },
            {
                "name": "facility_longitude",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "The longitude of the vaccination site. For example, 41.4356",
            },
            {
                "name": "facility_country_region",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of the country or region in English. For example, United States.",
            },
            {
                "name": "facility_country_region_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The ISO 3166-1 code for the country or region. For example, US.",
            },
            {
                "name": "facility_sub_region_1",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of a region in the country. For example, California.",
            },
            {
                "name": "facility_sub_region_1_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "A country-specific ISO 3166-2 code for the region. For example, US-CA.",
            },
            {
                "name": "facility_sub_region_2",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name (or type) of a region in the country. Typically a subdivision of sub_region_1. For example, Santa Clara County or municipal_borough.",
            },
            {
                "name": "facility_sub_region_2_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "In the US, the FIPS code for a US county (or equivalent). For example, 06085.",
            },
            {
                "name": "facility_region_place_id",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The Google place ID for the most-specific region, used in Google Places API and on Google Maps. For example, ChIJd_Y0eVIvkIARuQyDN0F1LBA.",
            },
            {
                "name": "mode_of_transportation",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The mode of transport used to calculate the catchment boundary. For example, driving.",
            },
            {
                "name": "travel_time_threshold_minutes",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "The maximum travel time, in minutes, used to calculate the catchment boundary. For example, 30.",
            },
            {
                "name": "facility_catchment_boundary",
                "type": "GEOGRAPHY",
                "mode": "NULLABLE",
                "description": "A GeoJSON representation of the catchment area boundary of the site, for a particular mode of transportation and travel time threshold. Consists of multiple latitude and longitude points.",
            },
        ],
    )

    # Task to load CSV file from covid19-open-data bucket to facility_boundary_us_transit
    gcs_to_bq_table_us_transit = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bq_table_us_transit",
        bucket="{{ var.json.covid19_vaccination_access.source_bucket }}",
        source_objects=[
            "{{ var.json.covid19_vaccination_access.source_prefix }}/facility-boundary-us-transit.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_vaccination_access.facility_boundary_us_transit",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "facility_place_id",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The Google Place ID of the vaccination site. For example, ChIJV3woGFkSK4cRWP9s3-kIFGk.",
            },
            {
                "name": "facility_provider_id",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "An identifier imported from the provider of the vaccination site information. In the US, we use the ID provided by VaccineFinder when available. For example, 7ede5bd5-44da-4a59-b4d9-b3a49c53472c.",
            },
            {
                "name": "facility_name",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of the vaccination site. For example, St. Joseph's Hospital.",
            },
            {
                "name": "facility_latitude",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "The latitude of the vaccination site. For example, 36.0507",
            },
            {
                "name": "facility_longitude",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "The longitude of the vaccination site. For example, 41.4356",
            },
            {
                "name": "facility_country_region",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of the country or region in English. For example, United States.",
            },
            {
                "name": "facility_country_region_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The ISO 3166-1 code for the country or region. For example, US.",
            },
            {
                "name": "facility_sub_region_1",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of a region in the country. For example, California.",
            },
            {
                "name": "facility_sub_region_1_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "A country-specific ISO 3166-2 code for the region. For example, US-CA.",
            },
            {
                "name": "facility_sub_region_2",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name (or type) of a region in the country. Typically a subdivision of sub_region_1. For example, Santa Clara County or municipal_borough.",
            },
            {
                "name": "facility_sub_region_2_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "In the US, the FIPS code for a US county (or equivalent). For example, 06085.",
            },
            {
                "name": "facility_region_place_id",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The Google place ID for the most-specific region, used in Google Places API and on Google Maps. For example, ChIJd_Y0eVIvkIARuQyDN0F1LBA.",
            },
            {
                "name": "mode_of_transportation",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The mode of transport used to calculate the catchment boundary. For example, driving.",
            },
            {
                "name": "travel_time_threshold_minutes",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "The maximum travel time, in minutes, used to calculate the catchment boundary. For example, 30.",
            },
            {
                "name": "facility_catchment_boundary",
                "type": "GEOGRAPHY",
                "mode": "NULLABLE",
                "description": "A GeoJSON representation of the catchment area boundary of the site, for a particular mode of transportation and travel time threshold. Consists of multiple latitude and longitude points.",
            },
        ],
    )

    # Task to load CSV file from covid19-open-data bucket to facility_boundary_us_walk
    gcs_to_bq_table_us_walk = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bq_table_us_walk",
        bucket="{{ var.json.covid19_vaccination_access.source_bucket }}",
        source_objects=[
            "{{ var.json.covid19_vaccination_access.source_prefix }}/facility-boundary-us-walk.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_vaccination_access.facility_boundary_us_walk",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "facility_place_id",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "The Google Place ID of the vaccination site. For example, ChIJV3woGFkSK4cRWP9s3-kIFGk.",
            },
            {
                "name": "facility_provider_id",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "An identifier imported from the provider of the vaccination site information. In the US, we use the ID provided by VaccineFinder when available. For example, 7ede5bd5-44da-4a59-b4d9-b3a49c53472c.",
            },
            {
                "name": "facility_name",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of the vaccination site. For example, St. Joseph's Hospital.",
            },
            {
                "name": "facility_latitude",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "The latitude of the vaccination site. For example, 36.0507",
            },
            {
                "name": "facility_longitude",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "The longitude of the vaccination site. For example, 41.4356",
            },
            {
                "name": "facility_country_region",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of the country or region in English. For example, United States.",
            },
            {
                "name": "facility_country_region_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The ISO 3166-1 code for the country or region. For example, US.",
            },
            {
                "name": "facility_sub_region_1",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name of a region in the country. For example, California.",
            },
            {
                "name": "facility_sub_region_1_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "A country-specific ISO 3166-2 code for the region. For example, US-CA.",
            },
            {
                "name": "facility_sub_region_2",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The name (or type) of a region in the country. Typically a subdivision of sub_region_1. For example, Santa Clara County or municipal_borough.",
            },
            {
                "name": "facility_sub_region_2_code",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "In the US, the FIPS code for a US county (or equivalent). For example, 06085.",
            },
            {
                "name": "facility_region_place_id",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The Google place ID for the most-specific region, used in Google Places API and on Google Maps. For example, ChIJd_Y0eVIvkIARuQyDN0F1LBA.",
            },
            {
                "name": "mode_of_transportation",
                "type": "STRING",
                "mode": "NULLABLE",
                "description": "The mode of transport used to calculate the catchment boundary. For example, driving.",
            },
            {
                "name": "travel_time_threshold_minutes",
                "type": "INTEGER",
                "mode": "NULLABLE",
                "description": "The maximum travel time, in minutes, used to calculate the catchment boundary. For example, 30.",
            },
            {
                "name": "facility_catchment_boundary",
                "type": "GEOGRAPHY",
                "mode": "NULLABLE",
                "description": "A GeoJSON representation of the catchment area boundary of the site, for a particular mode of transportation and travel time threshold. Consists of multiple latitude and longitude points.",
            },
        ],
    )

    gcs_to_bq_table_us_all
    gcs_to_bq_table_us_drive
    gcs_to_bq_table_us_transit
    gcs_to_bq_table_us_walk
