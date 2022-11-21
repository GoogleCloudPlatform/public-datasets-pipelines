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
import airflow.providers.google
import google.cloud
import os

import pandas as pd


def main(command: str) -> None:
    logging.info(f"process started")
    # os.system("airflow dags list")
    os.system(command)
    logging.info(f"process completed")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        command=os.environ.get("COMMAND", "ls")
    )
