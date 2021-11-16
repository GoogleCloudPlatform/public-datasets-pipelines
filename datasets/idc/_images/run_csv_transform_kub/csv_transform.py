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

import logging
import os
import pathlib

from airflow.contrib.operators.gcs_to_gcs import (
    GoogleCloudStorageToGoogleCloudStorageOperator,
)

# from airflow.exceptions import AirflowException
from google.cloud import bigquery, bigquery_datatransfer  # , storage


def main(
    source_gcs_bucket: pathlib.Path,
    source_gcs_files: str,
    target_gcs_bucket: pathlib.Path,
    target_gcs_path: str,
    source_project_id: str,
    source_dataset_prefix: str,
    source_dataset_list: list,
    target_project_id: str,
    user_id: str,
) -> None:

    logging.info("IDC data migration process started")

    # update_images(source_gcs_bucket, source_gcs_files, target_gcs_bucket, target_gcs_path)

    # dataset_ver = obtain_project_new_version(project_id=project_id, dataset_prefix=dataset_prefix)
    # logging.info(f"Dataset to use is {project_id}.{dataset_ver}")

    transfer_bq_data(
        source_project_id,
        source_dataset_list,
        target_project_id,
        user_id,
        copy_display_name="copy executing...",
    )

    logging.info("IDC data migration process completed")


def transfer_bq_data(
    source_project_id: str,
    source_dataset_list: list,
    target_project_id: str,
    user_id: str,
    copy_display_name: str = "copy executing...",
):
    transfer_client = bigquery_datatransfer.DataTransferServiceClient()
    # transfer_config = ""
    logging.info(
        f"Creating transfer config for {source_project_id}.[{source_dataset_list}] -> {target_project_id}"
    )
    for ds in source_dataset_list:
        transfer_config = bigquery_datatransfer.TransferConfig(
            destination_dataset_id=ds,
            display_name=copy_display_name,
            # data_source_id="cross_region_copy",
            params={
                "source_project_id": source_project_id,
                "source_dataset_id": ds,  # source_dataset_id,
            },
            # schedule="every 24 hours",
            user_id=user_id
            # authenticationinfo=user_id
        )
        transfer_config = transfer_client.create_transfer_config(
            parent=transfer_client.common_project_path(target_project_id),
            transfer_config=transfer_config,
        )
        logging.info(f"Created transfer config {transfer_config.name}")


def update_images(
    source_gcs_bucket: str,
    source_gcs_files: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
):
    download_images(
        source_gcs_bucket, source_gcs_files, target_gcs_bucket, target_gcs_path
    )
    # load_image_data()


def download_images(
    source_gcs_bucket: str,
    source_gcs_files: str,
    target_gcs_bucket: str,
    target_gcs_path: str,
) -> None:
    copy_image_files = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id="copy_files",
        source_bucket=source_gcs_bucket,
        source_object=source_gcs_files,
        destination_bucket=target_gcs_bucket,
        destination_object=f"{target_gcs_path}/",
    )
    copy_image_files.execute(None)


def list_datasets(project_id: str = "") -> None:
    if project_id:
        client = bigquery.Client(project=project_id)
    else:
        client = bigquery.Client()
    project = client.project
    datasets = list(client.list_datasets())
    if datasets:
        logging.info("Datasets in project {}:".format(project))
        for dataset in datasets:
            logging.info("\t{}".format(dataset.dataset_id))
    else:
        logging.info("{} project does not contain any datasets.".format(project))


def list_projects() -> None:
    client = bigquery.Client()
    projects = list(client.list_projects())
    idc_datasets = []
    if projects:
        logging.info("Projects in client {}:".format(client))
        for project in projects:
            if str(project.project_id).startswith("idc-pdp"):
                logging.info("\t{}".format(project.project_id))
                proj_dataset = ""
                for dataset in client.list_datasets(project=project.project_id):
                    if str(dataset.dataset_id).startswith("idc_v"):
                        proj_dataset = dataset.dataset_id
                        logging.info(f"Datasets in project {proj_dataset}:")
                        idc_datasets.append(dataset.dataset_id)
                max_ver = max(idc_datasets)
                logging.info(f"dataset with most recent varsion of data is {max_ver}")
    else:
        logging.info("{} client does not contain any projects.".format(client))


def obtain_project_new_version(project_id: str = "", dataset_prefix: str = "") -> str:
    if project_id:
        client = bigquery.Client(project=project_id)
    else:
        client = bigquery.Client()
    project = client.project
    logging.info("Identifying max version of dataset in project {}:".format(project))
    proj_dataset = ""
    idc_datasets = []
    max_ver = ""
    for dataset in client.list_datasets(project=project):
        if dataset_prefix == "":
            logging.info(
                "Please specify the dataset prefix used to identify the most recent version of the dataset"
            )
        else:
            if str(dataset.dataset_id).startswith(dataset_prefix):
                proj_dataset = dataset.dataset_id
                idc_datasets.append(proj_dataset)
            max_ver = max(idc_datasets)

    logging.info(f"dataset with most recent varsion of data is {max_ver}")

    return max_ver


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_gcs_bucket=os.environ["SOURCE_GCS_BUCKET"],
        source_gcs_files=os.environ["SOURCE_GCS_FILES"],
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        # chunksize=os.environ["CHUNKSIZE"],
        source_project_id=os.environ["SOURCE_PROJECT_ID"],
        source_dataset_prefix=os.environ["SOURCE_DATASET_PREFIX"],
        source_dataset_list=os.environ["SOURCE_DATASET_LIST"],
        target_project_id=os.environ["TARGET_PROJECT_ID"],
        user_id=os.environ["USER_ID"],
    )
