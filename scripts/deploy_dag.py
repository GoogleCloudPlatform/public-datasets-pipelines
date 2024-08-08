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


import argparse
import json
import pathlib
import subprocess
import typing

import click
from google.cloud.orchestration.airflow import service_v1beta1
from ruamel import yaml

yaml = yaml.YAML(typ="safe")

CURRENT_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_PATH.parent
DATASETS_PATH = PROJECT_ROOT / "datasets"
DEFAULT_AIRFLOW_VERSION = 2


class IncompatibilityError(Exception):
    pass


def main(
    env_path: pathlib.Path,
    dataset_id: str,
    composer_env: str,
    composer_bucket: typing.Union[str, None],
    composer_region: str,
    pipeline: typing.Union[str, None],
):
    if composer_bucket is None:
        composer_bucket = get_composer_bucket(composer_env, composer_region)

    print("\n========== AIRFLOW VARIABLES ==========")
    check_and_configure_airflow_variables(
        env_path, dataset_id, composer_env, composer_bucket, composer_region
    )

    print("========== AIRFLOW DAGS ==========")
    if pipeline:
        pipelines = [env_path / "datasets" / dataset_id / "pipelines" / pipeline]
    else:
        pipelines = list_subdirs(env_path / "datasets" / dataset_id / "pipelines")

    runtime_airflow_version = composer_airflow_version(composer_env, composer_region)

    for pipeline_path in pipelines:
        check_airflow_version_compatibility(pipeline_path, runtime_airflow_version)

        data_folder = (
            DATASETS_PATH / dataset_id / "pipelines" / pipeline_path.name / "data"
        )

        if data_folder.exists() and data_folder.is_dir() and any(data_folder.iterdir()):
            copy_data_folder_to_composer_bucket(
                dataset_id,
                data_folder,
                pipeline_path.name,
                composer_bucket,
            )

        copy_custom_callables_to_airflow_dags_folder(
            env_path,
            dataset_id,
            pipeline_path.name,
            composer_bucket,
        )

        copy_generated_dag_to_airflow_dags_folder(
            env_path,
            dataset_id,
            pipeline_path.name,
            composer_bucket,
        )


def get_gcp_project() -> str:
    return subprocess.run(
        ["gcloud", "config", "get-value", "project"], text=True, capture_output=True
    ).stdout.strip()


def get_composer_bucket(
    composer_env: str,
    composer_region: str,
) -> str:
    project_id = get_gcp_project()

    # Create a client
    client = service_v1beta1.EnvironmentsClient()

    # Initialize request argument(s)
    request = service_v1beta1.GetEnvironmentRequest(
        name=f"projects/{project_id}/locations/{composer_region}/environments/{composer_env}"
    )

    # Make the request
    response = client.get_environment(request=request)

    # Handle the response
    composer_bucket = response.config.dag_gcs_prefix.replace("/dags", "").replace(
        "gs://", ""
    )
    return composer_bucket


def run_gsutil_cmd(args: typing.List[str], cwd: pathlib.Path):
    subprocess.check_call(["gsutil"] + args, cwd=cwd)


def check_and_configure_airflow_variables(
    env_path: pathlib.Path,
    dataset_id: str,
    composer_env: str,
    composer_bucket: str,
    composer_region: str,
):
    """First checks if a `.vars.[ENV].yaml` file exists in the dataset folder and if the `pipelines` key exists in that file.
    If so, copy the JSON object equivalent of `pipelines` into the variables file at `.[ENV]/datasets/pipelines/[DATASET]_variables.json`.

    Finally, upload the pipeline variables file to the Composer bucket.
    """
    cwd = env_path / "datasets" / dataset_id / "pipelines"
    vars_json_path = cwd / f"{dataset_id}_variables.json"
    env_vars_file = DATASETS_PATH / dataset_id / f".vars{env_path.name}.yaml"
    env_vars = yaml.load(open(env_vars_file)) if env_vars_file.exists() else None

    if isinstance(env_vars, dict) and "pipelines" in env_vars:
        local_vars = env_vars["pipelines"]
    elif vars_json_path.exists() and vars_json_path.stat().st_size > 0:
        with open(vars_json_path) as file_:
            local_vars = json.load(file_)
    else:
        print("No local pipeline variables found.")
        local_vars = None

    overwrite_remote_vars = compare_and_set_airflow_variables(
        local_vars,
        composer_env,
        composer_region,
        dataset_id,
        vars_json_path,
    )
    if overwrite_remote_vars:
        import_variables_to_cloud_composer(
            env_path, dataset_id, composer_env, composer_bucket, composer_region
        )


