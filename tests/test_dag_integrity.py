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
import shutil
import tempfile
import typing

import pytest
from airflow import models
from ruamel import yaml

from scripts import generate_dag, generate_terraform

yaml = yaml.YAML(typ="safe")

PROJECT_ROOT = generate_dag.PROJECT_ROOT
SAMPLE_YAML_PATHS = {
    "dataset": PROJECT_ROOT / "samples" / "dataset.yaml",
    "pipeline": PROJECT_ROOT / "samples" / "pipeline.yaml",
}


@pytest.fixture
def env() -> str:
    return "test"


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


def copy_config_files_and_set_tmp_folder_names_as_ids(
    dataset_path: pathlib.Path, pipeline_path: pathlib.Path
):
    shutil.copyfile(
        SAMPLE_YAML_PATHS["dataset"], dataset_path / "pipelines" / "dataset.yaml"
    )
    shutil.copyfile(SAMPLE_YAML_PATHS["pipeline"], pipeline_path / "pipeline.yaml")

    dataset_config = yaml.load(dataset_path / "pipelines" / "dataset.yaml")
    dataset_yaml_str = (
        (dataset_path / "pipelines" / "dataset.yaml")
        .read_text()
        .replace(
            f"name: {dataset_config['dataset']['name']}", f"name: {dataset_path.name}"
        )
    )
    generate_dag.write_to_file(
        dataset_yaml_str, dataset_path / "pipelines" / "dataset.yaml"
    )

    pipeline_config = yaml.load(pipeline_path / "pipeline.yaml")
    pipeline_yaml_str = (
        (pipeline_path / "pipeline.yaml")
        .read_text()
        .replace(
            f"dag_id: {pipeline_config['dag']['initialize']['dag_id']}",
            f"dag_id: {pipeline_path.name}",
        )
    )
    generate_dag.write_to_file(pipeline_yaml_str, pipeline_path / "pipeline.yaml")


def test_correct_imports_have_no_errors(
    dataset_path: pathlib.Path, pipeline_path: pathlib.Path, env: str
):
    copy_config_files_and_set_tmp_folder_names_as_ids(dataset_path, pipeline_path)

    generate_dag.main(dataset_path.name, pipeline_path.name, env)

    dagbag = models.DagBag(dag_folder=str(pipeline_path))

    assert (
        generate_dag.namespaced_dag_id(pipeline_path.name, dataset_path.name)
        in dagbag.dag_ids
    )
    assert len(dagbag.import_errors) == 0


def test_incorrect_imports_will_raise_errors(
    dataset_path: pathlib.Path, pipeline_path: pathlib.Path, env: str
):
    copy_config_files_and_set_tmp_folder_names_as_ids(dataset_path, pipeline_path)

    generate_dag.main(dataset_path.name, pipeline_path.name, env)

    dag_path = pipeline_path / f"{pipeline_path.name}_dag.py"
    original_code = dag_path.read_text()
    with open(dag_path, "w") as modified:
        modified.write("from airflow.bogus import Bogus\n" + original_code)

    dagbag = models.DagBag(dag_folder=str(pipeline_path))
    assert len(dagbag.import_errors) == 1
    assert "No module named" in dagbag.import_errors[str(dag_path)]
