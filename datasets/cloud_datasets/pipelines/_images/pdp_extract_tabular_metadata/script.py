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

import dataclasses
import datetime
import logging
import os
import threading
import time
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from google.cloud import bigquery

NUM_THREADS = 5

# Update these three column variables if the schema in pipeline.yaml changes.
TABULAR_DATASETS_COLUMNS = [
    "extracted_at",
    "created_at",
    "modified_at",
    "project_id",
    "dataset_id",
    "description",
    "num_tables",
]

TABLES_COLUMNS = [
    "extracted_at",
    "created_at",
    "modified_at",
    "project_id",
    "dataset_id",
    "table_id",
    "description",
    "type",
    "num_bytes",
    "num_rows",
    "num_columns",
    "described_columns",
]

TABULES_FIELDS_COLUMNS = [
    "extracted_at",
    "project_id",
    "dataset_id",
    "table_id",
    "name",
    "description",
    "field_type",
    "mode",
    "precision",
    "scale",
    "max_length",
]


def is_empty(s: str) -> bool:
    """Return True if s is None or an empty string."""
    # pylint: disable=g-explicit-bool-comparison
    return pd.isnull(s) or str(s).strip() == ""


@dataclasses.dataclass
class FieldInfo:
    """Represents the schema of a column of a BQ table."""

    project_id: str = None
    dataset_id: str = None
    table_id: str = None
    name: str = None
    description: str = None
    field_type: str = None
    mode: str = None
    precision: int = None
    scale: int = None
    max_length: int = None

    def __init__(self, schema: bigquery.SchemaField):
        self.name = schema.name
        self.description = schema.description
        self.field_type = schema.field_type
        self.mode = schema.mode
        self.precision = schema.precision
        self.scale = schema.scale
        self.max_length = schema.max_length


@dataclasses.dataclass
class TableInfo:
    """Represents the metadata for a single table."""

    project_id: str = None
    dataset_id: str = None
    table_id: str = None
    type: str = None
    extracted_at: datetime.datetime = None
    created_at: datetime.datetime = None
    modified_at: datetime.datetime = None
    description: str = None
    num_rows: int = 0
    num_bytes: int = 0
    num_columns: int = 0
    described_columns: int = 0

    def __init__(self, table_object: bigquery.Table):
        self.project_id = table_object.project
        self.dataset_id = table_object.dataset_id
        self.table_id = table_object.table_id
        self.type = str(table_object.table_type)
        self.created_at = table_object.created
        self.modified_at = table_object.modified
        self.description = table_object.description
        self.location = table_object.location
        if is_empty(self.description):
            self.description = np.nan
        self.num_rows = table_object.num_rows
        self.num_bytes = table_object.num_bytes
        self.num_columns = len(table_object.schema)
        self.described_columns = len(
            [s.description for s in table_object.schema if not is_empty(s.description)]
        )

    def __repr__(self) -> str:
        return f"{self.project_id}.{self.dataset_id}.{self.table_id}"


@dataclasses.dataclass
class DatasetInfo:
    """Represents the metadata for a single dataset."""

    extracted_at: datetime.datetime = None
    created_at: datetime.datetime = None
    modified_at: datetime.datetime = None
    project_id: str = None
    dataset_id: str = None
    description: str = None
    num_tables: int = None

    def __init__(
        self,
        dataset_object: bigquery.Dataset,
        dataset_reference: bigquery.DatasetReference,
    ):
        self.project_id = dataset_object.project
        self.dataset_id = dataset_object.dataset_id
        self.description = dataset_reference.description
        if is_empty(self.description):
            self.description = np.nan
        self.created_at = dataset_reference.created
        self.modified_at = dataset_reference.modified

    def __repr__(self) -> str:
        return f"{self.project_id}.{self.dataset_id}"


