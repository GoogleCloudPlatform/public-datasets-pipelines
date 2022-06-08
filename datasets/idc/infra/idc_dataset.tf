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


resource "google_storage_bucket" "idc" {
  name                        = "${var.bucket_name_prefix}-idc"
  force_destroy               = true
  location                    = "US"
  uniform_bucket_level_access = true
  lifecycle {
    ignore_changes = [
      logging,
    ]
  }
}

data "google_iam_policy" "storage_bucket__idc" {
  dynamic "binding" {
    for_each = var.iam_policies["storage_buckets"]["idc"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_storage_bucket_iam_policy" "idc" {
  bucket      = google_storage_bucket.idc.name
  policy_data = data.google_iam_policy.storage_bucket__idc.policy_data
}
output "storage_bucket-idc-name" {
  value = google_storage_bucket.idc.name
}

resource "google_bigquery_dataset" "idc_v1" {
  dataset_id  = "idc_v1"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v1 data"
}

data "google_iam_policy" "bq_ds__idc_v1" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v1"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v1" {
  dataset_id  = google_bigquery_dataset.idc_v1.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v1.policy_data
}
output "bigquery_dataset-idc_v1-dataset_id" {
  value = google_bigquery_dataset.idc_v1.dataset_id
}

resource "google_bigquery_dataset" "idc_v2" {
  dataset_id  = "idc_v2"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v2 data"
}

data "google_iam_policy" "bq_ds__idc_v2" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v2"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v2" {
  dataset_id  = google_bigquery_dataset.idc_v2.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v2.policy_data
}
output "bigquery_dataset-idc_v2-dataset_id" {
  value = google_bigquery_dataset.idc_v2.dataset_id
}

resource "google_bigquery_dataset" "idc_v3" {
  dataset_id  = "idc_v3"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v3 data"
}

data "google_iam_policy" "bq_ds__idc_v3" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v3"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v3" {
  dataset_id  = google_bigquery_dataset.idc_v3.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v3.policy_data
}
output "bigquery_dataset-idc_v3-dataset_id" {
  value = google_bigquery_dataset.idc_v3.dataset_id
}

resource "google_bigquery_dataset" "idc_v4" {
  dataset_id  = "idc_v4"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v4 data"
}

data "google_iam_policy" "bq_ds__idc_v4" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v4"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v4" {
  dataset_id  = google_bigquery_dataset.idc_v4.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v4.policy_data
}
output "bigquery_dataset-idc_v4-dataset_id" {
  value = google_bigquery_dataset.idc_v4.dataset_id
}

resource "google_bigquery_dataset" "idc_v5" {
  dataset_id  = "idc_v5"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v5 data"
}

data "google_iam_policy" "bq_ds__idc_v5" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v5"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v5" {
  dataset_id  = google_bigquery_dataset.idc_v5.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v5.policy_data
}
output "bigquery_dataset-idc_v5-dataset_id" {
  value = google_bigquery_dataset.idc_v5.dataset_id
}

resource "google_bigquery_dataset" "idc_v6" {
  dataset_id  = "idc_v6"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v6 data"
}

data "google_iam_policy" "bq_ds__idc_v6" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v6"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v6" {
  dataset_id  = google_bigquery_dataset.idc_v6.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v6.policy_data
}
output "bigquery_dataset-idc_v6-dataset_id" {
  value = google_bigquery_dataset.idc_v6.dataset_id
}

resource "google_bigquery_dataset" "idc_v7" {
  dataset_id  = "idc_v7"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v7 data"
}

data "google_iam_policy" "bq_ds__idc_v7" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v7"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v7" {
  dataset_id  = google_bigquery_dataset.idc_v7.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v7.policy_data
}
output "bigquery_dataset-idc_v7-dataset_id" {
  value = google_bigquery_dataset.idc_v7.dataset_id
}

resource "google_bigquery_dataset" "idc_v8" {
  dataset_id  = "idc_v8"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v8 data"
}

data "google_iam_policy" "bq_ds__idc_v8" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v8"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v8" {
  dataset_id  = google_bigquery_dataset.idc_v8.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v8.policy_data
}
output "bigquery_dataset-idc_v8-dataset_id" {
  value = google_bigquery_dataset.idc_v8.dataset_id
}

resource "google_bigquery_dataset" "idc_v9" {
  dataset_id  = "idc_v9"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) v9 data"
}

data "google_iam_policy" "bq_ds__idc_v9" {
  dynamic "binding" {
    for_each = var.iam_policies["bigquery_datasets"]["idc_v9"]
    content {
      role    = binding.value["role"]
      members = binding.value["members"]
    }
  }
}

resource "google_bigquery_dataset_iam_policy" "idc_v9" {
  dataset_id  = google_bigquery_dataset.idc_v9.dataset_id
  policy_data = data.google_iam_policy.bq_ds__idc_v9.policy_data
}
output "bigquery_dataset-idc_v9-dataset_id" {
  value = google_bigquery_dataset.idc_v9.dataset_id
}

resource "google_bigquery_dataset" "idc_current" {
  dataset_id  = "idc_current"
  project     = var.project_id
  description = "Imaging Data Commons (IDC) - The Cancer Imaging Archive (TCIA) current data"
}

output "bigquery_dataset-idc_current-dataset_id" {
  value = google_bigquery_dataset.idc_current.dataset_id
}
