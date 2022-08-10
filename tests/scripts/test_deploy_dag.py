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


import json
import pathlib
import shutil
import subprocess
import tempfile
import typing
import uuid

import pytest
from ruamel import yaml

from scripts import deploy_dag, generate_dag

yaml = yaml.YAML(typ="safe")

PROJECT_ROOT = generate_dag.PROJECT_ROOT
SAMPLE_YAML_PATHS = {
    "dataset": PROJECT_ROOT / "samples" / "dataset.yaml",
    "pipeline": PROJECT_ROOT / "samples" / "pipeline.yaml",
    "variables": PROJECT_ROOT / "samples" / "dataset_variables.json",
}

ENV_PATH = generate_dag.PROJECT_ROOT / ".test"
ENV_DATASETS_PATH = ENV_PATH / "datasets"


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


@pytest.fixture
def env() -> str:
    return "test"


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
    (ENV_DATASETS_PATH / dataset_path.name / "pipelines" / pipeline_path.name).mkdir(
        parents=True, exist_ok=True
    )
    shutil.copyfile(
        pipeline_path / "pipeline.yaml",
        ENV_DATASETS_PATH
        / dataset_path.name
        / "pipelines"
        / pipeline_path.name
        / "pipeline.yaml",
    )


def setup_dag_and_variables(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    variables_filename: str,
    mocker,
):
    copy_config_files_and_set_tmp_folder_names_as_ids(dataset_path, pipeline_path)

    # Optimize test runtimes by skipping code formatting
    mocker.patch("scripts.generate_dag.format_python_code")

    generate_dag.main(
        dataset_id=dataset_path.name, pipeline_id=pipeline_path.name, env=env
    )

    shutil.copyfile(
        SAMPLE_YAML_PATHS["variables"],
        ENV_DATASETS_PATH / dataset_path.name / "pipelines" / variables_filename,
    )


def test_script_always_requires_dataset_arg(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(
            [
                "python",
                "scripts/deploy_dag.py",
                "--env",
                env,
            ],
            cwd=deploy_dag.PROJECT_ROOT,
        )


pipeline_path_2 = pipeline_path


def test_script_can_deploy_without_variables_files(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    # Delete the dataset-specific variables file
    (
        ENV_DATASETS_PATH
        / dataset_path.name
        / "pipelines"
        / f"{dataset_path.name}_variables.json"
    ).unlink()
    assert not (
        ENV_DATASETS_PATH
        / dataset_path.name
        / "pipelines"
        / f"{dataset_path.name}_variables.json"
    ).exists()

    mocker.patch("scripts.deploy_dag.run_gsutil_cmd")
    mocker.patch("scripts.deploy_dag.run_cloud_composer_vars_import")
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=2)

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )


def test_vars_yaml_generates_pipeline_vars_json_file(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    variables_filename = f"{dataset_path.name}_variables.json"
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        variables_filename,
        mocker,
    )

    # Delete the variables JSON file
    variables_json = (
        ENV_DATASETS_PATH / dataset_path.name / "pipelines" / variables_filename
    )
    variables_json.unlink()
    assert not variables_json.exists()

    # Create .vars.test.yaml file
    pipeline_vars = {
        f"{dataset_path.name}": {
            "airflow_var": f"var-{uuid.uuid4()}",
            "constant_var": 1234,
        }
    }
    yaml.dump({"pipelines": pipeline_vars}, dataset_path / f".vars.{env}.yaml")

    # Local variables will be used. Assum remote vars do not yet exist.
    mocker.patch(
        "scripts.deploy_dag.get_airflow_var_from_composer_env", return_value=None
    )

    # Patch remote calls
    mocker.patch("scripts.deploy_dag.run_cloud_composer_vars_import")
    mocker.patch("scripts.deploy_dag.run_gsutil_cmd")
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=2)

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )

    assert variables_json.exists()
    assert json.loads(variables_json.read_text()) == pipeline_vars


def test_import_vars_works_with_only_vars_json():
    pass


