# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,


import pathlib
import tempfile
import typing

import pytest
from click.testing import CliRunner
from ruamel import yaml

from scripts import generate_dag, generate_pipeline_files, generate_terraform
from scripts.generate_pipeline_files import create_pipeline

yaml = yaml.YAML(typ="safe")

PROJECT_ROOT = generate_pipeline_files.PROJECT_ROOT
DATASETS_PATH = PROJECT_ROOT / "datasets"

SAMPLE_YAML_PATHS = {
    "dataset": PROJECT_ROOT / "samples" / "dataset.yaml",
    "pipeline": PROJECT_ROOT / "samples" / "pipeline.yaml",
}

ENV_PATH = generate_pipeline_files.PROJECT_ROOT / ".test"
ENV_DATASETS_PATH = ENV_PATH / "datasets"


@pytest.fixture
def env() -> str:
    return "test"


@pytest.fixture
def click_flow() -> dict:
    test_flow = {
        "friendly_dataset_name": "my friendly dataset_description",
        "resource_needed1": "y",
        "resource1": "bq",
        "bq_description": "dataset.yaml bq description",
        "resource_needed2": "y",
        "resource2": "gcs",
        "gcs_bucket_name": "my-pipeline-test-bucket",
        "gcs_bucket_location": "US",
        "resource_needed3": "n",
        "bq_tables": "table1, table2, table3",
        "operators": "BashOperator",
        "add_another_operator": "n",
    }
    return test_flow


@pytest.fixture
def dataset_path() -> typing.Iterator[pathlib.Path]:
    with tempfile.TemporaryDirectory(
        dir=generate_dag.DATASETS_PATH, suffix="_dataset"
    ) as dir_path:
        yield pathlib.Path(dir_path)


@pytest.fixture
def pipeline_path(
    dataset_path: pathlib.Path, suffix="_pipeline"
) -> typing.Iterator[pathlib.Path]:
    pipelines_dir = dataset_path / "pipelines"
    pipelines_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=pipelines_dir, suffix=suffix) as dir_path:
        yield pathlib.Path(dir_path)


def all_pipelines() -> typing.Iterator[typing.Tuple[pathlib.Path, pathlib.Path]]:
    for dataset_path_ in generate_terraform.list_subdirs(generate_dag.DATASETS_PATH):
        for pipeline_path_ in generate_terraform.list_subdirs(
            dataset_path_ / "pipelines"
        ):
            yield dataset_path_, pipeline_path_


def test_pipeline_directory_is_created(click_flow: dict):
    runner = CliRunner()
    runner.invoke(
        create_pipeline,
        "--dataset_id test_dataset --pipeline_id test_pipeline",
        input="\n".join(list(click_flow.values())),
    )

    assert (DATASETS_PATH / "test_dataset" / "pipelines" / "test_pipeline").exists()
    assert (DATASETS_PATH / "test_dataset" / "pipelines" / "test_pipeline").is_dir()
    assert (DATASETS_PATH / "test_dataset" / "pipelines").exists()
    assert (DATASETS_PATH / "test_dataset" / "pipelines").is_dir()


def test_dataset_yaml_file_created(click_flow: dict):
    runner = CliRunner()
    runner.invoke(
        create_pipeline,
        "--dataset_id test_dataset --pipeline_id test_pipeline",
        input="\n".join(list(click_flow.values())),
    )
    assert (DATASETS_PATH / "test_dataset" / "pipelines" / "dataset.yaml").exists()
    assert (DATASETS_PATH / "test_dataset" / "pipelines" / "dataset.yaml").is_file()


def test_dataset_yaml_contains_proper_sample_templates(click_flow: dict):
    runner = CliRunner()
    runner.invoke(
        create_pipeline,
        "--dataset_id test_dataset --pipeline_id test_pipeline",
        input="\n".join(list(click_flow.values())),
    )
    dataset_yaml_file = (
        DATASETS_PATH / "test_dataset" / "pipelines" / "dataset.yaml"
    ).read_text()
    dataset_yaml = yaml.load(dataset_yaml_file)
    license_header = (
        PROJECT_ROOT / "templates" / "airflow" / "license_header.py.jinja2"
    ).read_text()

    assert license_header in dataset_yaml_file  # test for license header
    assert (
        len(dataset_yaml["resources"]) == 2
    )  # test dataset yaml has 2 resources added (bq, gcs)
    assert "dataset" in list(
        dataset_yaml.keys()
    )  # confirm keys of yaml file are correct
    assert "resources" in list(
        dataset_yaml.keys()
    )  # confirm keys of yaml file are correct


def test_pipeline_yaml_file_created(click_flow: dict):
    runner = CliRunner()
    runner.invoke(
        create_pipeline,
        "--dataset_id test_dataset --pipeline_id test_pipeline",
        input="\n".join(list(click_flow.values())),
    )
    assert (
        DATASETS_PATH / "test_dataset" / "pipelines" / "test_pipeline" / "pipeline.yaml"
    ).exists()
    assert (
        DATASETS_PATH / "test_dataset" / "pipelines" / "test_pipeline" / "pipeline.yaml"
    ).is_file()


def test_pipeline_yaml_contains_proper_sample_templates(click_flow: dict):
    runner = CliRunner()
    runner.invoke(
        create_pipeline,
        "--dataset_id test_dataset --pipeline_id test_pipeline",
        input="\n".join(list(click_flow.values())),
    )
    pipeline_yaml_file = (
        DATASETS_PATH / "test_dataset" / "pipelines" / "test_pipeline" / "pipeline.yaml"
    ).read_text()
    pipeline_yaml = yaml.load(pipeline_yaml_file)
    license_header = (
        PROJECT_ROOT / "templates" / "airflow" / "license_header.py.jinja2"
    ).read_text()

    assert license_header in pipeline_yaml_file  # test for license header
    assert len(pipeline_yaml["resources"]) == 3  # test pipeline yaml has 3 bq resources
    assert len(pipeline_yaml["dag"]["tasks"]) == 1  # confirm single task has been added
    assert (
        "BashOperator" == pipeline_yaml["dag"]["tasks"][0]["operator"]
    )  # confirm BashOperator was added
