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
FROM python:3.8
ENV PYTHONUNBUFFERED True
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install fsspec
RUN python3 -m pip install gcsfs
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin
WORKDIR /custom
COPY ./csv_transform.py .
CMD ["python3", "csv_transform.py"]
