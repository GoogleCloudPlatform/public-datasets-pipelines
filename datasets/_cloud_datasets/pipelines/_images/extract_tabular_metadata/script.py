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


def is_empty(s: str) -> bool:
    """Return True if s is None or an empty string."""
    # pylint: disable=g-explicit-bool-comparison
    return pd.isnull(s) or str(s).strip() == ''


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
        self.described_columns = len([
            s.description
            for s in table_object.schema
            if not is_empty(s.description)
        ])

    def __repr__(self) -> str:
        return f'{self.project_id}.{self.dataset_id}.{self.table_id}'


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

    def __init__(self, dataset_object: bigquery.Dataset,
                 dataset_reference: bigquery.DatasetReference):
        self.project_id = dataset_object.project
        self.dataset_id = dataset_object.dataset_id
        self.description = dataset_reference.description
        if is_empty(self.description):
            self.description = np.nan
        self.created_at = dataset_reference.created
        self.modified_at = dataset_reference.modified

    def __repr__(self) -> str:
        return f'{self.project_id}.{self.dataset_id}'


class DatasetsTablesInfoExtractor:
    """Extracts BQ datasets and tables metadata and stores them in BQ."""

    def __init__(self,
                 project_id: str,
                 target_project_id: str,
                 target_dataset: str):
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
        potential_interval_size = (num_tables // NUM_THREADS)
        residual = num_tables % NUM_THREADS
        index = 0
        threads = []
        while index < num_tables:
            actual_interval_size = potential_interval_size
            if residual > 0:
                actual_interval_size += 1
                residual -= 1
            tables_ids = full_table_ids[index:index + actual_interval_size]
            tr = threading.Thread(
                target=self._read_tables_and_schema, args=(tables_ids,))
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
        print(f'Enlisted Datasets: {len(datasets_list)}')
        for dataset_item in datasets_list:
            dataset_reference = self.client.get_dataset(dataset_item.reference)
            dataset = DatasetInfo(dataset_item, dataset_reference)
            table_ids = list(self.client.list_tables(dataset_reference))
            dataset.num_tables = len(table_ids)
            full_table_ids.extend(
                [t.full_table_id.replace(':', '.') for t in table_ids])

            self.datasets.append(dataset)

        self.parallel_read_tables(full_table_ids)
        print(f'Extracted Datasets: {len(self.datasets)}')
        print(f'Extracted Tables: {len(self.tables)}')
        print(f'Extracted Fields: {len(self.tables_fields)}')

    def write_datasets_to_bq(self, table_name: str,
                             extracted_time: datetime.datetime):
        """Write datasets metadata to BQ."""
        dataset_ref = bigquery.DatasetReference(self.target_project_id, self.target_dataset)
        table_id = bigquery.TableReference(dataset_ref, table_name)
        print(f'Writing to {table_id}...')

        job_config = bigquery.job.LoadJobConfig(
            autodetect=False,
            max_bad_records=5,
            schema=[
                bigquery.SchemaField(
                    'extracted_at',
                    'TIMESTAMP',
                    description='Datetime when this row was extracted from BQ'),
                bigquery.SchemaField(
                    'created_at',
                    'TIMESTAMP',
                    description='Datetime when the dataset was created'),
                bigquery.SchemaField(
                    'modified_at',
                    'TIMESTAMP',
                    description='Datetime when the dataset was last modified'),
                bigquery.SchemaField(
                    'project_id',
                    'STRING',
                    description='GCP project where from where public dataset is'),
                bigquery.SchemaField(
                    'dataset_id',
                    'STRING',
                    description='BigQuery dataset'),
                bigquery.SchemaField(
                    'description',
                    'STRING',
                    description='The dataset description'),
                bigquery.SchemaField(
                    'num_tables',
                    'INTEGER',
                    description='Number of tables contained in this dataset'),
            ])

        print(f'job sonfig: {job_config}')

        datasets_dataframe = self.get_datasets_as_dataframe()
        datasets_dataframe['extracted_at'] = extracted_time
        columns = [si.name for si in job_config.schema]
        datasets_dataframe = datasets_dataframe[columns]

        job = self.client.load_table_from_dataframe(
            datasets_dataframe, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete.

        print('write_datasets_to_bq done')

    def write_tables_to_bq(self, table_name: str,
                           extracted_time: datetime.datetime):
        """Write tables metadata to BQ."""
        dataset_ref = bigquery.DatasetReference(self.target_project_id, self.target_dataset)
        table_id = bigquery.TableReference(dataset_ref, table_name)
        print(f'Writing to {table_id}...')

        job_config = bigquery.job.LoadJobConfig(
            autodetect=False,
            max_bad_records=5,
            schema=[
                bigquery.SchemaField(
                    'extracted_at',
                    'TIMESTAMP',
                    description='Datetime when this row was extracted from BQ'),
                bigquery.SchemaField(
                    'created_at',
                    'TIMESTAMP',
                    description='Datetime when the dataset was created'),
                bigquery.SchemaField(
                    'modified_at',
                    'TIMESTAMP',
                    description='Datetime when the dataset was last modified'),
                bigquery.SchemaField(
                    'project_id',
                    'STRING',
                    description='GCP project where from where public dataset is'),
                bigquery.SchemaField(
                    'dataset_id',
                    'STRING',
                    description='BigQuery dataset'),
                bigquery.SchemaField(
                    'table_id',
                    'STRING',
                    description='BigQuery table'),
                bigquery.SchemaField(
                    'description',
                    'STRING',
                    description='The dataset description'),
                bigquery.SchemaField(
                    'type',
                    'STRING',
                    description='The type of the table'),
                bigquery.SchemaField(
                    'num_bytes',
                    'INTEGER',
                    description='The number of bytes the table allocated on disk'),
                bigquery.SchemaField(
                    'num_rows',
                    'INTEGER',
                    description='The number of rows of the table'),
                bigquery.SchemaField(
                    'num_columns',
                    'INTEGER',
                    description='The number of columns of the table'),
                bigquery.SchemaField(
                    'described_columns',
                    'INTEGER',
                    description='The number of columns with a description'),
            ])

        print(f'SCHEMA: {job_config.schema}')

        tables_dataframe = self.get_tables_as_dataframe()
        tables_dataframe['extracted_at'] = extracted_time
        columns = [si.name for si in job_config.schema]
        tables_dataframe = tables_dataframe[columns]

        job = self.client.load_table_from_dataframe(
            tables_dataframe, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete.

        print('write_tables_to_bq is done')

    def write_tables_fields_to_bq(self, table_name: str,
                                  extracted_time: datetime.datetime):
        """Write tables_fields to BQ."""
        dataset_ref = bigquery.DatasetReference(self.target_project_id, self.target_dataset)
        table_id = bigquery.TableReference(dataset_ref, table_name)
        print(f'Writing to {table_id}...')

        job_config = bigquery.job.LoadJobConfig(
            autodetect=False,
            max_bad_records=5,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema=[
                bigquery.SchemaField(
                    'extracted_at',
                    'TIMESTAMP',
                    description='Datetime when this row was extracted from BQ'),
                bigquery.SchemaField(
                    'project_id',
                    'STRING',
                    description='GCP project where from where public dataset is'),
                bigquery.SchemaField(
                    'dataset_id',
                    'STRING',
                    description='BigQuery dataset'),
                bigquery.SchemaField(
                    'table_id',
                    'STRING',
                    description='BigQuery table'),
                bigquery.SchemaField(
                    'name',
                    'STRING',
                    description='The name of the field'),
                bigquery.SchemaField(
                    'description',
                    'STRING',
                    description='Description for the field.'),
                bigquery.SchemaField(
                    'field_type',
                    'STRING',
                    description='The type of the field'),
                bigquery.SchemaField(
                    'mode',
                    'STRING',
                    description='The mode of the field'),
                bigquery.SchemaField(
                    'precision',
                    'INTEGER',
                    description='Precision for the NUMERIC field'),
                bigquery.SchemaField(
                    'scale',
                    'INTEGER',
                    description='Scale for the NUMERIC field'),
                bigquery.SchemaField(
                    'max_length',
                    'INTEGER',
                    description='Maximum length for the STRING or BYTES field'),
            ])

        print(f'SCHEMA: {job_config.schema}')

        tables_fields_dataframe = self.get_tables_fields_as_dataframe()
        tables_fields_dataframe['extracted_at'] = extracted_time
        columns = [si.name for si in job_config.schema]
        tables_fields_dataframe = tables_fields_dataframe[columns]

        job = self.client.load_table_from_dataframe(
            tables_fields_dataframe, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete.

        print('write_tables_fields_to_bq is done')


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
    for project_id in source_projects_ids.split(','):
        extractor = DatasetsTablesInfoExtractor(project_id, target_project_id, target_dataset)
        extractor.read_datasets()
        extracted = datetime.datetime.now()
        extractor.write_datasets_to_bq(tabular_dataset_table_name, extracted)
        extractor.write_tables_to_bq(tables_table_name, extracted)
        extractor.write_tables_fields_to_bq(tables_fields_table_name, extracted)
    print(f'Total time to run this function: {time.time() - st}')


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