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


import pathlib
import random
import re
import shutil
import subprocess
import tempfile
import uuid

import pytest
from ruamel import yaml

from scripts import generate_terraform

PROJECT_ROOT = generate_terraform.PROJECT_ROOT
FILE_PATHS = {
    "dataset": PROJECT_ROOT / "samples" / "dataset.yaml",
    "pipeline": PROJECT_ROOT / "samples" / "pipeline.yaml",
    "license": PROJECT_ROOT / "templates" / "airflow" / "license_header.py.jinja2",
}

ENV_PATH = PROJECT_ROOT / ".test"
ENV_DATASETS_PATH = ENV_PATH / "datasets"

yaml = yaml.YAML(typ="safe")


@pytest.fixture
def dataset_path():
    with tempfile.TemporaryDirectory(
        dir=generate_terraform.DATASETS_PATH, suffix="_dataset"
    ) as dir_path:
        try:
            yield pathlib.Path(dir_path)
        finally:
            shutil.rmtree(dir_path, ignore_errors=True)


@pytest.fixture
def pipeline_path(dataset_path, suffix="_pipeline"):
    pipelines_dir = dataset_path / "pipelines"
    pipelines_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=pipelines_dir, suffix=suffix) as dir_path:
        try:
            yield pathlib.Path(dir_path)
        finally:
            shutil.rmtree(dir_path)


@pytest.fixture
def project_id() -> str:
    return "test-gcp-project-id"


@pytest.fixture
def bucket_name_prefix() -> str:
    return "1234-zyxwvu"


@pytest.fixture
def region() -> str:
    return "us-east4"


@pytest.fixture
def impersonating_acct() -> str:
    return "test-impersonator@project.iam.gserviceaccount.com"


@pytest.fixture
def gcs_bucket_resource() -> dict:
    return {
        "type": "storage_bucket",
        "name": "{{ friendly_project_id }}.{{ dataset_id }}",
    }


@pytest.fixture
def bq_table_resource() -> dict:
    return {
        "type": "bigquery_table",
        "table_id": "test_bq_table",
        "schema": [
            {"name": "test_col_string", "type": "STRING"},
            {"name": "test_col_int", "type": "INT64"},
            {"name": "test_col_numeric", "type": "NUMERIC"},
            {"name": "test_col_datetime", "type": "DATETIME"},
            {"name": "test_col_struct", "type": "STRUCT"},
        ],
    }


@pytest.fixture
def tf_state_bucket() -> str:
    return "test-terraform-state-bucket"


@pytest.fixture
def tf_state_prefix() -> str:
    return "test/terraform/state"


@pytest.fixture
def env() -> str:
    return "test"


def set_dataset_ids_in_config_files(
    dataset_path: pathlib.Path, pipeline_path: pathlib.Path
):
    shutil.copyfile(FILE_PATHS["dataset"], dataset_path / "pipelines" / "dataset.yaml")
    shutil.copyfile(FILE_PATHS["pipeline"], pipeline_path / "pipeline.yaml")

    dataset_config = yaml.load(dataset_path / "pipelines" / "dataset.yaml")
    dataset_config["dataset"]["name"] = dataset_path.name

    for resource in dataset_config["resources"]:
        if resource["type"] == "bigquery_dataset":
            resource["dataset_id"] = dataset_path.name

    yaml.dump(dataset_config, dataset_path / "pipelines" / "dataset.yaml")

    pipeline_config = yaml.load(pipeline_path / "pipeline.yaml")
    for resource in pipeline_config["resources"]:
        if resource["type"] == "bigquery_table":
            resource["dataset_id"] = dataset_path.name

    yaml.dump(pipeline_config, pipeline_path / "pipeline.yaml")


def test_tf_templates_exist():
    for _, filepath in generate_terraform.TEMPLATE_PATHS.items():
        assert filepath.exists()