def get_airflow_var_from_composer_env(
    composer_env: str,
    composer_region: str,
    dataset_id: str,
) -> typing.Union[dict, None]:
    result = subprocess.run(
        [
            "gcloud",
            "composer",
            "environments",
            "run",
            composer_env,
            "--location",
            composer_region,
            "--project",
            get_gcp_project(),
            "variables",
            "--",
            "get",
            dataset_id,
        ],
        text=True,
        capture_output=True,
    )

    # The variable doesn't exist in the Composer environment
    if result.returncode == 1:
        print(
            f"Airflow variable `{dataset_id}` not found in Composer environment `{composer_env}`"
        )
        return
    else:
        print(
            f"Airflow variable `{dataset_id}` found in Composer environment `{composer_env}`"
        )
        return {dataset_id: json.loads(result.stdout.strip())}


def compare_and_set_airflow_variables(
    local_vars: typing.Union[dict, None],
    composer_env: str,
    composer_region: str,
    dataset_id: str,
    vars_json_path: pathlib.Path,
) -> bool:
    if not local_vars:
        print(
            f"Airflow variable `{dataset_id}` is not defined locally. Checking Cloud Composer environment for this variable.."
        )

    remote_vars = get_airflow_var_from_composer_env(
        composer_env, composer_region, dataset_id
    )
    if remote_vars is None and local_vars is None:
        print(
            "Airflow variables not defined locally and remotely. Cloud Composer variable import will be skipped.\n"
        )
        vars_to_use = None
        import_to_composer = False

    if remote_vars is not None and local_vars is not None:
        print(
            "Remote value:\n"
            f"{json.dumps(remote_vars, indent=2)}\n\n"
            "Local value:\n"
            f"{json.dumps(local_vars, indent=2)}\n"
        )
        if remote_vars == local_vars:
            print(
                "Remote and local Airflow variables are the same. Cloud Composer variable import will be skipped.\n"
            )
            vars_to_use = local_vars
            import_to_composer = False
        else:
            strategy = prompt_strategy_for_local_and_remote_vars()
            if strategy.lower() == "r":  # use remote variable (default)
                vars_to_use = remote_vars
                import_to_composer = False
            elif strategy.lower() == "l":  # use local variable
                vars_to_use = local_vars
                import_to_composer = True
            else:  # merge local and remote variables
                vars_to_use = merge_nested_dicts(remote_vars, local_vars)
                import_to_composer = True
            print(
                f"Airflow variable `{dataset_id}` is now set to\n"
                f"{json.dumps(vars_to_use, indent=2)}\n"
            )
    elif remote_vars is None and local_vars is not None:
        vars_to_use = local_vars
        import_to_composer = True
    else:  # remote vars exists and local vars is None
        print(
            f"Setting local variable `{dataset_id}` to\n"
            f"{json.dumps(remote_vars, indent=2)}\n\n"
        )
        vars_to_use = remote_vars
        import_to_composer = False

    if vars_to_use is not None:
        with open(vars_json_path, "w") as file_:
            file_.write(json.dumps(vars_to_use))

    return import_to_composer


def prompt_strategy_for_local_and_remote_vars() -> str:
    strategy = click.prompt(
        (
            "Remote and local Airflow variables are different.\n"
            "Select version to use: Merge (m), use local (l), use remote (r)?"
        ),
        type=click.Choice(["m", "l", "r"], case_sensitive=False),
        default="r",
    )
    return strategy


