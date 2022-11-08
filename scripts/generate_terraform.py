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
import pathlib
import subprocess
import typing

import jinja2
from ruamel import yaml

CURRENT_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_PATH.parent
DATASETS_PATH = PROJECT_ROOT / "datasets"
TEMPLATES_PATH = PROJECT_ROOT / "templates" / "terraform"

TEMPLATE_PATHS = {
    "storage_bucket": TEMPLATES_PATH / "google_storage_bucket.tf.jinja2",
    "bigquery_dataset": TEMPLATES_PATH / "google_bigquery_dataset.tf.jinja2",
    "bigquery_table": TEMPLATES_PATH / "google_bigquery_table.tf.jinja2",
    "license": TEMPLATES_PATH / "license_header.tf.jinja2",
    "tfvars": TEMPLATES_PATH / "terraform.tfvars.jinja2",
    "variables": TEMPLATES_PATH / "variables.tf.jinja2",
    "provider": TEMPLATES_PATH / "provider.tf.jinja2",
    "backend": TEMPLATES_PATH / "backend.tf.jinja2",
}

yaml = yaml.YAML(typ="safe")


def main(
    dataset_id: str,
    project_id: str,
    bucket_name_prefix: str,
    region: str,
    impersonating_acct: str,
    env: str,
    tf_state_bucket: str,
    tf_state_prefix: str,
    tf_apply: bool = False,
    format_code: bool = True,
):
    validate_bucket_name(bucket_name_prefix)

    env_path = PROJECT_ROOT / f".{env}"
    create_gitignored_env_path(dataset_id, env_path)

    generate_provider_tf(project_id, dataset_id, region, impersonating_acct, env_path)
    generate_backend_tf(dataset_id, tf_state_bucket, tf_state_prefix, env_path)

    dataset_config = yaml.load(
        open(DATASETS_PATH / dataset_id / "pipelines" / "dataset.yaml")
    )
    infra_vars = load_env_vars(dataset_id, env).get("infra")
    generate_dataset_tf(dataset_id, project_id, dataset_config, infra_vars, env)

    generate_all_pipelines_tf(dataset_id, project_id, env_path)

    generate_variables_tf(dataset_id, env_path)
    generate_tfvars_file(
        project_id,
        bucket_name_prefix,
        dataset_id,
        region,
        impersonating_acct,
        env_path,
        infra_vars,
    )

    if format_code and (env_path / "datasets" / dataset_id / "infra").exists():
        terraform_fmt(env_path / "datasets" / dataset_id / "infra")

    if format_code and (DATASETS_PATH / dataset_id / "infra").exists():
        terraform_fmt(DATASETS_PATH / dataset_id / "infra")

    if tf_apply:
        actuate_terraform_resources(dataset_id, env_path)


def load_env_vars(dataset_id: str, env: str) -> dict:
    env_vars_file = PROJECT_ROOT / "datasets" / dataset_id / f".vars.{env}.yaml"
    return yaml.load(open(env_vars_file)) if env_vars_file.exists() else {}


def generate_provider_tf(
    project_id: str,
    dataset_id: str,
    region: str,
    impersonating_acct: str,
    env_path: pathlib.Path,
):
    contents = apply_substitutions_to_template(
        TEMPLATE_PATHS["provider"],
        {
            "project_id": project_id,
            "region": region,
            "impersonating_acct": impersonating_acct,
        },
    )

    create_file_in_dir_tree(dataset_id, contents, "provider.tf", env_path)


def generate_backend_tf(
    dataset_id: str, tf_state_bucket: str, tf_state_prefix: str, env_path: pathlib.Path
):
    if not tf_state_bucket:
        return

    contents = apply_substitutions_to_template(
        TEMPLATE_PATHS["backend"],
        {
            "tf_state_bucket": tf_state_bucket,
            "tf_state_prefix": tf_state_prefix,
        },
    )

    create_file_in_dir_tree(
        dataset_id, contents, "backend.tf", env_path, use_project_dir=False
    )