def test_main_generates_tf_files(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
    tf_state_bucket,
    tf_state_prefix,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        tf_state_bucket,
        tf_state_prefix,
        format_code=False,
    )

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        assert (path_prefix / "provider.tf").exists()
        assert (path_prefix / f"{dataset_path.name}_dataset.tf").exists()
        assert (path_prefix / f"{pipeline_path.name}_pipeline.tf").exists()
        assert (path_prefix / "variables.tf").exists()

    assert not (
        generate_terraform.DATASETS_PATH
        / dataset_path.name
        / "infra"
        / "terraform.tfvars"
    ).exists()

    assert (
        ENV_DATASETS_PATH / dataset_path.name / "infra" / "terraform.tfvars"
    ).exists()

    assert not (
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra" / "backend.tf"
    ).exists()

    assert (ENV_DATASETS_PATH / dataset_path.name / "infra" / "backend.tf").exists()


def test_main_without_tf_remote_state_generates_tf_files_except_backend_tf(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
        format_code=False,
    )

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        assert (path_prefix / "provider.tf").exists()
        assert (path_prefix / f"{dataset_path.name}_dataset.tf").exists()
        assert (path_prefix / f"{pipeline_path.name}_pipeline.tf").exists()
        assert (path_prefix / "variables.tf").exists()
        assert not (path_prefix / "backend.tf").exists()

    assert not (
        generate_terraform.DATASETS_PATH
        / dataset_path.name
        / "infra"
        / "terraform.tfvars"
    ).exists()

    assert (
        ENV_DATASETS_PATH / dataset_path.name / "infra" / "terraform.tfvars"
    ).exists()


pipeline_path_2 = pipeline_path


def test_main_with_multiple_pipelines(
    dataset_path,
    pipeline_path,
    pipeline_path_2,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
    tf_state_bucket,
    tf_state_prefix,
):
    assert pipeline_path.name != pipeline_path_2.name

    shutil.copyfile(FILE_PATHS["dataset"], dataset_path / "pipelines" / "dataset.yaml")
    shutil.copyfile(FILE_PATHS["pipeline"], pipeline_path / "pipeline.yaml")
    shutil.copyfile(FILE_PATHS["pipeline"], pipeline_path_2 / "pipeline.yaml")

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        tf_state_bucket,
        tf_state_prefix,
        format_code=False,
    )

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        assert (path_prefix / "provider.tf").exists()
        assert (path_prefix / f"{dataset_path.name}_dataset.tf").exists()
        assert (path_prefix / f"{pipeline_path.name}_pipeline.tf").exists()
        assert (path_prefix / f"{pipeline_path_2.name}_pipeline.tf").exists()
        assert (path_prefix / "variables.tf").exists()

    assert not (
        generate_terraform.DATASETS_PATH
        / dataset_path.name
        / "infra"
        / "terraform.tfvars"
    ).exists()

    assert (
        ENV_DATASETS_PATH / dataset_path.name / "infra" / "terraform.tfvars"
    ).exists()

    assert not (
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra" / "backend.tf"
    ).exists()

    assert (ENV_DATASETS_PATH / dataset_path.name / "infra" / "backend.tf").exists()