class DatasetsTablesInfoExtractor:
    """Extracts BQ datasets and tables metadata and stores them in BQ."""

    def __init__(self, project_id: str, target_project_id: str, target_dataset: str):
        self.client = bigquery.Client(project_id)
        self.target_project_id = target_project_id
        self.target_dataset = target_dataset
        self.datasets = []
        self.tables = []
        self.tables_fields = []

    def _read_tables_and_schema(self, full_table_ids: List[str]):
        """Read the tables metadata and the schema of each table."""
        for full_table_id in full_table_ids:
            table_object = self.client.get_table(full_table_id)
            table = TableInfo(table_object)
            self.tables.append(table)
            for sch in table_object.schema:
                field_info = FieldInfo(sch)
                field_info.project_id = table.project_id
                field_info.dataset_id = table.dataset_id
                field_info.table_id = table.table_id
                self.tables_fields.append(field_info)

    def parallel_read_tables(self, full_table_ids: List[str]):
        """Read tables metadata in parallel."""
        num_tables = len(full_table_ids)
        potential_interval_size = num_tables // NUM_THREADS
        residual = num_tables % NUM_THREADS
        index = 0
        threads = []
        while index < num_tables:
            actual_interval_size = potential_interval_size
            if residual > 0:
                actual_interval_size += 1
                residual -= 1
            tables_ids = full_table_ids[index : index + actual_interval_size]
            tr = threading.Thread(
                target=self._read_tables_and_schema, args=(tables_ids,)
            )
            threads.append(tr)
            index += actual_interval_size
        for tr in threads:
            tr.start()
        for tr in threads:
            tr.join()

    def get_datasets_as_dict(self) -> Dict[str, Any]:
        return [dataclasses.asdict(d) for d in self.datasets]

    def get_tables_as_dict(self) -> Dict[str, Any]:
        return [dataclasses.asdict(t) for t in self.tables]

    def get_tables_fields_as_dict(self) -> Dict[str, Any]:
        return [dataclasses.asdict(t) for t in self.tables_fields]

    def get_datasets_as_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.get_datasets_as_dict())

    def get_tables_as_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.get_tables_as_dict())

    def get_tables_fields_as_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.get_tables_fields_as_dict())

    def read_datasets(self):
        """Read the datasets and tables metadata."""
        datasets_list = list(self.client.list_datasets())
        full_table_ids = []
        logging.info("Enlisted Datasets: %s", len(datasets_list))
        for dataset_item in datasets_list:
            if dataset_item.dataset_id.startswith("_"):
                continue  # Not a public dataset
            dataset_reference = self.client.get_dataset(dataset_item.reference)
            dataset = DatasetInfo(dataset_item, dataset_reference)
            table_ids = list(self.client.list_tables(dataset_reference))
            dataset.num_tables = len(table_ids)
            full_table_ids.extend(
                [t.full_table_id.replace(":", ".") for t in table_ids]
            )

            self.datasets.append(dataset)

        self.parallel_read_tables(full_table_ids)
        logging.info("Extracted Datasets: %s", len(self.datasets))
        logging.info("Extracted Tables: %s", len(self.tables))
        logging.info("Extracted Fields: %s", len(self.tables_fields))

    def write_datasets_to_bq(self, table_name: str, extracted_time: datetime.datetime):
        """Write datasets metadata to BQ."""

        dataset_ref = bigquery.DatasetReference(
            self.target_project_id, self.target_dataset
        )
        table_id = bigquery.TableReference(dataset_ref, table_name)
        logging.debug("Writing to %s...", table_id)

        job_config = bigquery.job.LoadJobConfig(autodetect=False, max_bad_records=5)

        datasets_dataframe = self.get_datasets_as_dataframe()
        datasets_dataframe["extracted_at"] = extracted_time
        datasets_dataframe = datasets_dataframe[TABULAR_DATASETS_COLUMNS]

        job = self.client.load_table_from_dataframe(
            datasets_dataframe, table_id, job_config=job_config
        )
        job.result()  # Wait for the job to complete.

        logging.debug("write_datasets_to_bq done")

    def write_tables_to_bq(self, table_name: str, extracted_time: datetime.datetime):
        """Write tables metadata to BQ."""
        dataset_ref = bigquery.DatasetReference(
            self.target_project_id, self.target_dataset
        )
        table_id = bigquery.TableReference(dataset_ref, table_name)
        logging.debug("Writing to %s...", table_id)

        job_config = bigquery.job.LoadJobConfig(autodetect=False, max_bad_records=5)

        tables_dataframe = self.get_tables_as_dataframe()
        tables_dataframe["extracted_at"] = extracted_time
        tables_dataframe = tables_dataframe[TABLES_COLUMNS]

        job = self.client.load_table_from_dataframe(
            tables_dataframe, table_id, job_config=job_config
        )
        job.result()  # Wait for the job to complete.

        logging.debug("write_tables_to_bq is done")

    def write_tables_fields_to_bq(
        self, table_name: str, extracted_time: datetime.datetime
    ):
        """Write tables_fields to BQ."""
        dataset_ref = bigquery.DatasetReference(
            self.target_project_id, self.target_dataset
        )
        table_id = bigquery.TableReference(dataset_ref, table_name)
        logging.debug("Writing to %s...", table_id)

        job_config = bigquery.job.LoadJobConfig(
            autodetect=False,
            max_bad_records=5,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        tables_fields_dataframe = self.get_tables_fields_as_dataframe()
        tables_fields_dataframe["extracted_at"] = extracted_time
        tables_fields_dataframe = tables_fields_dataframe[TABULES_FIELDS_COLUMNS]

        job = self.client.load_table_from_dataframe(
            tables_fields_dataframe, table_id, job_config=job_config
        )
        job.result()  # Wait for the job to complete.

        logging.debug("write_tables_fields_to_bq is done")


def main(
    source_projects_ids: List[str],
    target_project_id: str,
    target_dataset: str,
    tabular_dataset_table_name: str,
    tables_table_name: str,
    tables_fields_table_name: str,
):
    """Entry point for this cloud function."""
    st = time.time()
    for project_id in source_projects_ids.split(","):
        extractor = DatasetsTablesInfoExtractor(
            project_id, target_project_id, target_dataset
        )
        extractor.read_datasets()
        extracted = datetime.datetime.now()
        extractor.write_datasets_to_bq(tabular_dataset_table_name, extracted)
        extractor.write_tables_to_bq(tables_table_name, extracted)
        extractor.write_tables_fields_to_bq(tables_fields_table_name, extracted)
    logging.info("Total time to run this function: ", time.time() - st)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_projects_ids=os.environ["SOURCE_PROJECTS_IDS"],
        target_project_id=os.environ["TARGET_PROJECT_ID"],
        target_dataset=os.environ["TARGET_DATASET"],
        tabular_dataset_table_name=os.environ["TABULAR_DATASET_TABLE_NAME"],
        tables_table_name=os.environ["TABLES_TABLE_NAME"],
        tables_fields_table_name=os.environ["TABLES_FIELDS_TABLE_NAME"],
    )