def test_vars_not_imported_to_composer_when_local_and_remote_vars_are_equal(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    variables_filename = f"{dataset_path.name}_variables.json"
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        variables_filename,
        mocker,
    )

    # Set variables
    vars_ = {
        f"{dataset_path.name}": {
            "airflow_var": f"var-{uuid.uuid4()}",
            "constant_var": 1234,
        }
    }

    # Set local variables to `vars_`
    variables_json = (
        ENV_DATASETS_PATH / dataset_path.name / "pipelines" / variables_filename
    )
    variables_json.write_text(json.dumps(vars_))
    assert variables_json.stat().st_size > 0

    # Set remote variables to `vars_`
    mocker.patch(
        "scripts.deploy_dag.get_airflow_var_from_composer_env", return_value=vars_
    )

    # Patch remote calls
    mocker.patch("scripts.deploy_dag.run_cloud_composer_vars_import")
    mocker.patch("scripts.deploy_dag.run_gsutil_cmd")
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=2)

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )

    assert not deploy_dag.run_cloud_composer_vars_import.called


def test_vars_not_imported_to_composer_when_local_and_remote_vars_are_null(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    variables_filename = f"{dataset_path.name}_variables.json"
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        variables_filename,
        mocker,
    )

    # Remove local variables
    variables_json = (
        ENV_DATASETS_PATH / dataset_path.name / "pipelines" / variables_filename
    )
    variables_json.unlink()
    assert not variables_json.exists()

    # Remove remote variables
    mocker.patch(
        "scripts.deploy_dag.get_airflow_var_from_composer_env", return_value=None
    )

    # Patch remote calls
    mocker.patch("scripts.deploy_dag.run_cloud_composer_vars_import")
    mocker.patch("scripts.deploy_dag.run_gsutil_cmd")
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=2)

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )

    assert not deploy_dag.run_cloud_composer_vars_import.called


def test_vars_not_imported_to_composer_when_local_vars_are_null_but_remote_vars_exist(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    variables_filename = f"{dataset_path.name}_variables.json"
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        variables_filename,
        mocker,
    )

    # Delete local variables
    variables_json = (
        ENV_DATASETS_PATH / dataset_path.name / "pipelines" / variables_filename
    )
    variables_json.unlink()
    assert not variables_json.exists()

    # Set remote variables to some value
    remote_vars = {dataset_path.name: {"test-var": f"val-{uuid.uuid4()}"}}
    mocker.patch(
        "scripts.deploy_dag.get_airflow_var_from_composer_env", return_value=remote_vars
    )

    # Patch remote calls
    mocker.patch("scripts.deploy_dag.run_cloud_composer_vars_import")
    mocker.patch("scripts.deploy_dag.run_gsutil_cmd")
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=2)

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )

    assert not deploy_dag.run_cloud_composer_vars_import.called


def test_resulting_vars_when_user_gets_prompted_and_chooses_remote_vars(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    variables_filename = f"{dataset_path.name}_variables.json"
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        variables_filename,
        mocker,
    )

    # Set local variables to some value
    local_vars = {dataset_path.name: {"local": str(uuid.uuid4())}}
    variables_json = (
        ENV_DATASETS_PATH / dataset_path.name / "pipelines" / variables_filename
    )
    variables_json.write_text(json.dumps(local_vars))

    # Set remote variables to a different value
    remote_vars = {dataset_path.name: {"remote_var": f"remote-val-{uuid.uuid4()}"}}
    mocker.patch(
        "scripts.deploy_dag.get_airflow_var_from_composer_env", return_value=remote_vars
    )

    # Patch remote calls
    mocker.patch("scripts.deploy_dag.run_cloud_composer_vars_import")
    mocker.patch("scripts.deploy_dag.run_gsutil_cmd")
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=2)

    # User chooses to use remote variable
    mocker.patch(
        "scripts.deploy_dag.prompt_strategy_for_local_and_remote_vars", return_value="r"
    )
    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )
    assert not deploy_dag.run_cloud_composer_vars_import.called
    assert json.loads(variables_json.read_text()) == remote_vars