def generate_dataset_tf(
    dataset_id: str,
    project_id: str,
    config: dict,
    infra_vars: typing.Union[dict, None],
    env: str,
):
    if infra_vars:
        subs = infra_vars
    else:
        subs = {"project_id": project_id, "dataset_id": dataset_id, "env": env}

    if not config["resources"]:
        return

    contents = ""
    for resource in config["resources"]:
        if resource.get("dataset_id"):
            _subs = {**subs, **{"dataset_id": resource["dataset_id"]}}
        else:
            _subs = subs
        contents += tf_resource_contents(resource, {**resource, **_subs})

    create_file_in_dir_tree(
        dataset_id, contents, f"{dataset_id}_dataset.tf", PROJECT_ROOT / f".{env}"
    )


def generate_all_pipelines_tf(dataset_id: str, project_id: str, env_path: pathlib.Path):
    pipeline_paths = list_subdirs(DATASETS_PATH / dataset_id / "pipelines")

    for pipeline_path in pipeline_paths:
        pipeline_config = yaml.load(open(pipeline_path / "pipeline.yaml"))
        generate_pipeline_tf(
            dataset_id, project_id, pipeline_path.name, pipeline_config, env_path
        )


def generate_pipeline_tf(
    dataset_id: str,
    project_id: str,
    pipeline_id: str,
    config: dict,
    env_path: pathlib.Path,
):
    subs = {"project_id": project_id, "dataset_id": dataset_id}

    if not config["resources"]:
        return

    contents = ""
    for resource in config["resources"]:
        contents += tf_resource_contents(resource, {**subs, **resource})

    create_file_in_dir_tree(
        dataset_id, contents, f"{pipeline_id}_pipeline.tf", env_path
    )


def generate_variables_tf(dataset_id: str, env_path: pathlib.Path):
    contents = pathlib.Path(TEMPLATE_PATHS["variables"]).read_text()
    create_file_in_dir_tree(dataset_id, contents, "variables.tf", env_path)


def generate_tfvars_file(
    project_id: str,
    bucket_name_prefix: str,
    dataset_id: str,
    region: str,
    impersonating_acct: str,
    env_path: pathlib.Path,
    infra_vars: typing.Union[dict, None],
):
    if infra_vars:
        tf_vars = infra_vars
    else:
        tf_vars = {
            "project_id": project_id,
            "bucket_name_prefix": bucket_name_prefix,
            "impersonating_acct": impersonating_acct,
            "region": region,
            "env": env_path.name.replace(".", ""),
        }

    contents = apply_substitutions_to_template(
        TEMPLATE_PATHS["tfvars"], {"tf_vars": tf_vars}
    )

    target_path = env_path / "datasets" / dataset_id / "infra" / "terraform.tfvars"
    write_to_file(contents + "\n", target_path)
    print_created_files([target_path])


def tf_resource_contents(resource: dict, subs: dict) -> str:
    if resource["type"] not in TEMPLATE_PATHS:
        raise ValueError

    template_path = TEMPLATE_PATHS[resource["type"]]
    subs = customize_template_subs(resource, subs)
    return apply_substitutions_to_template(template_path, subs)


def customize_template_subs(resource: dict, subs: dict) -> dict:
    if resource["type"] == "storage_bucket":
        subs["name"] = validate_bucket_name(resource["name"])
        subs["uniform_bucket_level_access"] = resource.get(
            "uniform_bucket_level_access"
        )
    elif resource["type"] == "bigquery_table":
        dataset_table = f"{subs['dataset_id']}_{resource['table_id']}"

        # Terraform resource names cannot start with digits, but BigQuery allows
        # table names that start with digits. We prepend `bqt_` to table names
        # that doesn't comply with Terraform's naming rule.
        if resource["table_id"][0].isdigit():
            subs["tf_resource_name"] = f"bqt_{dataset_table}"
        else:
            subs["tf_resource_name"] = dataset_table
    return subs


def validate_bucket_name(name: str):
    if "." in name:
        raise ValueError

    # Bucket names cannot contain "google" or close misspellings, such as
    # "g00gle" as mentioned in the bucket naming guidelines:
    # https://cloud.google.com/storage/docs/naming-buckets#requirements
    mapped_name = name.replace("0", "o").replace("1", "l").replace("3", "e")
    if "google" in mapped_name.lower():
        raise ValueError(
            "Bucket names cannot contain 'google' or close misspellings, such"
            " as 'g00gle' as mentioned in the bucket naming guidelines:"
            " https://cloud.google.com/storage/docs/naming-buckets#requirements"
        )

    # We use the convention where hyphens are used for bucket names instead of
    # underscores.
    if "_" in mapped_name:
        raise ValueError("Use hyphens over underscores for bucket names")

    return name


