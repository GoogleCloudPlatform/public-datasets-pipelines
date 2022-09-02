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


resource "google_bigquery_dataset" "ebi_chembl" {
  dataset_id  = "ebi_chembl"
  project     = var.project_id
  description = "ChEMBL Data is a manually curated database of small molecules used in drug discovery, including information about existing patented drugs.\n\nDocumentation: https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/schema_documentation.html\n\n\u201cChEMBL\u201d by the European Bioinformatics Institute (EMBL-EBI), used under CC BY-SA 3.0. Modifications have been made to add normalized publication numbers.\n"
}

output "bigquery_dataset-ebi_chembl-dataset_id" {
  value = google_bigquery_dataset.ebi_chembl.dataset_id
}
