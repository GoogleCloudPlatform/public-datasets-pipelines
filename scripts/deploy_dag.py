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
import warnings

from ruamel import yaml

yaml = yaml.YAML(typ="safe")

CURRENT_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_PATH.parent
DATASETS_PATH = PROJECT_ROOT / "datasets"
DEFAULT_AIRFLOW_VERSION = 2


class IncompatibilityError(Exception):
    pass


def main(
    local: bool,
    env_path: pathlib.Path,
    dataset_id: str,
    pipeline: str = None,
    airflow_home: pathlib.Path = None,
    composer_env: str = None,
    composer_bucket: str = None,
    composer_region: str = None,
):
    print("\n========== AIRFLOW VARIABLES ==========")
    copy_variables_to_airflow_data_folder(
        local, env_path, dataset_id, airflow_home, composer_bucket
    )
    import_variables_to_airflow_env(
        local, env_path, dataset_id, composer_env, composer_bucket, composer_region
    )

    print("========== AIRFLOW DAGS ==========")
    if pipeline:
        pipelines = [env_path / "datasets" / dataset_id / pipeline]
    else:
        pipelines = list_subdirs(env_path / "datasets" / dataset_id)

    if local:
        runtime_airflow_version = local_airflow_version()
    else:
        runtime_airflow_version = composer_airflow_version(
            composer_env, composer_region
        )

    for pipeline_path in pipelines:
        check_airflow_version_compatibility(pipeline_path, runtime_airflow_version)

        copy_custom_callables_to_airflow_dags_folder(
            local,
            env_path,
            dataset_id,
            pipeline_path.name,
            composer_bucket,
            airflow_home,
        )

        copy_generated_dag_to_airflow_dags_folder(
            local,
            env_path,
            dataset_id,
            pipeline_path.name,
            composer_bucket,
            airflow_home,
        )


def run_gsutil_cmd(args: typing.List[str], cwd: pathlib.Path):
    subprocess.check_call(["gsutil"] + args, cwd=cwd)


def copy_variables_to_airflow_data_folder(
    local: bool,
    env_path: pathlib.Path,
    dataset_id: str,
    airflow_home: pathlib.Path = None,
    composer_bucket: str = None,
):
    """
    cd .{ENV}/datasets or .{ENV}/datasets/{dataset_id}
    """
    for cwd, filename in (
        (env_path / "datasets", "shared_variables.json"),
        (env_path / "datasets" / dataset_id, f"{dataset_id}_variables.json"),
    ):

        if not (cwd / filename).exists():
            warnings.warn(f"Airflow variables file {filename} does not exist.")
            continue

        if local:
            """
            cp {DATASET_ID}_variables.json {AIRFLOW_HOME}/data/variables/{filename}
            """
            target_path = airflow_home / "data" / "variables" / filename
            target_path.mkdir(parents=True, exist_ok=True)
            print(
                "\nCopying variables JSON file into Airflow data folder\n\n"
                f"  Source:\n  {cwd / filename}\n\n"
                f"  Destination:\n  {target_path}\n"
            )

            subprocess.check_call(["cp", "-rf", filename, str(target_path)], cwd=cwd)
        else:
            """
            [remote]
            gsutil cp {DATASET_ID}_variables.json gs://{COMPOSER_BUCKET}/data/variables/{filename}...
            """
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
    airflow_path: pathlib.Path,
    cwd: pathlib.Path,
):
    subprocess.check_call(
        [
            "gcloud",
            "beta",
            "composer",
            "environments",
            "run",
            str(composer_env),
            "--location",
            str(composer_region),
            "variables",
            "--",
            "import",
            str(airflow_path),
        ],
        cwd=cwd,
    )


def import_variables_to_airflow_env(
    local: bool,
    env_path: pathlib.Path,
    dataset_id: str,
    composer_env: str = None,
    composer_bucket: str = None,
    composer_region: str = None,
):
    """
    [local]
    airflow variables import .{ENV}/datasets/{DATASET_ID}/variables.json

    [remote]
    gcloud composer environments run COMPOSER_ENV --location COMPOSER_REGION variables -- import /home/airflow/gcs/data/variables/{DATASET_ID}_variables.json
    """
    for cwd, filename in (
        (env_path / "datasets", "shared_variables.json"),
        (env_path / "datasets" / dataset_id, f"{dataset_id}_variables.json"),
    ):
        if local:
            print(f"\nImporting Airflow variables from {cwd / filename}...\n")
            subprocess.check_call(
                ["airflow", "variables", "import", str(cwd / filename)], cwd=cwd
            )
        else:
            gcs_uri = f"gs://{composer_bucket}/data/variables/{filename}"
            airflow_path = f"/home/airflow/gcs/data/variables/{filename}"
            print(f"\nImporting Airflow variables from {gcs_uri} ({airflow_path})...\n")
            run_cloud_composer_vars_import(
                composer_env, composer_region, airflow_path, cwd=cwd
            )


