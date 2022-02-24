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
def dataset_path() -> typing.Iterator[pathlib.Path]:
    with tempfile.TemporaryDirectory(
        dir=generate_dag.DATASETS_PATH, suffix="_dataset"
    ) as dir_path:
        yield pathlib.Path(dir_path)


@pytest.fixture
def pipeline_path(dataset_path, suffix="_pipeline") -> typing.Iterator[pathlib.Path]:
    pipelines_dir = dataset_path / "pipelines"
    pipelines_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=pipelines_dir, suffix=suffix) as dir_path:
        yield pathlib.Path(dir_path)


def all_pipelines() -> typing.Iterator[typing.Tuple[pathlib.Path, pathlib.Path]]:
    for dataset_path in generate_terraform.list_subdirs(generate_dag.DATASETS_PATH):
        for pipeline_path in generate_terraform.list_subdirs(
            dataset_path / "pipelines"
        ):
            yield dataset_path, pipeline_path


def test_all_dag_ids_are_unique():
    dag_ids = set()
    for dataset_path, pipeline_path in all_pipelines():
        dag_config = yaml.load(open(pipeline_path / "pipeline.yaml"))

        config_dag_id = generate_dag.dag_init(dag_config)["dag_id"]
        namespaced_id = generate_dag.namespaced_dag_id(config_dag_id, dataset_path.name)

        assert namespaced_id not in dag_ids
        dag_ids.add(namespaced_id)


pipeline_path_2 = pipeline_path


def test_non_unique_dag_id_will_fail_validation(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    pipeline_path_2: pathlib.Path,
):
    shutil.copyfile(
        SAMPLE_YAML_PATHS["dataset"], dataset_path / "pipelines" / "dataset.yaml"
    )
    shutil.copyfile(SAMPLE_YAML_PATHS["pipeline"], pipeline_path / "pipeline.yaml")
    shutil.copyfile(SAMPLE_YAML_PATHS["pipeline"], pipeline_path_2 / "pipeline.yaml")

    dag_ids = set()
    all_unique = True
    for dataset_path, pipeline_path in all_pipelines():
        dag_config = yaml.load(open(pipeline_path / "pipeline.yaml"))

        config_dag_id = generate_dag.dag_init(dag_config)["dag_id"]
        namespaced_id = generate_dag.namespaced_dag_id(config_dag_id, dataset_path.name)

        if namespaced_id in dag_ids:
            all_unique = False
            break

        dag_ids.add(namespaced_id)

    assert not all_unique


def test_check_all_dag_ids_must_be_prepended_with_dataset_name():
    for dataset_path, pipeline_path in all_pipelines():
        dag_py = pipeline_path / f"{pipeline_path.name}_dag.py"
        generated_dag_id = f"{dataset_path.name}.{pipeline_path.name}"

        assert f'dag_id="{generated_dag_id}"' in dag_py.read_text()


def test_check_all_dags_have_no_import_errors():
    for dataset_path, pipeline_path in all_pipelines():
        dagbag = models.DagBag(dag_folder=str(pipeline_path))

        assert (
            generate_dag.namespaced_dag_id(pipeline_path.name, dataset_path.name)
            in dagbag.dag_ids
        )
        assert len(dagbag.import_errors) == 0
