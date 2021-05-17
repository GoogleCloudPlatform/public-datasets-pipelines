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

# The base image for this build
FROM python:3.8

# Allow statements and log messages to appear in Cloud logs
ENV PYTHONUNBUFFERED True

# Add your script's required packages here
RUN pip install --no-cache-dir \
    requests

# The WORKDIR instruction sets the working directory for any RUN, CMD,
# ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile.
# If the WORKDIR doesn’t exist, it will be created even if it’s not used in
# any subsequent Dockerfile instruction
WORKDIR /custom

# Copy the specific data processing script/s in the image under /custom/*
COPY ./script.py .

# Command to run the data processing script when the container is run
CMD ["python", "-s", "script.py"]
