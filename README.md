# Public Datasets Pipelines

Cloud-native, data pipeline architecture for onboarding datasets to the [Google Cloud Public Datasets Program](https://cloud.google.com/public-datasets).

# Overview

![public-datasets-pipelines](https://user-images.githubusercontent.com/1208372/113048389-7b8af100-9170-11eb-9156-a9c114fa6920.png)

# Requirements
- Familiarity with [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/1.10.14/concepts.html) (>=v1.10.14)
- [pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv) for creating similar Python environments via `Pipfile.lock`
- [gcloud](https://cloud.google.com/sdk/gcloud) command-line tool with Google Cloud Platform credentials configured. Instructions can be found [here](https://cloud.google.com/sdk/docs/initializing).
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) `>=v0.15.1`
- [Google Cloud Composer](https://cloud.google.com/composer/docs/concepts/overview) environment running [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/1.10.14/concepts.html) `v1.10.14,<2.0`. To create a new Cloud Composer environment, see [this guide](https://cloud.google.com/composer/docs/how-to/managing/creating).

# Other Requirements

## Google Cloud Resources

Identify what Google Cloud resources need to be provisioned for your pipelines. Some examples are

- BigQuery datasets and tables to store final, customer-facing data
- GCS bucket to store intermediate, midstream data.
- GCS bucket to store final, downstream, customer-facing data
- Sometimes, for very large datasets, you might need to provision a [Dataflow](https://cloud.google.com/dataflow/docs) job

## Authentication and Authorization

Review any connection requirements needed to fetch data from the sources. We might need any of the following:

- Authentication credentials (e.g. login credentials or API tokens)
- Authorization grants (e.g. permissions granted for us to access the data source/s)

# Environment Setup

We use Pipenv to make environment setup more deterministic and uniform across different machines.

If you haven't done so, install Pipenv using the instructions found [here](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv). Now with Pipenv installed, run the following command:

```bash
pipenv install --ignore-pipfile --dev
```

This uses the `Pipfile.lock` found in the project root and installs all the development dependencies.

Finally, initialize the Airflow database:

```bash
pipenv run airflow initdb
```

# Building Data Pipelines

Configuring, generating, and deploying data pipelines in a programmatic, standardized, and scalable way is the main purpose of this repository.

Follow the steps below to build a data pipeline for your dataset:

## 1. Create a folder hierarchy for your pipeline

```
datasets/DATASET/PIPELINE

[example]
datasets/covid19_tracking/national_testing_and_outcomes
```

where `DATASET` is the dataset name or category that your pipeline belongs to, and `PIPELINE` is your pipeline's name.

For examples of pipeline names, see [these pipeline folders in the repo](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/tree/main/datasets/covid19_tracking).

Use only underscores and alpha-numeric characters for the names.


## 2. Write your config (YAML) files

If you created a new dataset directory above, you need to create a `datasets/DATASET/dataset.yaml` config file. See this section for the `dataset.yaml` reference.

Create a `datasets/DATASET/PIPELINE/pipeline.yaml` config file for your pipeline. See this section for the `pipeline.yaml` reference.

If you'd like to get started faster, you can inspect config files that already exist in the repository and infer the patterns from there:

- [covid19_tracking](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/datasets/covid19_tracking/dataset.yaml) dataset config
- [covid19_tracking/national_testing_and_outcomes](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/datasets/covid19_tracking/national_testing_and_outcomes/pipeline.yaml) pipeline config (simple, only uses built-in Airflow operators)
- [covid19_tracking/city_level_cases_and_deaths](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/datasets/covid19_tracking/city_level_cases_and_deaths/pipeline.yaml) pipeline config (involves custom data transforms)

## 3. Generate Terraform files and actuate GCP resources

Run the following command from the project root:
```bash
$ python scripts/generate_terraform.py \
    --dataset DATASET_DIR_NAME \
    --gcp-project-id GCP_PROJECT_ID \
    --region REGION \
    [--env] dev \
    [--tf-apply] \
    [--impersonating-acct] IMPERSONATING_SERVICE_ACCT
```

This generates Terraform files (`*.tf`) in a `_terraform` directory inside that dataset. The files contain instrastructure-as-code on which GCP resources need to be actuated for use by the pipelines. If you passed in the `--tf-apply` parameter, the command will also run `terraform apply` to actuate those resources.

In addition, the command above creates a "dot" directory in the project root. The directory name is the value you pass to the `--env` parameter of the command. If no `--env` argument was passed, the value defaults to `dev` (which generates the `.dev` folder).

Consider this "dot" directory as your own dedicated space for prototyping. The files and variables created in that directory will use an isolated environment. All such directories are gitignored.

As a concrete example, the unit tests use a temporary `.test` directory as their environment.

## 4. Generate DAG (directed acyclic graph) files

Run the following command from the project root:

```bash
$ python scripts/generate_dag.py \
    --dataset DATASET_DIR \
    --pipeline PIPELINE_DIR
```

This generates a Python file that represents the DAG for the pipeline (the dot dir also gets a copy). To standardize DAG files, the resulting Python code is based entirely out of the contents in the `pipeline.yaml` config file.

## 5. Declare and set your pipeline variables

Running the command in the previous step will parse your pipeline config and inform you about the templated variables that need to be set for your pipeline to run.

All variables used by a dataset must have their values set in

```
  [.dev|.test]/datasets/{DATASET}/{DATASET}_variables.json
```

Airflow variables use JSON dot notation to access the variable's value. For example, if you're using the following variables in your pipeline config:

- `{{ var.json.shared.composer_bucket }}`
- `{{ var.json.parent.nested }}`
- `{{ var.json.parent.another_nested }}`

then your variables JSON file should look like this

```json
{
  "shared": {
    "composer_bucket": "us-east4-test-pipelines-abcde1234-bucket"
  },
  "parent": {
    "nested": "some value",
    "another_nested": "another value"
  }
}

```

## 6. Deploy the DAGs and variables

Deploy the DAG and the variables to your own Cloud Composer environment using one of the two commands:

```
# If you're using Cloud Composer
$ python scripts/deploy_dag.py \
  --dataset DATASET \
  --composer-env CLOUD_COMPOSER_ENVIRONMENT_NAME \
  --composer-bucket CLOUD_COMPOSER_BUCKET \
  --composer-region CLOUD_COMPOSER_REGION \
  --env ENV
```

or

```
# If you're using a local Airflow environment
$ python scripts/deploy_dag.py \
  --dataset DATASET \
  --local \
  [--airflow-home] (defaults to "~/airflow") \
  [--env] (defaults to "dev")
```

# Testing

Run the unit tests from the project root as follows:

```
$ pipenv run python -m pytest -v
```

# YAML Config Reference

Every dataset and pipeline folder must contain a `dataset.yaml` and a `pipeline.yaml` configuration file, respectively:

- For dataset configuration syntax, see [`samples/dataset.yaml`](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/samples/dataset.yaml) as a reference.
- For pipeline configuration syntax, see [`samples/pipeline.yaml`](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/samples/pipeline.yaml) as a reference.


# Best Practices

- When running `scripts/generate_terraform.py`, the argument `--bucket-name-prefix` helps prevent GCS bucket name collisions because bucket names must be globally unique. Make the prefix as unique as possible, and specific to your own environment or use case.
- When naming BigQuery columns, always use `snake_case` and lowercase.
- When specifying BigQuery schemas, be explicit and always include `name`, `type` and `mode` for every column. For column descriptions, derive it from the data source's definitions when available.
- When provisioning resources for pipelines, a good rule-of-thumb is one bucket per dataset, where intermediate data used by various pipelines (under that dataset) are stored in distinct paths under the same bucket. For example:

  ```
  gs://covid19-tracking-project-intermediate
      /dev
          /preprocessed_tests_and_outcomes
          /preprocessed_vaccinations
      /staging
          /national_tests_and_outcomes
          /state_tests_and_outcomes
          /state_vaccinations
      /prod
          /national_tests_and_outcomes
          /state_tests_and_outcomes
          /state_vaccinations

  ```
  The "one bucket per dataset" rule prevents us from creating too many buckets for too many purposes. This also helps in discoverability and organization as we scale to thousands of datasets and pipelines.

  Quick note: If you can conveniently fit the data in memory, the data transforms are close-to-trivial and are computationally cheap, you may skip having to store mid-stream data. Just apply the transformations in one go, and store the final resulting data to their final destinations.
