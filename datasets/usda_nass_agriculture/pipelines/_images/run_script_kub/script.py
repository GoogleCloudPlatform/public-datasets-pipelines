import logging
import os
from ftplib import FTP

from google.cloud import storage


def main(directory, host, gcs_bucket, gcs_path):
    ftp = FTP(host)
    ftp.login()
    ftp.cwd(directory)
    gzfiles = ftp.nlst()
    for file in gzfiles:
        if (
            file.endswith("gz")
            and "zipcode" not in file
            and "crop" not in file
            and "census2017" not in file
            and "environment" not in file
        ):
            logging.info(f"Downloading file {file} ---->")
            with open(file, "wb") as f:
                ftp.retrbinary(f"RETR {file}", f.write)
            upload_gcs(file, gcs_bucket, gcs_path)
            os.remove(file)


def upload_gcs(file, gcs_bucket, gcs_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path + file)
    blob.upload_from_filename(file)
    logging.info("Uploaded successfully")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        directory=os.environ.get("DIRECTORY"),
        host=os.environ.get("HOST"),
        gcs_bucket=os.environ.get("GCS_BUCKET"),
        gcs_path=os.environ.get("GCS_PATH"),
    )
