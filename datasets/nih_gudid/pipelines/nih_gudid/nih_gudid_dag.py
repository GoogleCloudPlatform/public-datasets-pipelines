# Copyright 2022 Google LLC
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
from airflow.operators import bash
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="nih_gudid.nih_gudid",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@weekly",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to download and unzip source files from https://accessgudid.nlm.nih.gov/
    download_unzip_source_zip_file = bash.BashOperator(
        task_id="download_unzip_source_zip_file",
        bash_command="mkdir -p $data_dir/files/\nfilename=$(basename $source_url)\necho Downloading ... $filename\ncurl -o $data_dir/$filename -L $source_url\nunzip -o $data_dir/$filename  -d $data_dir/files/\n",
        env={
            "data_dir": "/home/airflow/gcs/data/nih_gudid",
            "source_url": "https://accessgudid.nlm.nih.gov/release_files/download/AccessGUDID_Delimited_Full_Release_{{ macros.ds_format(ds_nodash, '%Y%m%d', '%Y%m') }}01.zip",
        },
    )

    # Task to load data to a BigQuery table
    load_contacts_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_contacts_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/contacts.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.contacts",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "phone", "type": "string", "mode": "nullable"},
            {"name": "phoneextension", "type": "string", "mode": "nullable"},
            {"name": "email", "type": "string", "mode": "nullable"},
        ],
    )

    # Task to load data to a BigQuery table
    load_device_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_device_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/device.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.device",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "publicdevicerecordkey", "type": "string", "mode": "nullable"},
            {"name": "publicversionstatus", "type": "string", "mode": "nullable"},
            {"name": "devicerecordstatus", "type": "string", "mode": "nullable"},
            {"name": "publicversionnumber", "type": "string", "mode": "nullable"},
            {"name": "publicversiondate", "type": "string", "mode": "nullable"},
            {"name": "devicepublishdate", "type": "string", "mode": "nullable"},
            {
                "name": "devicecommdistributionenddate",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "devicecommdistributionstatus",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "brandname", "type": "string", "mode": "nullable"},
            {"name": "versionmodelnumber", "type": "string", "mode": "nullable"},
            {"name": "catalognumber", "type": "string", "mode": "nullable"},
            {"name": "dunsnumber", "type": "string", "mode": "nullable"},
            {"name": "companyname", "type": "string", "mode": "nullable"},
            {"name": "devicecount", "type": "string", "mode": "nullable"},
            {"name": "devicedescription", "type": "string", "mode": "nullable"},
            {"name": "dmexempt", "type": "string", "mode": "nullable"},
            {"name": "premarketexempt", "type": "string", "mode": "nullable"},
            {"name": "devicehctp", "type": "string", "mode": "nullable"},
            {"name": "devicekit", "type": "string", "mode": "nullable"},
            {"name": "devicecombinationproduct", "type": "string", "mode": "nullable"},
            {"name": "singleuse", "type": "string", "mode": "nullable"},
            {"name": "lotbatch", "type": "string", "mode": "nullable"},
            {"name": "serialnumber", "type": "string", "mode": "nullable"},
            {"name": "manufacturingdate", "type": "string", "mode": "nullable"},
            {"name": "expirationdate", "type": "string", "mode": "nullable"},
            {"name": "donationidnumber", "type": "string", "mode": "nullable"},
            {"name": "labeledcontainsnrl", "type": "string", "mode": "nullable"},
            {"name": "labelednonrl", "type": "string", "mode": "nullable"},
            {"name": "mrisafetystatus", "type": "string", "mode": "nullable"},
            {"name": "rx", "type": "string", "mode": "nullable"},
            {"name": "otc", "type": "string", "mode": "nullable"},
            {"name": "devicesterile", "type": "string", "mode": "nullable"},
            {"name": "sterilizationpriortouse", "type": "string", "mode": "nullable"},
        ],
    )

    # Task to load data to a BigQuery table
    load_device_sizes_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_device_sizes_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/deviceSizes.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.device_sizes",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "sizetype", "type": "string", "mode": "nullable"},
            {"name": "size__unit_", "type": "string", "mode": "nullable"},
            {"name": "size__value_", "type": "string", "mode": "nullable"},
            {"name": "sizetext", "type": "string", "mode": "nullable"},
        ],
    )

    # Task to load data to a BigQuery table
    load_environmental_conditions_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_environmental_conditions_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/environmentalConditions.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.environmental_conditions",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "storagehandlingtype", "type": "string", "mode": "nullable"},
            {
                "name": "storagehandlinghigh__unit_",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "storagehandlinghigh__value_",
                "type": "string",
                "mode": "nullable",
            },
            {"name": "storagehandlinglow__unit_", "type": "string", "mode": "nullable"},
            {
                "name": "storagehandlinglow__value_",
                "type": "string",
                "mode": "nullable",
            },
            {
                "name": "storagehandlingspecialconditiontext",
                "type": "string",
                "mode": "nullable",
            },
        ],
    )

    # Task to load data to a BigQuery table
    load_gmdn_terms_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_gmdn_terms_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/gmdnTerms.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.gmdn_terms",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "gmdnptname", "type": "string", "mode": "nullable"},
            {"name": "gmdnptdefinition", "type": "string", "mode": "nullable"},
        ],
    )

    # Task to load data to a BigQuery table
    load_identifiers_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_identifiers_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/identifiers.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.identifiers",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "deviceid", "type": "string", "mode": "nullable"},
            {"name": "deviceidtype", "type": "string", "mode": "nullable"},
            {"name": "deviceidissuingagency", "type": "string", "mode": "nullable"},
            {"name": "containsdinumber", "type": "string", "mode": "nullable"},
            {"name": "pkgquantity", "type": "string", "mode": "nullable"},
            {"name": "pkgdiscontinuedate", "type": "string", "mode": "nullable"},
            {"name": "pkgstatus", "type": "string", "mode": "nullable"},
            {"name": "pkgtype", "type": "string", "mode": "nullable"},
        ],
    )

    # Task to load data to a BigQuery table
    load_premarket_submissions_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_premarket_submissions_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/premarketSubmissions.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.premarket_submissions",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "submissionnumber", "type": "string", "mode": "nullable"},
            {"name": "supplementnumber", "type": "string", "mode": "nullable"},
        ],
    )

    # Task to load data to a BigQuery table
    load_product_codes_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_product_codes_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/productCodes.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.product_codes",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "productcode", "type": "string", "mode": "nullable"},
            {"name": "productcodename", "type": "string", "mode": "nullable"},
        ],
    )

    # Task to load data to a BigQuery table
    load_sterilization_method_types_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_sterilization_method_types_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=["data/nih_gudid/files/sterilizationMethodTypes.txt"],
        source_format="CSV",
        destination_project_dataset_table="nih_gudid.sterilization_method_types",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        field_delimiter="|",
        schema_fields=[
            {"name": "primarydi", "type": "string", "mode": "nullable"},
            {"name": "sterilizationmethod", "type": "string", "mode": "nullable"},
        ],
    )

    download_unzip_source_zip_file >> [
        load_contacts_to_bq,
        load_device_to_bq,
        load_device_sizes_to_bq,
        load_environmental_conditions_to_bq,
        load_gmdn_terms_to_bq,
        load_identifiers_to_bq,
        load_premarket_submissions_to_bq,
        load_product_codes_to_bq,
        load_sterilization_method_types_to_bq,
    ]
