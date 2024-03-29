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


import pathlib
import shutil

CURRENT_PATH = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_PATH.parent


def pytest_sessionfinish(session, exitstatus):
    test_folder = PROJECT_ROOT / ".test"
    if test_folder.exists():
        shutil.rmtree(test_folder)

    # clean up generated directories created from test/test_generate_pipeline.py
    test_dataset_folder = PROJECT_ROOT / "datasets" / "test_dataset"
    if test_dataset_folder.exists():
        shutil.rmtree(test_dataset_folder)