def test_main_with_multiple_bq_dataset_ids(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    # First, declare an additional custom BQ dataset in dataset.yaml
    another_dataset_id = "another_dataset"
    assert another_dataset_id != dataset_path.name

    dataset_config = yaml.load(dataset_path / "pipelines" / "dataset.yaml")
    dataset_config["resources"].append(
        {"type": "bigquery_dataset", "dataset_id": another_dataset_id}
    )
    yaml.dump(dataset_config, dataset_path / "pipelines" / "dataset.yaml")

    # Then, add a BQ table under the additional BQ dataset
    pipeline_config = yaml.load(pipeline_path / "pipeline.yaml")
    pipeline_config["resources"].append(
        {
            "type": "bigquery_table",
            "table_id": "another_table",
            "dataset_id": another_dataset_id,
        }
    )
    yaml.dump(pipeline_config, pipeline_path / "pipeline.yaml")

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
        format_code=False,
    )

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        assert (path_prefix / f"{dataset_path.name}_dataset.tf").exists()
        assert (path_prefix / f"{pipeline_path.name}_pipeline.tf").exists()

    # Match the "google_bigquery_dataset" properties, i.e. any lines between the
    # curly braces, in the *_dataset.tf file
    regexp = r"\"google_bigquery_dataset\" \"" + r"[A-Za-z0-9_]+" + r"\" \{(.*?)\}"
    bq_dataset_tf_string = re.compile(regexp, flags=re.MULTILINE | re.DOTALL)

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        matches = bq_dataset_tf_string.findall(
            (path_prefix / f"{dataset_path.name}_dataset.tf").read_text()
        )

        dataset_ids = set()
        for match in matches:
            result = re.search(r"dataset_id\s+\=\s+\"([A-Za-z0-9_]+)\"", match)
            assert result.group(1)
            dataset_ids.add(result.group(1))

        # Assert that the dataset_ids are unique
        assert len(dataset_ids) == len(matches)

        assert another_dataset_id in dataset_ids
        assert dataset_path.name in dataset_ids


def test_dataset_without_any_pipelines(
    dataset_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
    tf_state_bucket,
    tf_state_prefix,
):
    (dataset_path / "pipelines").mkdir(parents=True)
    shutil.copyfile(FILE_PATHS["dataset"], dataset_path / "pipelines" / "dataset.yaml")

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        tf_state_bucket,
        tf_state_prefix,
        format_code=False,
    )

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        assert (path_prefix / "provider.tf").exists()
        assert (path_prefix / f"{dataset_path.name}_dataset.tf").exists()

    assert not (
        generate_terraform.DATASETS_PATH
        / dataset_path.name
        / "infra"
        / "terraform.tfvars"
    ).exists()

    assert (
        ENV_DATASETS_PATH / dataset_path.name / "infra" / "terraform.tfvars"
    ).exists()

    assert not (
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra" / "backend.tf"
    ).exists()

    assert (ENV_DATASETS_PATH / dataset_path.name / "infra" / "backend.tf").exists()


def test_dataset_path_does_not_exist(
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
    tf_state_bucket,
    tf_state_prefix,
):
    with pytest.raises(FileNotFoundError):
        generate_terraform.main(
            "non_existing_dir",
            project_id,
            bucket_name_prefix,
            region,
            impersonating_acct,
            env,
            tf_state_bucket,
            tf_state_prefix,
        )


def test_generated_tf_files_contain_license_headers(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
    tf_state_bucket,
    tf_state_prefix,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        tf_state_bucket,
        tf_state_prefix,
        format_code=False,
    )

    license_header = pathlib.Path(
        generate_terraform.TEMPLATE_PATHS["license"]
    ).read_text()

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        assert (path_prefix / "provider.tf").read_text().count(license_header) == 1
        assert (path_prefix / f"{dataset_path.name}_dataset.tf").read_text().count(
            license_header
        ) == 1
        assert (path_prefix / f"{pipeline_path.name}_pipeline.tf").read_text().count(
            license_header
        ) == 1
        assert (path_prefix / "variables.tf").read_text().count(license_header) == 1

    assert (
        ENV_DATASETS_PATH / dataset_path.name / "infra" / "terraform.tfvars"
    ).read_text().count(license_header) == 1

    assert (
        ENV_DATASETS_PATH / dataset_path.name / "infra" / "backend.tf"
    ).read_text().count(license_header) == 1


