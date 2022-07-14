import itertools
import json
import os
import pathlib

import click
import yaml

# ignore yaml alias
yaml.Dumper.ignore_aliases = lambda self, data: True
CURRENT_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_PATH.parent
DATASETS_PATH = PROJECT_ROOT / "datasets"
AIRFLOW_TEMPLATES_PATH = PROJECT_ROOT / "templates" / "airflow"


@click.command()
@click.option(
    "--dataset_id",
    prompt="Your dataset name",
    required=True,
    type=str,
    help="Dataset Name or Category that your pipeline belongs to",
)
@click.option(
    "--pipeline_id",
    "-p",
    prompt="Your pipeline name",
    required=True,
    type=str,
    help="The name of your pipeline",
)
def create_pipeline(dataset_id: str, pipeline_id: str):
    new_pipeline_path = f"{DATASETS_PATH}/{dataset_id}/pipelines/{pipeline_id}/"
    dir = os.path.dirname(new_pipeline_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        click.echo(
            f"{DATASETS_PATH}/{dataset_id}/pipelines/{pipeline_id} has been created"
        )
    else:
        click.echo(f"{new_pipeline_path} already exists")
    create_dataset_yaml(dir, dataset_id)
    create_pipeline_yaml(dir, dataset_id)


def create_dataset_yaml(dir: str, dataset_id: str):
    sample_yaml = None
    output = {}
    with open(f"{PROJECT_ROOT}/samples/dataset.yaml", "r") as sample_dataset_yaml:
        try:
            sample_yaml = yaml.safe_load(sample_dataset_yaml)
            sample_yaml["dataset"]["name"] = dataset_id
            dataset_desc = click.prompt(
                "A user-friendly description of the dataset", type=str
            )
            sample_yaml["dataset"]["description"] = dataset_desc
            output["dataset"] = sample_yaml["dataset"]
        except yaml.YAMLError as exc:
            print(exc)
    resources = []

    if click.confirm("Will you need GCP Resource(s) for your pipeline?"):
        while True:
            resource = click.prompt(
                (
                    "Which GCP Resource(s) are required for your pipeline\n"
                    "Select Resources Needed: BigQuery (BQ), Google Cloud Storage (GCS)?"
                ),
                type=click.Choice(["BQ", "GCS"], case_sensitive=False),
                default="r",
            )
            if resource == "BQ":
                bq_yaml = sample_yaml["resources"][0]
                bq_yaml["dataset_id"] = dataset_id
                bq_desc = click.prompt(
                    "A user-friendly description of the dataset", type=str
                )
                bq_yaml["description"] = bq_desc
                resources.append(bq_yaml)
            if resource == "GCS":
                gcs_yaml = sample_yaml["resources"][1]
                gcs_bucket_name = click.prompt(
                    "Your Cloud Storage Bucket Name\n"
                    "Use hyphenated syntax, e.g. `some-prefix-123`, for the names.\n"
                    "Note that bucket names must not contain 'google' or close misspellings, such as 'g00gle'.",
                    type=str,
                )
                location = click.prompt(
                    (
                        "The location of the bucket.\n"
                        "Object data for objects in the bucket resides in physical storage within this region.\n"
                        "Defaults to US."
                    ),
                    type=click.Choice(["US", "EU", "ASIA"], case_sensitive=False),
                    default="US",
                )
                gcs_yaml["name"] = gcs_bucket_name
                gcs_yaml["location"] = location
                resources.append(gcs_yaml)
            if not click.confirm("Would you like to add another resource"):
                output["resources"] = resources
                with open(f"{dir}/dataset.yaml", "w") as dataset_out:
                    yaml.dump(output, dataset_out, Dumper=yaml.Dumper, sort_keys=False)
                break


def create_pipeline_yaml(dir: str, pipeline_id: str):
    sample_yaml = None
    output = {}
    resources = []
    with open(f"{PROJECT_ROOT}/samples/pipeline.yaml", "r") as sample_pipeline_yaml:
        try:
            sample_yaml = yaml.safe_load(sample_pipeline_yaml)
            tables = click.prompt(
                "Input your BigQuery Table name(s) required for your pipeline\n"
                "If you have multiple tables, please use a comma-seperated list. (eg. table1, table2, table3)"
            )
            for table_name in tables.split(","):
                print(table_name)
                sample_yaml["resources"][0]["table_id"] = table_name
                bq_resource = sample_yaml["resources"][0]
                resources.append(bq_resource.copy())
            output["resources"] = resources

        except yaml.YAMLError as exc:
            print(exc)

    tasks = []
    with open(f"{PROJECT_ROOT}/scripts/dag_imports.json", "r") as dag_imports:
        airflow_operators = json.load(dag_imports)
        airflow_version = click.prompt(
            "Which Airflow Version does your pipeline use?",
            type=click.Choice(["1", "2"], case_sensitive=False),
        )
        if airflow_version == "1":
            operators = airflow_operators[airflow_version]
            while True:
                operator = click.prompt(
                    "Which operator would you like to add?",
                    type=click.Choice(list(operators), case_sensitive=False),
                )
                t = [task["operator"] for task in sample_yaml["dag"]["tasks"]]
                operator_idx = t.index(operator)
                tasks.append(sample_yaml["dag"]["tasks"][operator_idx])
                if not click.confirm("Would you like to add another operator?"):
                    sample_yaml["dag"]["tasks"] = tasks
                    output["dag"] = sample_yaml["dag"]
                    print(output)
                    break
        if airflow_version == "2":
            operators = airflow_operators[airflow_version]
            while True:
                operator = click.prompt(
                    "Which operator would you like to add?",
                    type=click.Choice(list(operators), case_sensitive=False),
                )
                t = [task["operator"] for task in sample_yaml["dag"]["tasks"]]
                operator_idx = t.index(operator)
                tasks.append(sample_yaml["dag"]["tasks"][operator_idx])
                if not click.confirm("Would you like to add another operator?"):
                    sample_yaml["dag"]["tasks"] = tasks
                    output["dag"] = sample_yaml["dag"]
                    print(output)
                    break


if __name__ == "__main__":
    create_pipeline()