def test_resulting_vars_when_user_gets_prompted_and_chooses_local_vars(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    variables_filename = f"{dataset_path.name}_variables.json"
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        variables_filename,
        mocker,
    )

    # Set local variables to some value
    local_vars = {dataset_path.name: {"local": str(uuid.uuid4())}}
    variables_json = (
        ENV_DATASETS_PATH / dataset_path.name / "pipelines" / variables_filename
    )
    variables_json.write_text(json.dumps(local_vars))

    # Set remote variables to a different value
    remote_vars = {dataset_path.name: {"remote_var": f"remote-val-{uuid.uuid4()}"}}
    mocker.patch(
        "scripts.deploy_dag.get_airflow_var_from_composer_env", return_value=remote_vars
    )

    # Patch remote calls
    mocker.patch("scripts.deploy_dag.run_cloud_composer_vars_import")
    mocker.patch("scripts.deploy_dag.run_gsutil_cmd")
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=2)

    # User chooses to use local variable
    mocker.patch(
        "scripts.deploy_dag.prompt_strategy_for_local_and_remote_vars", return_value="l"
    )
    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )
    deploy_dag.run_cloud_composer_vars_import.assert_called_once()
    assert json.loads(variables_json.read_text()) == local_vars


def test_resulting_vars_when_user_gets_prompted_and_chooses_to_merge_local_and_remote_vars(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    variables_filename = f"{dataset_path.name}_variables.json"
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        variables_filename,
        mocker,
    )

    # Set local variables to some value
    local_vars = {dataset_path.name: {"local": str(uuid.uuid4())}}
    variables_json = (
        ENV_DATASETS_PATH / dataset_path.name / "pipelines" / variables_filename
    )
    variables_json.write_text(json.dumps(local_vars))

    # Set remote variables to a different value
    remote_vars = {dataset_path.name: {"remote_var": f"remote-val-{uuid.uuid4()}"}}
    mocker.patch(
        "scripts.deploy_dag.get_airflow_var_from_composer_env", return_value=remote_vars
    )

    # Patch remote calls
    mocker.patch("scripts.deploy_dag.run_cloud_composer_vars_import")
    mocker.patch("scripts.deploy_dag.run_gsutil_cmd")
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=2)

    # User chooses to merge local and remote variables
    mocker.patch(
        "scripts.deploy_dag.prompt_strategy_for_local_and_remote_vars", return_value="m"
    )
    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )
    deploy_dag.run_cloud_composer_vars_import.assert_called_once()
    assert json.loads(variables_json.read_text()) == deploy_dag.merge_nested_dicts(
        remote_vars, local_vars
    )


