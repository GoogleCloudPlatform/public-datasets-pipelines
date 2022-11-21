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


resource "google_bigquery_dataset" "fec" {
  dataset_id  = "fec"
  project     = var.project_id
  description = "The FEC dataset contains committee, candidate and campaign finance data for the current election cycle and for election cycles through 1980.\nSpecifically the data set contains the following data points:\nCommittees(CM Data Dictionary): The committee tables contains one record for each committee registered with the Federal Election Commission. This includes federal political action committees and party committees, campaign committees for presidential, house and senate candidates, as well as groups or organizations who are spending money for or against candidates for federal office.\nCandidates(CN  Data Dictionary): The candidate tables contains one record for each candidate who has either registered with the Federal Election Commission or appeared on a ballot list prepared by a state elections office.\nCandidate-Committee Linkages(CCL Data Dictionary): These tables contains one record for each candidate to committee linkage.\nItemized Records (Any Transaction from One Committee to Another)(OTH Data Dictionary): The itemized records (miscellaneous transactions) tables contains all transactions (contributions, transfers, etc. among federal committees). Contributions to Candidates(PAS2 Data Dictionary) : These tables are a subset of the Itemized Records (OTH) tables. The itemized committee contributions file contains each contribution or independent expenditure made by a PAC, party committee, candidate committee, or other federal committee to a candidate during the two-year election cycle.\nIndividual Contributions(INDIV Data Dictionary) : The individual contributions file contains each contribution from an individual to a federal committee.\nOperating Expenditures(OPPEXP Data Dictionary) : The Operating Expenditures file contains disbursements reported on FEC Form 3 Line 17, FEC Form 3P Line 23and FEC Form 3X Lines 21(a)(i), 21(a)(ii) and 21(b)"
}

output "bigquery_dataset-fec-dataset_id" {
  value = google_bigquery_dataset.fec.dataset_id
}

resource "google_storage_bucket" "fec" {
  name                        = "${var.bucket_name_prefix}-fec"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

output "storage_bucket-fec-name" {
  value = google_storage_bucket.fec.name
}
