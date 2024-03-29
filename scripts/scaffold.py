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

import json
import pathlib

import click
from ruamel import yaml
from ruamel.yaml.comments import CommentedMap

yaml = yaml.YAML()
yaml.representer.ignore_aliases = lambda *data: True

CURRENT_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_PATH.parent
DATASETS_PATH = PROJECT_ROOT / "datasets"
AIRFLOW_TEMPLATES_PATH = PROJECT_ROOT / "templates" / "airflow"

license_header = (
    pathlib.Path(AIRFLOW_TEMPLATES_PATH / "license_header.py.jinja2").read_text() + "\n"
)


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
    dir = f"{DATASETS_PATH}/{dataset_id}/pipelines/{pipeline_id}/"
    new_pipeline_path = pathlib.Path(dir)
    new_pipeline_path.mkdir(parents=True, exist_ok=True)
    click.echo(
        f"\n{DATASETS_PATH}/{dataset_id}/pipelines/{pipeline_id} has been created\n"
    )

    create_dataset_yaml(dataset_id)
    create_pipeline_yaml(dir)


def create_dataset_yaml(dataset_id: str):
    dataset_yaml = {}
    sample_yaml = yaml.load((PROJECT_ROOT / "samples" / "dataset.yaml").read_text())
    sample_yaml["dataset"]["name"] = dataset_id
    sample_yaml["dataset"]["friendly_name"] = dataset_id
    dataset_desc = click.prompt("A user-friendly description of the dataset", type=str)
    sample_yaml["dataset"]["description"] = dataset_desc
    dataset_yaml["dataset"] = sample_yaml["dataset"]

    resources = []
    while True:
        resource = click.prompt(
            (
                "\nWhich GCP Resource(s) are required for your pipeline\n"
                "Select Resources Needed: BigQuery (BQ), Google Cloud Storage (GCS)?"
            ),
            type=click.Choice(["BQ", "GCS", "None"], case_sensitive=False),
            default="r",
        )
        if resource == "BQ":
            resource = next(
                res
                for res in sample_yaml["resources"]
                if res["type"] == "bigquery_dataset"
            )
            resource["dataset_id"] = dataset_id
            bq_desc = click.prompt(
                "\nA user-friendly description of the dataset", type=str
            )
            resource["description"] = bq_desc
            resources.append(resource)
        if resource == "GCS":
            resource = next(
                res
                for res in sample_yaml["resources"]
                if res["type"] == "storage_bucket"
            )
            gcs_bucket_name = click.prompt(
                "\nYour Cloud Storage Bucket Name\n"
                "Use hyphenated syntax, e.g. `some-prefix-123`, for the names.\n"
                "Note that bucket names must not contain 'google' or close misspellings, such as 'g00gle'.",
                type=str,
            )
            location = click.prompt(
                (
                    "\nThe location of the bucket.\n"
                    "Object data for objects in the bucket resides in physical storage within this region.\n"
                    "Defaults to US."
                ),
                type=click.Choice(["US", "EU", "ASIA"], case_sensitive=False),
                default="US",
            )
            resource["name"] = gcs_bucket_name
            resource["location"] = location
            resources.append(resource)
        if resource == "None":
            break
    dataset_yaml["resources"] = resources
    with open(
        f"{DATASETS_PATH}/{dataset_id}/pipelines/dataset.yaml", "w"
    ) as dataset_out:
        dataset_out.write(license_header)
        yaml.dump(CommentedMap(dataset_yaml), dataset_out)
        click.echo(
            f"\n{DATASETS_PATH}/{dataset_id}/pipelines/dataset.yaml has been created\n"
        )


def create_pipeline_yaml(dir: str):
    pipeline_yaml = {}
    resources = []
    sample_yaml = yaml.load((PROJECT_ROOT / "samples" / "pipeline.yaml").read_text())
    tables = click.prompt(
        "Input your BigQuery Table name(s) required for your pipeline\n"
        "If you have multiple tables, please use a comma-seperated list. (eg. table1, table2, table3)"
    )
    for table_name in tables.split(","):
        sample_yaml["resources"][0]["table_id"] = table_name.strip()
        bq_resource = sample_yaml["resources"][0]
        resources.append(bq_resource.copy())
    pipeline_yaml["resources"] = resources

    tasks = []
    airflow_operators = json.loads(
        (PROJECT_ROOT / "scripts" / "dag_imports.json").read_text()
    )
    operators = airflow_operators["2"]
    while True:
        operator = click.prompt(
            "\nWhich operator would you like to add?",
            type=click.Choice(list(operators), case_sensitive=False),
        )
        t = [task["operator"] for task in sample_yaml["dag"]["tasks"]]
        operator_idx = t.index(operator)
        tasks.append(sample_yaml["dag"]["tasks"][operator_idx])
        if not click.confirm("\nWould you like to add another operator?"):
            sample_yaml["dag"]["tasks"] = tasks
            pipeline_yaml["dag"] = sample_yaml["dag"]
            with open(f"{dir}/pipeline.yaml", "w") as pipeline_out:
                pipeline_out.write(license_header)
                yaml.dump(CommentedMap(pipeline_yaml), pipeline_out)
                click.echo(f"\n{dir}/pipeline.yaml has been created\n")
            break


if __name__ == "__main__":
    create_pipeline()