def test_script_errors_out_when_deploying_airflow2_dag_to_airflow1_env(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    mocker.patch("scripts.deploy_dag.get_dag_airflow_version", return_value=2)
    mocker.patch("scripts.deploy_dag.composer_airflow_version", return_value=1)

    with pytest.raises(Exception):
        deploy_dag.main(
            env_path=ENV_PATH,
            dataset_id=dataset_path.name,
            pipeline=pipeline_path.name,
            composer_env="test-env",
            composer_bucket="test-bucket",
            composer_region="test-region",
        )


def test_script_without_pipeline_arg_deploys_all_pipelines_under_the_dataset(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    pipeline_path_2: pathlib.Path,
    env: str,
    mocker,
):
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    setup_dag_and_variables(
        dataset_path,
        pipeline_path_2,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    airflow_version = 2
    mocker.patch("scripts.deploy_dag.check_and_configure_airflow_variables")
    mocker.patch(
        "scripts.deploy_dag.composer_airflow_version", return_value=airflow_version
    )
    mocker.patch("scripts.deploy_dag.copy_custom_callables_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.copy_generated_dag_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.check_airflow_version_compatibility")

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
        pipeline=None,
    )

    pipelines_dir = ENV_DATASETS_PATH / dataset_path.name / "pipelines"
    deploy_dag.check_airflow_version_compatibility.assert_any_call(
        pipelines_dir / pipeline_path.name, airflow_version
    )
    deploy_dag.check_airflow_version_compatibility.assert_any_call(
        pipelines_dir / pipeline_path_2.name, airflow_version
    )


def test_script_with_pipeline_arg_deploys_only_that_pipeline(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    pipeline_path_2: pathlib.Path,
    env: str,
    mocker,
):
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    setup_dag_and_variables(
        dataset_path,
        pipeline_path_2,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    airflow_version = 2
    mocker.patch("scripts.deploy_dag.check_and_configure_airflow_variables")
    mocker.patch(
        "scripts.deploy_dag.composer_airflow_version", return_value=airflow_version
    )
    mocker.patch("scripts.deploy_dag.copy_custom_callables_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.copy_generated_dag_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.check_airflow_version_compatibility")

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path_2.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )

    deploy_dag.check_airflow_version_compatibility.assert_called_once()


def test_script_with_pipeline_arg_deploys_without_gcs_bucket_param(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    airflow_version = 2
    mocker.patch("scripts.deploy_dag.check_and_configure_airflow_variables")
    mocker.patch(
        "scripts.deploy_dag.composer_airflow_version", return_value=airflow_version
    )
    mocker.patch("scripts.deploy_dag.copy_custom_callables_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.copy_generated_dag_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.check_airflow_version_compatibility")
    mocker.patch("scripts.deploy_dag.get_composer_bucket")

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket=None,
        composer_region="test-region",
    )

    deploy_dag.get_composer_bucket.assert_called_once()
    deploy_dag.check_airflow_version_compatibility.assert_called_once()


def test_script_copy_files_in_data_folder_to_composer_with_folder_created(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    data_folder = pipeline_path / "data"
    data_folder.mkdir(parents=True)
    (data_folder / "test_file.txt").touch()
    assert data_folder.exists() and data_folder.is_dir() and any(data_folder.iterdir())

    airflow_version = 2
    mocker.patch("scripts.deploy_dag.check_and_configure_airflow_variables")
    mocker.patch(
        "scripts.deploy_dag.composer_airflow_version", return_value=airflow_version
    )
    mocker.patch("scripts.deploy_dag.copy_custom_callables_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.copy_generated_dag_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.check_airflow_version_compatibility")
    mocker.patch("scripts.deploy_dag.copy_data_folder_to_composer_bucket")

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="tests-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )

    deploy_dag.copy_data_folder_to_composer_bucket.assert_called_once()


def test_script_copy_files_in_data_folder_to_composer_data_folder_without_folder(
    dataset_path: pathlib.Path,
    pipeline_path: pathlib.Path,
    env: str,
    mocker,
):
    setup_dag_and_variables(
        dataset_path,
        pipeline_path,
        env,
        f"{dataset_path.name}_variables.json",
        mocker,
    )

    airflow_version = 2
    mocker.patch("scripts.deploy_dag.check_and_configure_airflow_variables")
    mocker.patch(
        "scripts.deploy_dag.composer_airflow_version", return_value=airflow_version
    )
    mocker.patch("scripts.deploy_dag.copy_custom_callables_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.copy_generated_dag_to_airflow_dags_folder")
    mocker.patch("scripts.deploy_dag.check_airflow_version_compatibility")
    mocker.patch("scripts.deploy_dag.copy_data_folder_to_composer_bucket")

    deploy_dag.main(
        env_path=ENV_PATH,
        dataset_id=dataset_path.name,
        pipeline=pipeline_path.name,
        composer_env="test-env",
        composer_bucket="test-bucket",
        composer_region="test-region",
    )

    deploy_dag.copy_data_folder_to_composer_bucket.assert_not_called()


def test_script_without_composer_env_or_region_fails(env: str):
    with pytest.raises(subprocess.CalledProcessError):
        # No --composer-env parameter
        subprocess.check_call(
            [
                "python",
                "scripts/deploy_dag.py",
                "--dataset",
                "some_test_dataset",
                "--env",
                env,
                "--composer-bucket",
                "us-east4-composer-env-bucket",
                "--composer-region",
                "us-east4",
            ],
            cwd=deploy_dag.PROJECT_ROOT,
        )

    with pytest.raises(subprocess.CalledProcessError):
        # No --composer-region parameter
        subprocess.check_call(
            [
                "python",
                "scripts/deploy_dag.py",
                "--dataset",
                "some_test_dataset",
                "--env",
                env,
                "--composer-env",
                "test-composer-env",
                "--composer-bucket",
                "us-east4-composer-env-bucket",
            ],
            cwd=deploy_dag.PROJECT_ROOT,
        )