def uppercase_bq_schema_types(schema: list) -> list:
    return [{"name": col["name"], "type": col["type"].upper()} for col in schema]


def create_gitignored_env_path(dataset_id: str, env_path: pathlib.Path):
    if not (PROJECT_ROOT / "datasets" / dataset_id).exists():
        raise FileNotFoundError(
            f"Directory {PROJECT_ROOT / 'datasets' / dataset_id} doesn't exist"
        )
    (env_path / "datasets" / dataset_id).mkdir(parents=True, exist_ok=True)


def create_file_in_dir_tree(
    dataset_id: str,
    contents: str,
    filename: str,
    env_path: pathlib.Path,
    use_env_dir: bool = True,
    use_project_dir: bool = True,
):
    filepaths = []
    prefixes = []

    if use_env_dir:
        prefixes.append(env_path / "datasets" / dataset_id / "infra")

    if use_project_dir:
        prefixes.append(DATASETS_PATH / dataset_id / "infra")

    for prefix in prefixes:
        if not prefix.exists():
            prefix.mkdir(parents=True, exist_ok=True)

        target_path = prefix / filename
        write_to_file(contents + "\n", target_path)
        filepaths.append(target_path)

    print_created_files(filepaths)


def print_created_files(filepaths: list):
    print("\nCreated\n")
    for filepath in sorted(filepaths):
        print(f"  - {filepath.relative_to(PROJECT_ROOT)}")


def write_to_file(contents: str, filepath: pathlib.Path):
    license_header = pathlib.Path(TEMPLATE_PATHS["license"]).read_text()
    with open(filepath, "w") as file_:
        file_.write(license_header + contents.replace(license_header, ""))


def list_subdirs(path: pathlib.Path) -> typing.List[pathlib.Path]:
    """Returns a list of subdirectories"""
    subdirs = [f for f in path.iterdir() if f.is_dir() and not f.name[0] in (".", "_")]
    return subdirs


def terraform_fmt(target_file: pathlib.Path):
    subprocess.Popen(
        f"terraform fmt -write=true {target_file}",
        stdout=subprocess.DEVNULL,
        shell=True,
    ).wait()


def actuate_terraform_resources(dataset_id: str, env_path: pathlib.Path):
    cwd = env_path / "datasets" / dataset_id / "infra"
    subprocess.check_call(["terraform", "init"], cwd=cwd)
    subprocess.check_call(["terraform", "apply"], cwd=cwd)


def apply_substitutions_to_template(template: pathlib.Path, subs: dict) -> str:
    j2_template = jinja2.Template(pathlib.Path(template).read_text())
    return j2_template.render(**subs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Terraform code for infrastructure required by every dataset"
    )
    parser.add_argument(
        "-d",
        "--dataset",
        required=True,
        type=str,
        dest="dataset",
        help="The directory name of the dataset",
    )
    parser.add_argument(
        "--gcp-project-id",
        type=str,
        default="",
        dest="project_id",
        help="The Google Cloud project ID",
    )
    parser.add_argument(
        "-b",
        "--bucket-name-prefix",
        type=str,
        default="",
        dest="bucket_name_prefix",
        help="The prefix to use for GCS bucket names for global uniqueness",
    )
    parser.add_argument(
        "--tf-state-bucket",
        type=str,
        dest="tf_state_bucket",
        help="The GCS bucket name for the Terraform remote state",
    )
    parser.add_argument(
        "--tf-state-prefix",
        type=str,
        default="terraform/state",
        dest="tf_state_prefix",
        help="The GCS bucket prefix for the Terraform remote state",
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
        "-r",
        "--region",
        type=str,
        dest="region",
        help="The GCP region for the Cloud Composer environment",
    )
    parser.add_argument(
        "-i",
        "--impersonating-acct",
        dest="impersonating_acct",
        help="Use service account impersonation for Terraform",
    )
    parser.add_argument("--tf-apply", dest="tf_apply", action="store_true")

    # Usage: python scripts/generate_terraform.py -d covid19_staging -i sa@projectiam.gserviceaccount.com
    args = parser.parse_args()
    main(
        args.dataset,
        args.project_id,
        args.bucket_name_prefix,
        args.region,
        args.impersonating_acct,
        args.env,
        args.tf_state_bucket,
        args.tf_state_prefix,
        args.tf_apply,
    )