def merge_nested_dicts(a: dict, b: dict, path=None) -> dict:
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_nested_dicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def copy_data_folder_to_composer_bucket(
    dataset_id: str,
    data_folder: pathlib.Path,
    pipeline: str,
    composer_bucket: str,
):
    print(
        f"Data folder exists: {data_folder}.\nCopying contents into Composer bucket.."
    )
    gcs_uri = f"gs://{composer_bucket}/data/{dataset_id}/{pipeline}"
    run_gsutil_cmd(["-q", "cp", "-r", f"{data_folder}/*", gcs_uri], data_folder)

    print("Done. Files uploaded to GCS:")
    for file in data_folder.iterdir():
        print(f"  - {gcs_uri}/{file.name}")


def run_cloud_composer_vars_import(
    composer_env: str,
    composer_region: str,
    airflow_path: str,
    cwd: pathlib.Path,
):
    subprocess.check_call(
        [
            "gcloud",
            "beta",
            "composer",
            "environments",
            "run",
            composer_env,
            "--location",
            composer_region,
            "variables",
            "--",
            "import",
            airflow_path,
        ],
        cwd=cwd,
    )


def import_variables_to_cloud_composer(
    env_path: pathlib.Path,
    dataset_id: str,
    composer_env: str,
    composer_bucket: str,
    composer_region: str,
):
    """
    gcloud composer environments run COMPOSER_ENV --location COMPOSER_REGION variables -- import /home/airflow/gcs/data/variables/{DATASET_ID}_variables.json
    """
    cwd = env_path / "datasets" / dataset_id / "pipelines"
    filename = f"{dataset_id}_variables.json"
    gcs_uri = f"gs://{composer_bucket}/data/variables/{filename}"
    airflow_path = f"/home/airflow/gcs/data/variables/{filename}"

    print(
        "\nCopying variables JSON file into Cloud Composer data folder\n\n"
        f"  Source:\n  {cwd / filename}\n\n"
        f"  Destination:\n  {gcs_uri}\n"
    )
    run_gsutil_cmd(["cp", filename, gcs_uri], cwd=cwd)

    print(f"\nImporting Airflow variables from {gcs_uri} ({airflow_path})...\n")
    run_cloud_composer_vars_import(composer_env, composer_region, airflow_path, cwd=cwd)


def copy_generated_dag_to_airflow_dags_folder(
    env_path: pathlib.Path,
    dataset_id: str,
    pipeline_id: str,
    composer_bucket: str,
):
    """
    Runs the command

        gsutil cp {PIPELINE_ID}_dag.py gs://{COMPOSER_BUCKET}/dags/{DATASET_ID}__{PIPELINE_ID}_dag.py

    inside $DATASET/pipelines/$PIPELINE
    """
    cwd = env_path / "datasets" / dataset_id / "pipelines" / pipeline_id
    filename = f"{pipeline_id}_dag.py"

    target = f"gs://{composer_bucket}/dags/{dataset_id}__{pipeline_id}_dag.py"
    print(
        f"\nCopying DAG file for pipeline `{pipeline_id}` into Cloud Composer DAG folder\n\n"
        f"  Source:\n  {cwd / filename}\n\n"
        f"  Destination:\n  {target}\n"
    )
    run_gsutil_cmd(["cp", filename, target], cwd=cwd)


def copy_custom_callables_to_airflow_dags_folder(
    env_path: pathlib.Path,
    dataset_id: str,
    pipeline_id: str,
    composer_bucket: str,
):
    """
    Runs the command

        gsutil cp -r custom gs://$COMPOSER_BUCKET/dags/$DATASET/$PIPELINE_ID/

    inside $DATASET/pipelines/$PIPELINE.
    """
    cwd = env_path / "datasets" / dataset_id / "pipelines" / pipeline_id

    if not (cwd / "custom").exists():
        return

    target = f"gs://{composer_bucket}/dags/{dataset_id}/{pipeline_id}/"
    print(
        f"\nCopying custom callables folder for pipeline `{pipeline_id}` into Cloud Composer DAG folder\n\n"
        f"  Source:\n  {cwd / 'custom'}\n\n"
        f"  Destination:\n  {target}\n"
    )
    run_gsutil_cmd(["-m", "cp", "-r", "custom", target], cwd=cwd)