def test_dataset_tf_file_contains_description_when_specified(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
        format_code=False,
    )

    config = yaml.load(open(dataset_path / "pipelines" / "dataset.yaml"))
    bq_dataset = next(
        (r for r in config["resources"] if r["type"] == "bigquery_dataset"), None
    )
    assert bq_dataset
    assert bq_dataset["description"]

    # Match the "google_bigquery_dataset" properties, i.e. any lines between the
    # curly braces, in the *_dataset.tf file
    regexp = r"\"google_bigquery_dataset\" \"" + dataset_path.name + r"\" \{(.*?)\}"
    bq_dataset_tf_string = re.compile(regexp, flags=re.MULTILINE | re.DOTALL)

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        result = bq_dataset_tf_string.search(
            (path_prefix / f"{dataset_path.name}_dataset.tf").read_text()
        )

        assert re.search(r"dataset_id\s+\=", result.group(1))
        assert re.search(r"description\s+\=", result.group(1))


def test_bq_dataset_can_have_a_description_with_newlines_and_quotes(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    shutil.copyfile(FILE_PATHS["dataset"], dataset_path / "pipelines" / "dataset.yaml")
    shutil.copyfile(FILE_PATHS["pipeline"], pipeline_path / "pipeline.yaml")

    config = yaml.load(open(dataset_path / "pipelines" / "dataset.yaml"))

    # Get a bigquery_dataset resource and modify the `description` field
    bq_dataset = next(
        (r for r in config["resources"] if r["type"] == "bigquery_dataset"), None
    )
    test_description = 'Multiline\nstring with\n"quotes"'
    bq_dataset["description"] = test_description
    with open(dataset_path / "pipelines" / "dataset.yaml", "w") as file:
        yaml.dump(config, file)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
        format_code=False,
    )

    env_dataset_path = ENV_DATASETS_PATH / dataset_path.name
    subprocess.check_call(["terraform", "fmt"], cwd=env_dataset_path / "infra")


def test_dataset_tf_has_no_bq_dataset_description_when_unspecified(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    config = yaml.load(open(dataset_path / "pipelines" / "dataset.yaml"))

    # Get the first bigquery_dataset resource and delete the `description` field
    bq_dataset = next(
        (r for r in config["resources"] if r["type"] == "bigquery_dataset")
    )
    del bq_dataset["description"]
    with open(dataset_path / "pipelines" / "dataset.yaml", "w") as file:
        yaml.dump(config, file)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
    )

    # Match the "google_bigquery_dataset" properties, i.e. any lines between the
    # curly braces, in the *_dataset.tf file
    regexp = r"\"google_bigquery_dataset\" \"" + dataset_path.name + r"\" \{(.*?)\}"
    bq_dataset_tf_string = re.compile(regexp, flags=re.MULTILINE | re.DOTALL)

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        result = bq_dataset_tf_string.search(
            (path_prefix / f"{dataset_path.name}_dataset.tf").read_text()
        )

        assert re.search(r"dataset_id\s+\=", result.group(1))
        assert not re.search(r"description\s+\=", result.group(1))


def test_pipeline_tf_contains_optional_properties_when_specified(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
    )

    config = yaml.load(open(pipeline_path / "pipeline.yaml"))
    bq_table = next(
        (r for r in config["resources"] if r["type"] == "bigquery_table"), None
    )
    assert bq_table
    assert bq_table["description"]
    assert bq_table["time_partitioning"]
    assert bq_table["clustering"]
    assert bq_table["deletion_protection"]

    # Match the "google_bigquery_table" properties, i.e. any lines between the
    # curly braces, in the *_pipeline.tf file
    regexp = (
        r"\"google_bigquery_table\" \""
        + bq_table["dataset_id"]
        + "_"
        + bq_table["table_id"]
        + r"\" \{(.*?)^\}"
    )
    bq_table_tf_string = re.compile(regexp, flags=re.MULTILINE | re.DOTALL)

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        result = bq_table_tf_string.search(
            (path_prefix / f"{pipeline_path.name}_pipeline.tf").read_text()
        )

        assert re.search(r"table_id\s+\=", result.group(1))
        assert re.search(r"description\s+\=", result.group(1))
        assert re.search(r"time_partitioning\s+\{", result.group(1))
        assert re.search(r"clustering\s+\=", result.group(1))
        assert re.search(r"deletion_protection\s+\=", result.group(1))


