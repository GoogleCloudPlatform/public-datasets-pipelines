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
import re
import subprocess
import typing

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
<<<<<<< HEAD
    composer_bucket: None,
=======
    composer_bucket: typing.Union[str, None],
>>>>>>> main
    composer_region: str,
    pipeline: typing.Union[str, None],
):
    if composer_bucket is None:
<<<<<<< HEAD
        composer_bucket = get_composer_bucket(env_path, composer_region, composer_env)

    data_folder = DATASETS_PATH / dataset_id / "pipelines" / pipeline / "data"
    
    # Do the check if the directory exists then make the call to the copy_schema_function
    # include a check to make sure array dir is not empty either*
    if(data_folder.exists() and data_folder.is_dir()):
        copy_schema_to_composer_data_folder(dataset_id, data_folder, composer_bucket, pipeline)
=======
        composer_bucket = get_composer_bucket(composer_env, composer_region)
>>>>>>> main

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


def get_composer_bucket(
<<<<<<< HEAD
    env_path: pathlib.Path,
    composer_region: str,
    composer_env: str,
):
=======
    composer_env: str,
    composer_region: str,
) -> str:
    project_sub = subprocess.check_output(
        [
            "gcloud",
            "config",
            "get-value",
            "project",
            "--format",
            "json",
        ],
    )

    project_id = str(project_sub).split('"')[1]

>>>>>>> main
    # Create a client
    client = service_v1beta1.EnvironmentsClient()

    # Initialize request argument(s)
    request = service_v1beta1.GetEnvironmentRequest(
<<<<<<< HEAD
        name=f"projects/{env_path}/locations/{composer_region}/environments/{composer_env}"
=======
        name=f"projects/{project_id}/locations/{composer_region}/environments/{composer_env}"
>>>>>>> main
    )

    # Make the request
    response = client.get_environment(request=request)

<<<<<<< HEAD
    composer_bucket = response.config.dag_gcs_prefix
    # Handle the response
    print(composer_bucket)


# [END composer_v1beta1_generated_Environments_GetEnvironment_sync]
=======
    # Handle the response
    composer_bucket = response.config.dag_gcs_prefix.replace("/dags", "").replace(
        "gs://", ""
    )
    return composer_bucket
>>>>>>> main


def run_gsutil_cmd(args: typing.List[str], cwd: pathlib.Path):
    subprocess.check_call(["gsutil"] + args, cwd=cwd)


def copy_variables_to_airflow_data_folder(
    env_path: pathlib.Path,
    dataset_id: str,
    composer_bucket: str,
):
    """First checks if a `.vars.[ENV].yaml` file exists in the dataset folder and if the `pipelines` key exists in that file.
    If so, copy the JSON object equivalent of `pipelines` into the variables file at `.[ENV]/datasets/pipelines/[DATASET]_variables.json`.

    Finally, upload the pipeline variables file to the Composer bucket.
    """
    cwd = env_path / "datasets" / dataset_id / "pipelines"
    pipeline_vars_file = f"{dataset_id}_variables.json"
    env_vars_file = DATASETS_PATH / dataset_id / f".vars{env_path.name}.yaml"
    env_vars = yaml.load(open(env_vars_file)) if env_vars_file.exists() else {}

    if "pipelines" in env_vars:
        print(
            f"Pipeline variables found in {env_vars_file}:\n"
            f"{json.dumps(env_vars['pipelines'], indent=2)}"
        )
        with open(cwd / pipeline_vars_file, "w") as file_:
            file_.write(json.dumps(env_vars["pipelines"]))

    gcs_uri = f"gs://{composer_bucket}/data/variables/{pipeline_vars_file}"
    print(
        "\nCopying variables JSON file into Cloud Composer data folder\n\n"
        f"  Source:\n  {cwd / pipeline_vars_file}\n\n"
        f"  Destination:\n  {gcs_uri}\n"
    )
    run_gsutil_cmd(["cp", pipeline_vars_file, gcs_uri], cwd=cwd)


def copy_schema_to_composer_data_folder(
    dataset_id: str,
    data_folder: pathlib.Path,
    composer_bucket: str = None,
    pipeline: str = None,
):
    gcs_uri = f"gs://{composer_bucket}/data/{dataset_id}/pipeline/{pipeline}/data"
    schema_file_dir_pattern = "*"
    schema_file_dir = []

    #if(cwd.is_dir() and sorted(cwd.rglob(schema_file_dir_pattern))):
    schema_file_dir = sorted(data_folder.rglob(schema_file_dir_pattern))
    """
    [remote]
    gsutil cp * gs://{composer_bucket}/data/{dataset_id}/pipeline/{pipeline}
    cd .{ENV}/datasets/{dataset_id}/data
    """

    #refactor code to use - https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/45dd0b2c15821e38f0b7b511c253025fc7497ad0/scripts/generate_dag.py#L182

    if(len(schema_file_dir)>0):
        print("\nCopying files from local data folder into Cloud Composer data folder\n")                
        print("  Source:\n")
        for x in schema_file_dir:
            schema_file_names = str(x)
            print("  " + str(x) + "\n")

        print("  Destination:\n")
        for y in schema_file_dir:
            schema_file_names = str(y)
            print("  " + gcs_uri + "/" + schema_file_names.split('/data/')[1] + "\n")

        #run_gsutil_cmd(["cp", schema_file_dir_pattern , gcs_uri])
        
    else :
        print("\n No files in local data folder to copy into Cloud Composer data folder \n")       
#copy_schema_to_composer_data_folder("austin_bikeshare","us-central1-composer-demo-5e589749-bucket","bikeshare_stations")


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
