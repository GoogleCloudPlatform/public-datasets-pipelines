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


resource "google_bigquery_table" "_cloud_datasets_tabular_datasets" {
  project     = var.project_id
  dataset_id  = "_cloud_datasets"
  table_id    = "tabular_datasets"
  description = "This table contains all the metadata for all the tabular datasets in the Cloud Datasets program"
  schema      = <<EOF
    [
  {
      "name": "extracted_at",
      "description": "The date and time when this row was extracted from BigQuery",
      "type": "TIMESTAMP"
  },
  {
      "name": "created_at",
      "description": "The date and time when the dataset was created",
      "type": "TIMESTAMP"
  },
  {
      "name": "modified_at",
      "description": "The date and time when the dataset was last modified",
      "type": "TIMESTAMP"
  },
  {
      "name": "project_id",
      "description": "The GCP project where the public dataset is stored",
      "type": "STRING"
  },
  {
      "name": "dataset_id",
      "description": "The BigQuery dataset ID",
      "type": "STRING"
  },
  {
      "name": "description",
      "description": "The dataset description",
      "type": "STRING"
  },
  {
      "name": "num_tables",
      "description": "Number of tables contained in this dataset",
      "type": "INTEGER"
  }
]
    EOF
  depends_on = [
    google_bigquery_dataset._cloud_datasets
  ]
}

output "bigquery_table-_cloud_datasets_tabular_datasets-table_id" {
  value = google_bigquery_table._cloud_datasets_tabular_datasets.table_id
}

output "bigquery_table-_cloud_datasets_tabular_datasets-id" {
  value = google_bigquery_table._cloud_datasets_tabular_datasets.id
}

resource "google_bigquery_table" "_cloud_datasets_tables" {
  project     = var.project_id
  dataset_id  = "_cloud_datasets"
  table_id    = "tables"
  description = "This table contains all the metadata for all the tables in the Cloud Datasets program"
  schema      = <<EOF
    [
  {
      "name": "extracted_at",
      "description": "The date and time when this row was extracted from BigQuery",
      "type": "TIMESTAMP"
  },
  {
      "name": "created_at",
      "description": "The date and time when the dataset was created",
      "type": "TIMESTAMP"
  },
  {
      "name": "modified_at",
      "description": "The date and time when the dataset was last modified",
      "type": "TIMESTAMP"
  },
  {
      "name": "project_id",
      "description": "The GCP project where the public dataset is stored",
      "type": "STRING"
  },
  {
      "name": "dataset_id",
      "description": "The BigQuery dataset ID",
      "type": "STRING"
  },
  {
      "name": "table_id",
      "description": "The BigQuery table ID",
      "type": "STRING"
  },
  {
      "name": "description",
      "description": "The dataset description",
      "type": "STRING"
  },
  {
      "name": "type",
      "description": "The type of the table",
      "type": "STRING"
  },
  {
      "name": "num_bytes",
      "description": "The number of bytes the table allocated on disk",
      "type": "INTEGER"
  },
  {
      "name": "num_rows",
      "description": "The number of rows in the table",
      "type": "INTEGER"
  },
  {
      "name": "num_columns",
      "description": "The number of columns in the table",
      "type": "INTEGER"
  },
  {
      "name": "described_columns",
      "description": "The number of columns in the table with a description",
      "type": "INTEGER"
  }
]
    EOF
  depends_on = [
    google_bigquery_dataset._cloud_datasets
  ]
}

output "bigquery_table-_cloud_datasets_tables-table_id" {
  value = google_bigquery_table._cloud_datasets_tables.table_id
}

output "bigquery_table-_cloud_datasets_tables-id" {
  value = google_bigquery_table._cloud_datasets_tables.id
}

resource "google_bigquery_table" "_cloud_datasets_tables_fields" {
  project     = var.project_id
  dataset_id  = "_cloud_datasets"
  table_id    = "tables_fields"
  description = "This table contains all the metadata for all the field in all the tables in the Cloud Datasets program"
  schema      = <<EOF
    [
  {
      "name": "extracted_at",
      "description": "The date and time when this row was extracted from BigQuery",
      "type": "TIMESTAMP"
  },
  {
      "name": "project_id",
      "description": "The GCP project where the public dataset is stored",
      "type": "STRING"
  },
  {
      "name": "dataset_id",
      "description": "The BigQuery dataset ID",
      "type": "STRING"
  },
  {
      "name": "table_id",
      "description": "The BigQuery table ID",
      "type": "STRING"
  },
  {
      "name": "name",
      "description": "The name of the field",
      "type": "STRING"
  },
  {
      "name": "description",
      "description": "The description for the field",
      "type": "STRING"
  },
  {
      "name": "field_type",
      "description": "The type of the field",
      "type": "STRING"
  },
  {
      "name": "mode",
      "description": "The mode of the field",
      "type": "STRING"
  },
  {
      "name": "precision",
      "description": "Precision for the NUMERIC field",
      "type": "INTEGER"
  },
  {
      "name": "scale",
      "description": "Scale for the NUMERIC field",
      "type": "INTEGER"
  },
  {
      "name": "max_length",
      "description": "Maximum length for the STRING or BYTES field",
      "type": "INTEGER"
  }
]
    EOF
  depends_on = [
    google_bigquery_dataset._cloud_datasets
  ]
}

output "bigquery_table-_cloud_datasets_tables_fields-table_id" {
  value = google_bigquery_table._cloud_datasets_tables_fields.table_id
}

output "bigquery_table-_cloud_datasets_tables_fields-id" {
  value = google_bigquery_table._cloud_datasets_tables_fields.id
}