def test_infra_vars_are_in_tfvars_file(
    dataset_path,
    pipeline_path,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    # Creates a .env.test.yaml file in the dataset folder and sets its contents
    env_vars = {
        "infra": {
            "project_id": f"test-{uuid.uuid4()}",
            "region": "test_region",
            "env": env,
        }
    }
    yaml.dump(env_vars, dataset_path / f".vars.{env}.yaml")

    generate_terraform.main(
        dataset_path.name,
        "",
        "",
        "",
        "",
        env,
        "",
        "",
    )

    tfvars_file = ENV_DATASETS_PATH / dataset_path.name / "infra" / "terraform.tfvars"
    assert tfvars_file.exists()

    for key, val in env_vars["infra"].items():
        # Matches the following expressions in the *.tfvars file
        #
        # key         = "value"
        # another_key = "another value"
        regexp = key + r"\s+= \"" + val + r"\""
        assert re.search(regexp, tfvars_file.read_text())


def test_infra_vars_generates_gcs_buckets_with_iam_policies(
    dataset_path,
    pipeline_path,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    test_bucket = f"bucket-{uuid.uuid4()}"

    # Replace bucket name in dataset.yaml
    dataset_config = yaml.load(dataset_path / "pipelines" / "dataset.yaml")
    for resource in dataset_config["resources"]:
        if resource["type"] == "storage_bucket":
            resource["name"] = test_bucket

    yaml.dump(dataset_config, dataset_path / "pipelines" / "dataset.yaml")

    # Creates a .env.test.yaml file in the dataset folder and sets its contents
    env_vars = {
        "infra": {
            "project_id": f"test-{uuid.uuid4()}",
            "region": "test_region",
            "env": env,
            "iam_policies": {
                "storage_buckets": {
                    test_bucket: [
                        {
                            "role": "roles/storage.objectViewer",
                            "members": ["test-user@google.com"],
                        }
                    ]
                }
            },
        }
    }
    yaml.dump(env_vars, dataset_path / f".vars.{env}.yaml")

    generate_terraform.main(
        dataset_path.name,
        "",
        "",
        "",
        "",
        env,
        "",
        "",
    )

    dataset_tf_file = dataset_path / "infra" / f"{dataset_path.name}_dataset.tf"
    assert dataset_tf_file.exists()

    regex_data_iam_block = (
        r"data \"google_iam_policy\" \"storage_bucket__" + test_bucket + r"\" \{"
    )
    assert re.search(regex_data_iam_block, dataset_tf_file.read_text())

    regex_resource_iam_block = (
        r"resource \"google_storage_bucket_iam_policy\" \"" + test_bucket + r"\" \{"
    )
    assert re.search(regex_resource_iam_block, dataset_tf_file.read_text())


def test_infra_vars_generates_bq_datasets_with_iam_policies(
    dataset_path,
    pipeline_path,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    bq_dataset = f"bq-dataset-{uuid.uuid4()}"

    # Replace bucket name in dataset.yaml
    dataset_config = yaml.load(dataset_path / "pipelines" / "dataset.yaml")
    for resource in dataset_config["resources"]:
        if resource["type"] == "bigquery_dataset":
            resource["dataset_id"] = bq_dataset

    yaml.dump(dataset_config, dataset_path / "pipelines" / "dataset.yaml")

    # Creates a .env.test.yaml file in the dataset folder and sets its contents
    env_vars = {
        "infra": {
            "project_id": f"test-{uuid.uuid4()}",
            "region": "test_region",
            "env": env,
            "iam_policies": {
                "bigquery_datasets": {
                    bq_dataset: [
                        {
                            "role": "roles/storage.objectViewer",
                            "members": ["test-user@google.com"],
                        }
                    ]
                }
            },
        }
    }
    yaml.dump(env_vars, dataset_path / f".vars.{env}.yaml")

    generate_terraform.main(dataset_path.name, "", "", "", "", env, "", "")

    dataset_tf_file = dataset_path / "infra" / f"{dataset_path.name}_dataset.tf"
    assert dataset_tf_file.exists()

    regex_data_iam_block = (
        r"data \"google_iam_policy\" \"bq_ds__" + bq_dataset + r"\" \{"
    )
    assert re.search(regex_data_iam_block, dataset_tf_file.read_text())

    regex_resource_iam_block = (
        r"resource \"google_bigquery_dataset_iam_policy\" \"" + bq_dataset + r"\" \{"
    )
    assert re.search(regex_resource_iam_block, dataset_tf_file.read_text())


def test_infra_vars_without_iam_policies_generate_tf_without_iam_policies(
    dataset_path,
    pipeline_path,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    test_bucket = f"bucket-{uuid.uuid4()}"

    # Replace bucket name in dataset.yaml
    dataset_config = yaml.load(dataset_path / "pipelines" / "dataset.yaml")
    for resource in dataset_config["resources"]:
        if resource["type"] == "storage_bucket":
            resource["name"] = test_bucket

    yaml.dump(dataset_config, dataset_path / "pipelines" / "dataset.yaml")

    # Creates a .env.test.yaml file in the dataset folder and sets its contents
    env_vars = {
        "infra": {
            "project_id": f"test-{uuid.uuid4()}",
            "region": "test_region",
            "env": env,
        }
    }
    yaml.dump(env_vars, dataset_path / f".vars.{env}.yaml")

    generate_terraform.main(
        dataset_path.name, "", "", "", "", env, "", "", format_code=False
    )

    dataset_tf_file = dataset_path / "infra" / f"{dataset_path.name}_dataset.tf"
    assert dataset_tf_file.exists()

    assert not re.search("google_iam_policy", dataset_tf_file.read_text())


def test_pipeline_tf_has_no_optional_properties_when_unspecified(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    config = yaml.load(open(pipeline_path / "pipeline.yaml"))

    # Get the first bigquery_table resource and delete the `description` field
    bq_table = next((r for r in config["resources"] if r["type"] == "bigquery_table"))
    del bq_table["description"]
    del bq_table["time_partitioning"]
    del bq_table["clustering"]
    del bq_table["deletion_protection"]
    with open(pipeline_path / "pipeline.yaml", "w") as file:
        yaml.dump(config, file)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
    )

    # Match the "google_bigquery_table" properties, i.e. any lines between the
    # curly braces, in the *_pipeline.tf file
    regexp = (
        r"\"google_bigquery_table\" \""
        + bq_table["dataset_id"]
        + "_"
        + bq_table["table_id"]
        + r"\" \{(.*?)^\}"
    )
    bq_table_tf_string = re.compile(regexp, flags=re.MULTILINE | re.DOTALL)

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        result = bq_table_tf_string.search(
            (path_prefix / f"{pipeline_path.name}_pipeline.tf").read_text()
        )

        assert re.search(r"table_id\s+\=", result.group(1))
        assert not re.search(r"description\s+\=", result.group(1))
        assert not re.search(r"time_partitioning\s+\{", result.group(1))
        assert not re.search(r"clustering\s+\=", result.group(1))
        assert not re.search(r"deletion_protection\s+\=", result.group(1))


def test_bq_table_can_have_a_description_with_newlines_and_quotes(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    config = yaml.load(open(pipeline_path / "pipeline.yaml"))

    # Get a bigquery_table resource and modify the `description` field
    bq_table = next(
        (r for r in config["resources"] if r["type"] == "bigquery_table"), None
    )
    bq_table["description"] = 'Multiline\nstring with\n"quotes"'
    with open(pipeline_path / "pipeline.yaml", "w") as file:
        yaml.dump(config, file)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
        format_code=False,
    )

    env_dataset_path = ENV_DATASETS_PATH / dataset_path.name
    subprocess.check_call(["terraform", "fmt"], cwd=env_dataset_path / "infra")


def test_bq_table_name_starts_with_digits_but_tf_resource_name_does_not(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    config = yaml.load(open(pipeline_path / "pipeline.yaml"))
    table_name_starting_with_digit = f"{str(random.randint(0, 9))}_table"

    # In the YAML config, set the BigQuery table name to start with a digit
    bq_table = next(
        (r for r in config["resources"] if r["type"] == "bigquery_table"), None
    )
    bq_table["table_id"] = table_name_starting_with_digit
    with open(pipeline_path / "pipeline.yaml", "w") as file:
        yaml.dump(config, file)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
    )

    # Match the Terraform resource name and the table_id value in the BigQuery
    # table's resource definition. As a concrete example, substrings in
    # ALL_CAPS are matched below:
    #
    # resource "google_bigquery_table" "RESOURCE_NAME_STARTING_WITH_NONDIGIT" {
    #   description = ""
    #   table_id    = "TABLE_NAME_STARTING_WITH_DIGIT"
    # }
    tf_resource_regexp = r"\"google_bigquery_table\" \"([a-zA-Z0-9_-]+)\" .*?"
    table_id_regexp = r"table_id\s+\= \"(.*?)\"\n"
    matcher = re.compile(
        tf_resource_regexp + table_id_regexp,
        flags=re.MULTILINE | re.DOTALL,
    )

    for path_prefix in (
        ENV_DATASETS_PATH / dataset_path.name / "infra",
        generate_terraform.DATASETS_PATH / dataset_path.name / "infra",
    ):
        result = matcher.search(
            (path_prefix / f"{pipeline_path.name}_pipeline.tf").read_text()
        )

        tf_resource_name = result.group(1)
        table_id = result.group(2)

        assert table_id == table_name_starting_with_digit
        assert not tf_resource_name[0].isdigit()
        assert table_id[0].isdigit()
        assert table_id in tf_resource_name


def test_bucket_names_must_not_contain_dots_and_google():
    for name in (
        "test.bucket.name",
        "google-bucket",
        "google.bucket.name",
        "g00gle",
        "googl3",
    ):
        with pytest.raises(ValueError):
            generate_terraform.validate_bucket_name(name)


def test_bucket_names_must_use_hyphens_instead_of_underscores():
    for name in (
        "test_underscore",
        "test-bucket_with-underscore",
    ):
        with pytest.raises(ValueError):
            generate_terraform.validate_bucket_name(name)


def test_bucket_prefixes_must_use_hyphens_instead_of_underscores(
    dataset_path,
    project_id,
    region,
    impersonating_acct,
    env,
    tf_state_bucket,
    tf_state_prefix,
):
    for prefix in (
        "test_prefix",
        "test-hyphens_and_underscores",
    ):
        with pytest.raises(ValueError):
            generate_terraform.main(
                dataset_path.name,
                project_id,
                prefix,
                region,
                impersonating_acct,
                env,
                tf_state_bucket,
                tf_state_prefix,
                format_code=False,
            )


def test_validation_on_generated_tf_files_in_dot_env_dir(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
        format_code=False,
    )
    env_dataset_path = ENV_DATASETS_PATH / dataset_path.name

    subprocess.check_call(["terraform", "init"], cwd=env_dataset_path / "infra")
    subprocess.check_call(["terraform", "validate"], cwd=env_dataset_path / "infra")


def test_validation_on_generated_tf_files_in_project_dir(
    dataset_path,
    pipeline_path,
    project_id,
    bucket_name_prefix,
    region,
    impersonating_acct,
    env,
):
    set_dataset_ids_in_config_files(dataset_path, pipeline_path)

    generate_terraform.main(
        dataset_path.name,
        project_id,
        bucket_name_prefix,
        region,
        impersonating_acct,
        env,
        None,
        None,
        format_code=False,
    )
    project_dataset_path = generate_terraform.DATASETS_PATH / dataset_path.name

    subprocess.check_call(["terraform", "init"], cwd=(project_dataset_path / "infra"))
    subprocess.check_call(
        ["terraform", "validate"], cwd=(project_dataset_path / "infra")
    )
