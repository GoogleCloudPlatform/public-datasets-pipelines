FROM python:3.8

# Allow statements and log messages to appear in Cloud logs
ENV PYTHONUNBUFFERED True
# ENV service_account_key_path="my-personal-instance-2c2c15d75117.json"

# Copy the requirements file into the image
COPY requirements.txt ./

# Install the packages specified in the requirements file
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# The WORKDIR instruction sets the working directory for any RUN, CMD,
# ENTRYPOINT, COPY and ADD instructions that follow it in the Dockerfile.
# If the WORKDIR doesn’t exist, it will be created even if it’s not used in
# any subsequent Dockerfile instruction
WORKDIR /custom

# Copy the specific data processing script/s in the image under /custom/*
COPY ./fake.py .
COPY ./data ./data

# Command to run the data processing script when the container is run
CMD ["python3", "fake.py"]
