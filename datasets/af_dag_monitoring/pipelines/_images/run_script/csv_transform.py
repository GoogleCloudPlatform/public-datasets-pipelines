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
import logging
import os

# import airflow as af
# import airflow.api.client.api_client as dag_api
# import airflow.models as model

# import google.cloud
# import pandas as pd

# import airflow.providers.google as af
# from airflow import DAG as dag_obj

# from airflow.contrib.operators import gcs_to_bq, gcs_to_gcs
# from airflow.operators import bash as bash_op


def main(
            command: str,
            environment: str
         ) -> None:
    logging.info(f"process started")

    # cmd = f"gcloud composer environments run {environment} dags list --location us-central1 -- -o json"
    logging.info("running command:")
    logging.info(command)
    os.system(command)
    logging.info("completed command")

    # logging.info(f"Executing command... {command}")
    # dags = model.DagBag(dag_folder="/", include_examples=False, safe_mode=True, read_dags_from_db=True)
    # for daga in dags.dags:
    #     print(daga)
    # logging.info(str(api.Client.get_pools()))
    # logging.info(af.__all__)


    # logging.info(bag.DagBag("dags").dagbag_report())
    # test = bash_op.BashOperator(
    #     task_id="my_test",
    #     env={
    #         "airflow_home": "{{ var.value.airflow_home }}"
    #     },
    #     bash_command=command
    # )
    # test
    # os.system("airflow dags list")
    # os.system(command)
    logging.info(f"process completed")

# def list_dags() -> None:
#     with client.ApiClient(configuration) as api_client:
#         # Create an instance of the API class
#         api_instance = dag_api.DAGApi(api_client)
#         limit = 100
#         offset = 0
#         order_by = "order_by_example"
#         tags = [
#             "tags_example",
#         ]
#         only_active = True
#         try:
#             # List DAGs
#             api_response = api_instance.get_dags(limit=limit, offset=offset, order_by=order_by, tags=tags, only_active=only_active)
#             pprint(api_response)
#         except client.ApiException as e:
#             print("Exception when calling DAGApi->get_dags: %s\n" % e)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        command=os.environ.get("COMMAND", "ls"),
        environment=os.environ.get("ENVIRONMENT", "")
    )
