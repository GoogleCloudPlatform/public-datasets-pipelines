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
ENV DEBIAN_FRONTEND noninteractive

# Copy the requirements file into the image
COPY requirements.txt ./

# Install the packages specified in the requirements file
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Upgrade pip
RUN python3 -m pip install --upgrade pip

RUN apt-get update && apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

WORKDIR /custom

# Copy the specific data processing script/s in the image under /custom/*
COPY ./csv_transform.py .

# Command to run the data processing script when the container is run
CMD ["python3", "csv_transform.py"]