def check_existence_of_variables_file(file_path: pathlib.Path):
    if not file_path:
        raise FileNotFoundError(f"Airflow variables file {file_path} does not exist.")


def list_subdirs(path: pathlib.Path) -> typing.List[pathlib.Path]:
    """Returns a list of subdirectories"""
    subdirs = [f for f in path.iterdir() if f.is_dir() and not f.name[0] in (".", "_")]
    return subdirs


def composer_airflow_version(
    composer_env: str, composer_region: str
) -> typing.Literal[1, 2]:
    config = json.loads(
        subprocess.run(
            [
                "gcloud",
                "composer",
                "environments",
                "describe",
                composer_env,
                "--location",
                composer_region,
                "--format",
                "json",
            ],
            stdout=subprocess.PIPE,
        ).stdout.decode("utf-8")
    )

    # Example image version: composer-1.17.0-preview.8-airflow-2.1.1
    image_version = config["config"]["softwareConfig"]["imageVersion"]

    airflow_version = image_version.split("-airflow-")[-1]
    return 2 if airflow_version.startswith("2") else 1


def get_dag_airflow_version(config: dict) -> int:
    return config["dag"].get("airflow_version", DEFAULT_AIRFLOW_VERSION)


def check_airflow_version_compatibility(
    pipeline_path: pathlib.Path, runtime_airflow_version: int
) -> None:
    """If a DAG uses Airflow 2 operators but the runtime version uses Airflow 1,
    raise a compatibility error. On the other hand, DAGs using Airflow 1.x operators
    can still run in an Airflow 2 runtime environment via backport providers.
    """
    dag_airflow_version = get_dag_airflow_version(
        yaml.load((pipeline_path / "pipeline.yaml").read_text())
    )

    if dag_airflow_version > runtime_airflow_version:
        raise IncompatibilityError(
            f"The DAG {pipeline_path.name} uses Airflow 2, but"
            " you are deploying to an Airflow 1.x environment."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy DAGs and variables to an Airflow environment"
    )
    parser.add_argument(
        "-d",
        "--dataset",
        required=True,
        type=str,
        dest="dataset",
        help="The directory name of the dataset.",
    )
    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="dev",
        dest="env",
        help="The stage used for the resources: dev|staging|prod",
    )
    parser.add_argument(
        "-n",
        "--composer-env",
        required=True,
        type=str,
        dest="composer_env",
        help="The Google Cloud Composer environment name",
    )
    parser.add_argument(
        "-b",
        "--composer-bucket",
        required=False,
        type=str,
        dest="composer_bucket",
        help="The Google Cloud Composer bucket name",
    )
    parser.add_argument(
        "-r",
        "--composer-region",
        required=True,
        type=str,
        dest="composer_region",
        help="The region of the Google Cloud Composer environment",
    )
    parser.add_argument(
        "-p",
        "--pipeline",
        required=False,
        type=str,
        dest="pipeline",
        help="The directory name of the pipeline",
    )

    args = parser.parse_args()
    if not args.composer_env:
        raise ValueError(
            "Argument `-n|--composer-env` (Composer environment name) not specified"
        )

    if not args.composer_region:
        raise ValueError(
            "Argument `-r|--composer-region` (Composer environment region) not specified"
        )

    main(
        env_path=PROJECT_ROOT / f".{args.env}",
        dataset_id=args.dataset,
        pipeline=args.pipeline,
        composer_env=args.composer_env,
        composer_bucket=args.composer_bucket,
        composer_region=args.composer_region,
    )
