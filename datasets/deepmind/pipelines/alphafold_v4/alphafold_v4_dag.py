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
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.operators import cloud_storage_transfer_service
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2022-10-01",
}


with DAG(
    dag_id="deepmind.alphafold_v4",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Copy v4 JSON metadata, accession IDs, and FASTA to public bucket
    copy_json_metadata_accession_and_fasta_to_public_bucket = cloud_storage_transfer_service.CloudDataTransferServiceGCSToGCSOperator(
        task_id="copy_json_metadata_accession_and_fasta_to_public_bucket",
        timeout=43200,
        retries=0,
        wait=True,
        project_id="bigquery-public-data",
        source_bucket="{{ var.json.deepmind.alphafold.source_bucket }}",
        destination_bucket="{{ var.json.deepmind.alphafold.destination_bucket_v4 }}",
        object_conditions={
            "includePrefixes": ["metadata", "accession_ids.csv", "sequences.fasta"]
        },
        transfer_options={
            "overwriteWhen": "DIFFERENT",
            "deleteObjectsUniqueInSink": True,
        },
    )

    # Copy proteomes to public bucket
    copy_proteomes_to_public_bucket = cloud_storage_transfer_service.CloudDataTransferServiceGCSToGCSOperator(
        task_id="copy_proteomes_to_public_bucket",
        timeout=43200,
        retries=0,
        wait=True,
        project_id="bigquery-public-data",
        source_bucket="{{ var.json.deepmind.alphafold.source_bucket }}",
        destination_bucket="{{ var.json.deepmind.alphafold.destination_bucket_v4 }}",
        object_conditions={"includePrefixes": ["proteomes"]},
        transfer_options={
            "overwriteWhen": "DIFFERENT",
            "deleteObjectsUniqueInSink": True,
        },
    )

    # Download accession_ids.csv to Composer bucket
    download_accession_ids_to_composer_bucket = (
        cloud_storage_transfer_service.CloudDataTransferServiceGCSToGCSOperator(
            task_id="download_accession_ids_to_composer_bucket",
            timeout=43200,
            retries=0,
            wait=True,
            project_id="bigquery-public-data",
            source_bucket="{{ var.json.deepmind.alphafold.source_bucket }}",
            destination_bucket="{{ var.value.composer_bucket }}",
            destination_path="data/deepmind/alphafold/v4",
            object_conditions={"includePrefixes": ["accession_ids.csv"]},
            transfer_options={"overwriteWhen": "DIFFERENT"},
        )
    )

    # Download accession_ids.csv, then split it into multiple manifest files
    generate_manifests = bash.BashOperator(
        task_id="generate_manifests",
        bash_command="set -e\nmkdir -p $WORKING_DIR\ncut -d , -f 4 $WORKING_DIR/accession_ids.csv \u003e $WORKING_DIR/accession_ids_trimmed.csv\nsplit --numeric-suffixes=1 -a 3 -l $OBJECTS_PER_MANIFEST $WORKING_DIR/accession_ids_trimmed.csv $WORKING_DIR/part- --additional-suffix=.csv\n",
        env={
            "WORKING_DIR": "/home/airflow/gcs/data/deepmind/alphafold/v4",
            "OBJECTS_PER_MANIFEST": "10000000",
            "SERVICE_ACCOUNT": "{{ var.json.deepmind.alphafold.service_account }}",
            "SOURCE_BUCKET": "{{ var.json.deepmind.alphafold.source_bucket }}",
        },
    )
    suffix_confidence_v4_json = bash.BashOperator(
        task_id="suffix_confidence_v4_json",
        bash_command='set -e\nmkdir -p $WORKING_DIR/manifests\nfor f in `find $WORKING_DIR/part*.csv -exec basename {} \\;`;\n  do sed "s/$/-confidence_v4.json/" $WORKING_DIR/$f \u003e $WORKING_DIR/manifests/manifest-confidence_v4_json-$f;\ndone\n',
        env={"WORKING_DIR": "/home/airflow/gcs/data/deepmind/alphafold/v4"},
    )
    suffix_model_v4_cif = bash.BashOperator(
        task_id="suffix_model_v4_cif",
        bash_command='set -e\nmkdir -p $WORKING_DIR/manifests\nfor f in `find $WORKING_DIR/part*.csv -exec basename {} \\;`;\n  do sed "s/$/-model_v4.cif/" $WORKING_DIR/$f \u003e $WORKING_DIR/manifests/manifest-model_v4_cif-$f;\ndone\n',
        env={"WORKING_DIR": "/home/airflow/gcs/data/deepmind/alphafold/v4"},
    )
    suffix_predicted_aligned_error_v4_json = bash.BashOperator(
        task_id="suffix_predicted_aligned_error_v4_json",
        bash_command='set -e\nmkdir -p $WORKING_DIR/manifests\nfor f in `find $WORKING_DIR/part*.csv -exec basename {} \\;`;\n  do sed "s/$/-predicted_aligned_error_v4.json/" $WORKING_DIR/$f \u003e $WORKING_DIR/manifests/manifest-predicted_aligned_error_v4_json-$f;\ndone\n',
        env={"WORKING_DIR": "/home/airflow/gcs/data/deepmind/alphafold/v4"},
    )

    # Create and run transfer jobs using manifest files
    create_and_run_sts_jobs_using_manifests = kubernetes_pod.KubernetesPodOperator(
        task_id="create_and_run_sts_jobs_using_manifests",
        name="create_and_run_sts_jobs_using_manifests",
        namespace="composer-user-workloads",
        service_account_name="default",
        config_file="/home/airflow/composer_kube_config",
        image_pull_policy="Always",
        image="{{ var.json.deepmind.alphafold.sts_jobs_generator }}",
        env_vars={
            "MANIFEST_BUCKET": "{{ var.value.composer_bucket }}",
            "MANIFEST_PREFIX": "data/deepmind/alphafold/v4/manifests",
            "SOURCE_BUCKET": "{{ var.json.deepmind.alphafold.source_bucket }}",
            "DESTINATION_BUCKET": "{{ var.json.deepmind.alphafold.destination_bucket_v4 }}",
            "GCP_PROJECT": "{{ var.value.gcp_project }}",
        },
    )

    # Copy manifests to public bucket
    copy_manifests_to_public_bucket = cloud_storage_transfer_service.CloudDataTransferServiceGCSToGCSOperator(
        task_id="copy_manifests_to_public_bucket",
        timeout=43200,
        retries=0,
        wait=True,
        project_id="bigquery-public-data",
        source_bucket="{{ var.value.composer_bucket }}",
        source_path="data/deepmind/alphafold/v4/manifests",
        destination_bucket="{{ var.json.deepmind.alphafold.destination_bucket_v4 }}",
        destination_path="manifests",
        transfer_options={"overwriteWhen": "DIFFERENT"},
    )

    # Load JSON metadata files to BQ
    load_json_metadata_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_json_metadata_to_bq",
        bucket="{{ var.json.deepmind.alphafold.destination_bucket_v4 }}",
        source_objects=["metadata/*.json"],
        source_format="NEWLINE_DELIMITED_JSON",
        destination_project_dataset_table="deepmind_alphafold.metadata",
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "description": "An array of AFDB versions this prediction has had",
                "mode": "REPEATED",
                "name": "allVersions",
                "type": "INTEGER",
            },
            {
                "description": "The latest AFDB version for this prediction",
                "mode": "NULLABLE",
                "name": "latestVersion",
                "type": "INTEGER",
            },
            {
                "description": "List of common organism names",
                "mode": "REPEATED",
                "name": "organismCommonNames",
                "type": "STRING",
            },
            {
                "description": "Number of the last residue in the entry relative to the UniProt entry. This is equal to the length of the protein unless we are dealing with protein fragments",
                "mode": "NULLABLE",
                "name": "uniprotEnd",
                "type": "INTEGER",
            },
            {
                "description": "Short names of the protein",
                "mode": "REPEATED",
                "name": "proteinShortNames",
                "type": "STRING",
            },
            {
                "description": "Number of the first residue in the entry relative to the UniProt entry. This is 1 unless we are dealing with protein fragments",
                "mode": "NULLABLE",
                "name": "uniprotStart",
                "type": "INTEGER",
            },
            {
                "description": "Fraction of the residues in the prediction with pLDDT between 70 and 90",
                "mode": "NULLABLE",
                "name": "fractionPlddtConfident",
                "type": "FLOAT",
            },
            {
                "description": "List of synonyms for the organism",
                "mode": "REPEATED",
                "name": "organismSynonyms",
                "type": "STRING",
            },
            {
                "description": "Fraction of the residues in the prediction with pLDDT greater than 90",
                "mode": "NULLABLE",
                "name": "fractionPlddtVeryHigh",
                "type": "FLOAT",
            },
            {
                "description": "Full names of the protein",
                "mode": "REPEATED",
                "name": "proteinFullNames",
                "type": "STRING",
            },
            {
                "description": "The mean pLDDT of this prediction",
                "mode": "NULLABLE",
                "name": "globalMetricValue",
                "type": "FLOAT",
            },
            {
                "description": "The scientific name of the organism",
                "mode": "NULLABLE",
                "name": "organismScientificName",
                "type": "STRING",
            },
            {
                "description": "The name recommended by the UniProt consortium",
                "mode": "NULLABLE",
                "name": "uniprotDescription",
                "type": "STRING",
            },
            {
                "description": "Fraction of the residues in the prediction with pLDDT between 50 and 70",
                "mode": "NULLABLE",
                "name": "fractionPlddtLow",
                "type": "FLOAT",
            },
            {
                "description": "Uniprot accession ID",
                "mode": "NULLABLE",
                "name": "uniprotAccession",
                "type": "STRING",
            },
            {
                "description": "CRC64 hash of the sequence. Can be used for cheaper lookups.",
                "mode": "NULLABLE",
                "name": "sequenceChecksum",
                "type": "STRING",
            },
            {
                "description": "NCBI taxonomic id of the originating species",
                "mode": "NULLABLE",
                "name": "taxId",
                "type": "INTEGER",
            },
            {
                "description": "The Uniprot EntryName field",
                "mode": "NULLABLE",
                "name": "uniprotId",
                "type": "STRING",
            },
            {
                "description": 'The date of creation for this entry, e.g. "2022-06-01"',
                "mode": "NULLABLE",
                "name": "modelCreatedDate",
                "type": "DATE",
            },
            {
                "description": "Fraction of the residues in the prediction with pLDDT less than 50",
                "mode": "NULLABLE",
                "name": "fractionPlddtVeryLow",
                "type": "FLOAT",
            },
            {
                "description": "Date when the sequence data was last modified in UniProt",
                "mode": "NULLABLE",
                "name": "sequenceVersionDate",
                "type": "DATE",
            },
            {
                "description": 'The AFDB entry ID, e.g. "AF-Q1HGU3-F1"',
                "mode": "NULLABLE",
                "name": "entryId",
                "type": "STRING",
            },
            {
                "description": "Additional synonyms for the gene",
                "mode": "REPEATED",
                "name": "geneSynonyms",
                "type": "STRING",
            },
            {
                "description": "Amino acid sequence for this prediction",
                "mode": "NULLABLE",
                "name": "uniprotSequence",
                "type": "STRING",
            },
            {
                "description": 'The name of the gene if known, e.g. "COII"',
                "mode": "NULLABLE",
                "name": "gene",
                "type": "STRING",
            },
            {
                "description": "Is this protein part of the reference proteome?",
                "mode": "NULLABLE",
                "name": "isReferenceProteome",
                "type": "BOOL",
            },
            {
                "description": "Has this protein been reviewed, i.e. is it part of SwissProt?",
                "mode": "NULLABLE",
                "name": "isReviewed",
                "type": "BOOL",
            },
        ],
    )

    [
        copy_json_metadata_accession_and_fasta_to_public_bucket,
        copy_proteomes_to_public_bucket,
    ] >> load_json_metadata_to_bq
    (
        download_accession_ids_to_composer_bucket
        >> generate_manifests
        >> [
            suffix_confidence_v4_json,
            suffix_model_v4_cif,
            suffix_predicted_aligned_error_v4_json,
        ]
    )
    [
        suffix_confidence_v4_json,
        suffix_model_v4_cif,
        suffix_predicted_aligned_error_v4_json,
    ] >> create_and_run_sts_jobs_using_manifests
    create_and_run_sts_jobs_using_manifests >> [
        copy_manifests_to_public_bucket,
        load_json_metadata_to_bq,
    ]
