# Public Datasets Pipelines

Cloud-native, data pipeline architecture for onboarding public datasets to [Datasets for Google Cloud](https://cloud.google.com/solutions/datasets).

# Overview

![public-datasets-pipelines](images/architecture.png)

# Requirements
- Python `>=3.6.10,<3.9`. We currently use `3.8`. For more info, see the [Cloud Composer version list](https://cloud.google.com/composer/docs/concepts/versioning/composer-versions).
- Familiarity with [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/concepts/index.html) (`>=v2.1.0`)
- [pipenv](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv) for creating similar Python environments via `Pipfile.lock`
- [gcloud](https://cloud.google.com/sdk/gcloud) command-line tool with Google Cloud Platform credentials configured. Instructions can be found [here](https://cloud.google.com/sdk/docs/initializing).
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) `>=v0.15.1`
- [Google Cloud Composer](https://cloud.google.com/composer/docs/concepts/overview) environment running [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html) `>=2.1.0` and Cloud Composer `>=2.0.0`. To create a new Cloud Composer environment, see [this guide](https://cloud.google.com/composer/docs/how-to/managing/creating).

# Environment Setup

We use Pipenv to make environment setup more deterministic and uniform across different machines. If you haven't done so, install Pipenv using these [instructions](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv).

With Pipenv installed, run the following command to install the dependencies:

```bash
pipenv install --ignore-pipfile --dev
```

This installs dependencies using the specific versions in the `Pipfile.lock` file (instead of the `Pipfile` file which is ignored via `--ignore-pipfile`).

Finally, initialize the Airflow database:

```bash
pipenv run airflow db init
```

To ensure you have a proper setup, run the tests:
```
$ pipenv run python -m pytest -v
```

# Building Data Pipelines

Configuring, generating, and deploying data pipelines in a programmatic, standardized, and scalable way is the main purpose of this repository.

Follow the steps below to build a data pipeline for your dataset:

## 1. Create a folder hierarchy for your pipeline

```
mkdir -p datasets/$DATASET/pipelines/$PIPELINE

[example]
datasets/google_trends/pipelines/top_terms
```

where `DATASET` is the dataset name or category that your pipeline belongs to, and `PIPELINE` is your pipeline's name.

For examples of pipeline names, see [these pipeline folders in the repo](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/tree/main/datasets/covid19_tracking).

Use only underscores and alpha-numeric characters for the names.


## 2. Write your YAML configs

### Define your `dataset.yaml`

If you created a new dataset directory above, you need to create a `datasets/$DATASET/pipelines/dataset.yaml` file. See this [section](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/README.md#yaml-config-reference) for the `dataset.yaml` reference.

### Define your `pipeline.yaml`

Create a `datasets/$DATASET/pipelines/$PIPELINE/pipeline.yaml` config file for your pipeline. See [here](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/samples/) for the `pipeline.yaml` references.

For a YAML config template using Airflow 1.10 operators, see [`samples/pipeline.airflow1.yaml`](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/samples/pipeline.airflow1.yaml).

As an alternative, you can inspect config files that are already in the repository and use them as a basis for your pipelines.

Every YAML file supports a `resources` block. To use this, identify what Google Cloud resources need to be provisioned for your pipelines. Some examples are

- BigQuery datasets and tables to store final, customer-facing data
- GCS bucket to store downstream data, such as those linked to in the [Datasets Marketplace](https://console.cloud.google.com/marketplace/browse?filter=solution-type:dataset).
- Sometimes, for very large datasets that requires processing to be parallelized, you might need to provision a [Dataflow](https://cloud.google.com/dataflow/docs) (Apache Beam) job


## 3. Generate Terraform files and actuate GCP resources

Run the following command from the project root:
```bash
$ pipenv run python scripts/generate_terraform.py \
    --dataset $DATASET \
    --gcp-project-id $GCP_PROJECT_ID \
    --region $REGION \
    --bucket-name-prefix $UNIQUE_BUCKET_PREFIX \
    [--env $ENV] \
    [--tf-state-bucket $TF_BUCKET] \
    [--tf-state-prefix $TF_BUCKET_PREFIX ] \
    [--impersonating-acct] $IMPERSONATING_SERVICE_ACCT \
    [--tf-apply]
```

This generates Terraform `*.tf` files  in your dataset's `infra` folder. The `.tf` files contain infrastructure-as-code: GCP resources that need to be created for the pipelines to work. The pipelines (DAGs) interact with resources such as GCS buckets or BQ tables while performing its operations (tasks).

To actuate the resources specified in the generated `.tf` files, use the `--tf-apply` flag. For those familiar with Terraform, this will run the `terraform apply` command inside the `infra` folder.

The `--bucket-name-prefix` is used to ensure that the buckets created by different environments and contributors are kept unique. This is to satisfy the rule where bucket names must be globally unique across all of GCS. Use hyphenated names (`some-prefix-123`) instead of snakecase or underscores (`some_prefix_123`).

The `--tf-state-bucket` and `--tf-state-prefix` parameters can be optionally used if one needs to use a remote store for the Terraform state. This will create a `backend.tf` file that points to the GCS bucket and prefix to use in storing the Terraform state. For more info, see the [Terraform docs for using GCS backends](https://www.terraform.io/docs/language/settings/backends/gcs.html).

In addition, the command above creates a "dot env" directory in the project root. The directory name is the value you set for `--env`. If it's not set, the value defaults to `dev` which generates the `.dev` folder.

We strongly recommend using a dot directory as your own sandbox, specific to your machine, that's mainly used for prototyping. This directory is where you will set the variables specific to your environment: such as actual GCS bucket names, GCR repository URLs, and secrets (we recommend using [Secret Manager](https://cloud.google.com/composer/docs/secret-manager) for this). The files and variables created or copied in the dot directories are isolated from the main repo, meaning that all dot directories are gitignored.

As a concrete example, the unit tests use a temporary `.test` directory as their environment.


## 4. Generate DAGs and container images

Run the following command from the project root:

```bash
$ pipenv run python scripts/generate_dag.py \
    --dataset $DATASET \
    --pipeline $PIPELINE \
    [--all-pipelines] \
    [--skip-builds] \
    [--env $ENV]
```

**Note: When this command runs successfully, it may ask you to set your pipeline's variables. Declaring and setting pipeline variables are explained in the [next step](https://github.com/googlecloudplatform/public-datasets-pipelines#5-declare-and-set-your-airflow-variables).**

This generates an Airflow DAG file (`.py`) in the `datasets/$DATASET/pipelines/$PIPELINE` directory, where the contents are based on the configuration specific in the `pipeline.yaml` file. This helps standardize Python code styling for all pipelines.

The generated DAG file is a Python file that represents your pipeline (the dot dir also gets a copy), ready to be interpreted by Airflow / Cloud Composer. , the code in the generated `.py` files is based entirely out of the contents in the `pipeline.yaml` config file.

### Using the `KubernetesPodOperator` for custom DAG tasks

Sometimes, Airflow's built-in operators don't support a specific, custom process you need for your pipeline. The recommended solution is to use `KubernetesPodOperator` which runs a container image that houses the scripts, build instructions, and dependencies needd to perform a custom process.

To prepare a container image containing your custom code, follow these instructions:

1. Create an `_images` folder in your dataset's `pipelines` folder if it doesn't exist.

2. Inside the `_images` folder, create a subfolder and name it after the image you intend to build or what it's expected to do, e.g. `transform_csv`, `process_shapefiles`, `read_cdf_metadata`.

3. In that subfolder, create a [Dockerfile](https://docs.docker.com/engine/reference/builder/) along with the scripts and dependencies you need to run process. See the [`samples/container`](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/samples/container/) folder for an example. Use the [COPY command](https://docs.docker.com/engine/reference/builder/#copy) in your `Dockerfile` to include your scripts when the image gets built.

The resulting file tree for a dataset that uses two container images may look like

```
datasets/
└── $DATASET/
   ├── infra/
   └── pipelines/
       ├── _images/
       │   ├── container_image_1/
       │   │   ├── Dockerfile
       │   │   ├── requirements.txt
       │   │   └── script.py
       │   └── container_image_2/
       │       ├── Dockerfile
       │       ├── requirements.txt
       │       └── script.py
       ├── PIPELINE_A/
       ├── PIPELINE_B/
       ├── ...
       └── dataset.yaml
```

Running the `generate_dag.py` script allows you to build and push your container images to [Google Container Registry](https://cloud.google.com/container-registry), where they can now be referenced in the `image` parameter of the `KubernetesPodOperator`.

Docker images will be built and pushed to GCR by default whenever the command above is run. To skip building and pushing images, use the optional `--skip-builds` flag.

## 5. Declare and set your Airflow variables

**Note: If your pipeline doesn't use any Airflow variables, you can skip this step.**

Running the `generate_dag` command in the previous step will parse your pipeline config and inform you about the parameterized Airflow variables your pipeline expects to use. In this step, you will be declaring and setting those variables.

There are two types of variables that pipelines use in this repo: **built-in environment variables** and **dataset-specific variables**.

### Built-in environment variables

Built-in variables are those that are [stored as environment variables](https://cloud.google.com/composer/docs/composer-2/set-environment-variables) in the Cloud Composer environment. This is a built-in Airflow feature, as shown in [this guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/variable.html#storing-variables-in-environment-variables).

The table below contains the built-in variables we're using for this architecture and configured in our Composer environment:

Value  |  Template Syntax
------- | --------
GCP project of the Composer environment | `{{ var.value.gcp_project }}`
GCS bucket of the Composer environment | `{{ var.value.composer_bucket }}`
Airflow home directory. This is convenient when using `BashOperator` to save data to [local directories mapped into GCS paths](https://cloud.google.com/composer/docs/composer-2/cloud-storage). | `{{ var.value.airflow_home }}`

**When a pipeline requires one of these variables, its associated template syntax must be used.** Users who are using this architecture to develop and manage pipelines in their own GCP project must have these set as [environment variables](https://cloud.google.com/composer/docs/composer-2/set-environment-variables) in their Cloud Composer environment.

### Dataset-specific variables

Another type of variable is dataset-specific variables. To make use of dataset-specific variables, create the following JSON file

```
  [.dev|.test]/datasets/$DATASET/pipelines/$DATASET_variables.json
```

In general, pipelines use the JSON dot notation to access Airflow variables. Make sure to define and nest your variables under the dataset's name as the parent key. Airflow variables are globally accessed by any pipeline, which means namespacing your variables under a dataset helps avoid collisions. For example, if you're using the following variables in your pipeline config for a dataset named `google_sample_dataset`:

- `{{ var.json.google_sample_dataset.some_variable }}`
- `{{ var.json.google_sample_dataset.some_nesting.nested_variable }}`

then your variables JSON file should look like this

```json
{
  "google_sample_dataset": {
    "some_variable": "value",
    "some_nesting": {
      "nested_variable": "another value"
    }
  }
}

```

## 6. Deploy the DAGs and variables

This step requires a Cloud Composer environment up and running in your Google Cloud project because you will deploy the DAG to this environment. To create a new Cloud Composer environment, see [this guide](https://cloud.google.com/composer/docs/how-to/managing/creating).

To deploy the DAG and the variables to your Cloud Composer environment, use the command

```
$ pipenv run python scripts/deploy_dag.py \
  --dataset DATASET \
  [--pipeline PIPELINE] \
  --composer-env CLOUD_COMPOSER_ENVIRONMENT_NAME \
  --composer-bucket CLOUD_COMPOSER_BUCKET \
  --composer-region CLOUD_COMPOSER_REGION \
  --env ENV
```

Specifying an argument to `--pipeline` is optional. By default, the script deploys all pipelines under the dataset set in `--dataset`.

# Testing

Run the unit tests from the project root as follows:

```
$ pipenv run python -m pytest -v
```

# YAML Config Reference

Every dataset and pipeline folder must contain a `dataset.yaml` and a `pipeline.yaml` configuration file, respectively.

The `samples` folder contains references for the YAML config files, complete with descriptions for config blocks and Airflow operators and parameters. When creating a new dataset or pipeline, you can copy them to your specific dataset/pipeline paths to be used as templates.

- For dataset configuration syntax, see the [`samples/dataset.yaml`](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/samples/dataset.yaml) reference.
- For pipeline configuration syntax:
  - For the default Airflow 2 operators, see the [`samples/pipeline.yaml`](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/samples/pipeline.yaml) reference.
  - If you'd like to use Airflow 1.10 operators, see the [`samples/pipeline.airflow1.yaml`](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/blob/main/samples/pipeline.yaml) as a reference.


# Best Practices

- When your tabular data contains percentage values, represent them as floats between 0 to 1.
- To represent hierarchical data in BigQuery, use either:
  - (Recommended) Nested columns in BigQuery. For more info, see [the documentation on nested and repeated columns](https://cloud.google.com/bigquery/docs/nested-repeated).
  - Or, represent each level as a separate column. For example, if you have the following hierarchy: `chapter > section > subsection`, then represent them as

    ```
    |chapter          |section|subsection          |page|
    |-----------------|-------|--------------------|----|
    |Operating Systems|       |                    |50  |
    |Operating Systems|Linux  |                    |51  |
    |Operating Systems|Linux  |The Linux Filesystem|51  |
    |Operating Systems|Linux  |Users & Groups      |58  |
    |Operating Systems|Linux  |Distributions       |70  |
    ```

- When running `scripts/generate_terraform.py`, the argument `--bucket-name-prefix` helps prevent GCS bucket name collisions because bucket names must be globally unique. Use hyphens over underscores for the prefix and make it as unique as possible, and specific to your own environment or use case.
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
