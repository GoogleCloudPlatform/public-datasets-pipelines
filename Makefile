# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

export TF_IN_AUTOMATION=1

generate-dag:
	python3 scripts/dag_generator.py

generate-terraform:
	python3 scripts/terraform_generator.py

build: generate-dag generate-terraform

build-image:
	gcloud builds submit --config=cloudbuild/cloudbuild.yaml cloudbuild/

build-test:
	gcloud builds submit --config=cloudbuild.yaml .

test:
	python3 -m unittest tests/dag_integrity_test.py

destroy:
	terraform destroy -input=false -auto-approve .generated

clean:
	find . -name "resources.tf" -exec rm -rf {} +
	find . -name "table.tf" -exec rm -rf {} +
	find . -name "terraform.tfstate*" -exec rm -rf {} +
	find . -name ".terraform" -exec rm -rf {} +
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".generated" -exec rm -rf {} +
	rm -rf ./bin
	rm -rf ./lib
	rm -f pyvenv.cfg

create-triggers:
	gcloud beta builds triggers create github --repo-owner="GoogleCloudPlatform" --repo-name="cloud-builders" --pull-request-pattern="^master$" --build-config="cloudbuild.yaml"

create-venv:
	python3 -m venv $(CURDIR); \
	. ./bin/activate; \
	pip3 install -r cloudbuild/requirements.txt; \
	export AIRFLOW_HOME=`pwd`/tmp; \
	export AIRFLOW__CORE__LOAD_EXAMPLES=False; \
	export AIRFLOW__CORE__DAGS_FOLDER=`pwd`/datasets; \
	airflow initdb

test-venv:
	. ./bin/activate; \
	$(MAKE) build; \
	export AIRFLOW_HOME=`pwd`/tmp; \
	export AIRFLOW__CORE__LOAD_EXAMPLES=False; \
	export AIRFLOW__CORE__DAGS_FOLDER=`pwd`/datasets; \
	python3 -m unittest tests/dag_integrity_test.py