def copy_generated_dag_to_airflow_dags_folder(
    local: bool,
    env_path: pathlib.Path,
    dataset_id: str,
    pipeline_id: str,
    composer_bucket: str = None,
    airflow_home: pathlib.Path = None,
):
    """
    cd {DATASET_ID}/{PIPELINE_ID}

    [local]
    cp {PIPELINE_ID}_dag.py {AIRFLOW_HOME}/dags/{DATASET_ID}__{PIPELINE_ID}_dag.py

    [remote]
    gsutil cp {PIPELINE_ID}_dag.py gs://{COMPOSER_BUCKET}/dags/{DATASET_ID}__{PIPELINE_ID}_dag.py
    """
    cwd = env_path / "datasets" / dataset_id / pipeline_id
    filename = f"{pipeline_id}_dag.py"

    if local:
        target = airflow_home / "dags" / f"{dataset_id}__{pipeline_id}_dag.py"
        print(
            f"\nCopying DAG file for pipeline `{pipeline_id}` into Airflow DAGs folder\n\n"
            f"  Source:\n  {cwd / filename}\n\n"
            f"  Destination:\n  {target}\n"
        )
        subprocess.check_call(["cp", "-rf", filename, str(target)], cwd=cwd)
    else:
        target = f"gs://{composer_bucket}/dags/{dataset_id}__{pipeline_id}_dag.py"
        print(
            f"\nCopying DAG file for pipeline `{pipeline_id}` into Cloud Composer DAG folder\n\n"
            f"  Source:\n  {cwd / filename}\n\n"
            f"  Destination:\n  {target}\n"
        )
        run_gsutil_cmd(["cp", filename, target], cwd=cwd)


def copy_custom_callables_to_airflow_dags_folder(
    local: bool,
    env_path: pathlib.Path,
    dataset_id: str,
    pipeline_id: str,
    composer_bucket: str = None,
    airflow_home: pathlib.Path = None,
):
    """
    cd {DATASET_ID}/{PIPELINE_ID}

    [local]
    mkdir -p {AIRFLOW_HOME}/dags/DATASET_ID/PIPELINE_ID/custom
    cp -rf custom {AIRFLOW_HOME}/dags/DATASET_ID/PIPELINE_ID/custom

    [remote]
    gsutil cp -r custom gs://{COMPOSER_BUCKET}/dags/{DATASET_ID}/{PIPELINE_ID}/
    """
    cwd = env_path / "datasets" / dataset_id / pipeline_id

    if not (cwd / "custom").exists():
        return

    if local:
        target_parent = airflow_home / "dags" / dataset_id / pipeline_id
        target_parent.mkdir(parents=True, exist_ok=True)
        print(
            f"\nCopying custom callables folder for pipeline `{pipeline_id}` into Airflow DAGs folder\n\n"
            f"  Source:\n  {cwd / 'custom'}\n\n"
            f"  Destination:\n  {target_parent / 'custom'}\n"
        )
        subprocess.check_call(["cp", "-rf", "custom", str(target_parent)], cwd=cwd)
    else:
        target = f"gs://{composer_bucket}/dags/{dataset_id}/{pipeline_id}/"
        print(
            f"\nCopying custom callables folder for pipeline `{pipeline_id}` into Cloud Composer DAG folder\n\n"
            f"  Source:\n  {cwd / 'custom'}\n\n"
            f"  Destination:\n  {target}\n"
        )
        run_gsutil_cmd(["cp", "-r", "custom", target], cwd=cwd)


def check_existence_of_variables_file(file_path: pathlib.Path):
    if not file_path:
        raise FileNotFoundError(f"Airflow variables file {file_path} does not exist.")


def list_subdirs(path: pathlib.Path) -> typing.List[pathlib.Path]:
    """Returns a list of subdirectories"""
    subdirs = [f for f in path.iterdir() if f.is_dir() and not f.name[0] in (".", "_")]
    return subdirs


def local_airflow_version() -> str:
    airflow_version = subprocess.run(
        ["airflow", "version"], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    return 2 if airflow_version.startswith("2") else 1


def composer_airflow_version(composer_env: str, composer_region: str) -> str:
    composer_env = json.loads(
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
    image_version = composer_env["config"]["softwareConfig"]["imageVersion"]

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
        type=str,
        dest="composer_env",
        help="The Google Cloud Composer environment name",
    )
    parser.add_argument(
        "-b",
        "--composer-bucket",
        type=str,
        dest="composer_bucket",
        help="The Google Cloud Composer bucket name",
    )
    parser.add_argument(
        "-r",
        "--composer-region",
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
    parser.add_argument(
        "-a",
        "--airflow-home",
        type=str,
        default="~/airflow",
        dest="airflow_home",
        help="pathlib.Path to the Airflow home directory (defaults to `~/airflow`)",
    )
    parser.add_argument("--local", required=False, dest="local", action="store_true")

    args = parser.parse_args()
    airflow_path = pathlib.Path(args.airflow_home).expanduser()

    if args.local:
        if not airflow_path.exists() and airflow_path.is_dir():
            raise ValueError(
                "Argument `-a|--airflow-home` must exist and be a directory"
            )
    else:
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
        local=args.local,
        env_path=PROJECT_ROOT / f".{args.env}",
        dataset_id=args.dataset,
        pipeline=args.pipeline,
        airflow_home=airflow_path,
        composer_env=args.composer_env,
        composer_bucket=args.composer_bucket,
        composer_region=args.composer_region,
    )
