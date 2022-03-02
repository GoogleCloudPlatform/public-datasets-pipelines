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
    composer_bucket: str,
    composer_region: str,
    pipeline: str = None,
):
    print("\n========== AIRFLOW VARIABLES ==========")
    copy_variables_to_airflow_data_folder(env_path, dataset_id, composer_bucket)
    import_variables_to_airflow_env(
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


def run_gsutil_cmd(args: typing.List[str], cwd: pathlib.Path):
    subprocess.check_call(["gsutil"] + args, cwd=cwd)


def copy_variables_to_airflow_data_folder(
    env_path: pathlib.Path,
    dataset_id: str,
    composer_bucket: str = None,
):
    """
    [remote]
    gsutil cp {DATASET_ID}_variables.json gs://{COMPOSER_BUCKET}/data/variables/{filename}...
    cd .{ENV}/datasets or .{ENV}/datasets/{dataset_id}
    """
    cwd = env_path / "datasets" / dataset_id / "pipelines"
    filename = f"{dataset_id}_variables.json"
    gcs_uri = f"gs://{composer_bucket}/data/variables/{filename}"
    print(
        "\nCopying variables JSON file into Cloud Composer data folder\n\n"
        f"  Source:\n  {cwd / filename}\n\n"
        f"  Destination:\n  {gcs_uri}\n"
    )
    run_gsutil_cmd(["cp", filename, gcs_uri], cwd=cwd)


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


def import_variables_to_airflow_env(
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

    print(f"\nImporting Airflow variables from {gcs_uri} ({airflow_path})...\n")
    run_cloud_composer_vars_import(composer_env, composer_region, airflow_path, cwd=cwd)


def copy_generated_dag_to_airflow_dags_folder(
    env_path: pathlib.Path,
    dataset_id: str,
    pipeline_id: str,
    composer_bucket: str = None,
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
    composer_bucket: str = None,
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
        required=True,
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

    if not args.composer_bucket:
        raise ValueError(
            "Argument `-b|--composer-bucket` (Composer bucket name) not specified"
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
