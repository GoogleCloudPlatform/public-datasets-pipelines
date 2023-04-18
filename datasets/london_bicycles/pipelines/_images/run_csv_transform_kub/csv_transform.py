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

import csv
import datetime
import json
import logging
import os
import pathlib
import typing
from io import StringIO
from xml.etree import ElementTree

import bs4
import requests

import selenium.webdriver as web
from google.cloud import storage
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def main(
    source_url: dict,
    source_file: str,
    required_cols: list,
    rename_mappings: dict,
    date_cols: list,
    integer_cols: list,
    float_cols: list,
    string_cols: list,
    output_file: str,
    gcs_bucket: str,
    target_gcs_path: str,
    pipeline: str
) -> None:
    logging.info(
        f'{pipeline} pipeline process started at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )
    source_folder = os.path.split(source_file)[0]
    pathlib.Path(source_folder).mkdir(parents=True, exist_ok=True)
    if pipeline == "London Cycle Stations Dataset":
        for src_url in source_url:
            src_file_name = os.path.basename(source_url[src_url])
            dest_file = f"{source_folder}/{src_file_name}"
            # import pdb; pdb.set_trace()
            download_file(source_url[src_url], dest_file)
            process_xml(
                source_file,
                output_file,
                required_cols,
                rename_mappings,
                date_cols,
                integer_cols,
                float_cols,
                string_cols,
            )
            upload_file_to_gcs(output_file, gcs_bucket, target_gcs_path)
    elif pipeline == "London Cycle Trips Dataset":
        # import pdb; pdb.set_trace()
        files_list = https_list_all_file_links(url=source_url["trips"])
        logging.info(files_list)
    logging.info(
        f'{pipeline} pipeline process completed at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )


def https_list_all_file_links(url: str) -> typing.List[str]:
    serv = ChromeService(ChromeDriverManager().install())
    serv.start()
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    opt = Options()
    opt.add_argument("--no-sandbox")
    opt.add_argument("--headless")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--window-size=1920x1080")
    driver = web.Chrome(service=serv, desired_capabilities=caps, options=opt)
    driver.maximize_window()
    driver.get('https://cycling.data.tfl.gov.uk')
    driver.refresh()
    try:
        elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, "cycling-load.json")) #This is a dummy element
        )
        logging.info(f"found element {elem}")
    finally:
        pass
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    parser = etree.HTMLParser()
    page = driver.execute_script('return document.body;')
    body = page.get_attribute('innerHTML')
    soup=bs4.BeautifulSoup(body,"html.parser")
    links = []
    for link in soup.findAll('a'): links += [link.get('href')]
    serv.stop()
    tree = etree.parse(StringIO(body), parser=parser)
    refs = tree.xpath("//a")
    links = [link.get('href', '') for link in refs]
    return links


def download_file(source_url: str, source_file: str) -> None:
    logging.info(f"Downloading data from {source_url} to {source_file} .")
    res = requests.get(source_url, stream=True)
    if res.status_code == 200:
        with open(source_file, "wb") as fb:
            for chunk in res:
                fb.write(chunk)
    else:
        logging.info(f"Couldn't download {source_url}: {res.text}")
    logging.info(f"Downloaded data from {source_url} into {source_file}")


def get_data_dict(
    row_tag: ElementTree.Element,
    date_cols: list,
    integer_cols: list,
    float_cols: list,
    string_cols: list,
) -> dict:
    row_data = {}
    for col in row_tag:
        if col.tag in date_cols:
            row_data[col.tag] = parse_date(col.text)
        elif col.tag in integer_cols:
            row_data[col.tag] = int(col.text)
        elif col.tag in float_cols:
            row_data[col.tag] = float(col.text)
        elif col.tag in string_cols:
            row_data[col.tag] = col.text
    return row_data


def parse_date(date: str) -> datetime.datetime.date:
    if not date:
        return None
    date = datetime.datetime.fromtimestamp(int(date) / 1000)
    return date.date()


def process_xml(
    source_file: str,
    output_file: str,
    required_cols: list,
    rename_mappings: dict,
    date_cols: list,
    integer_cols: list,
    float_cols: list,
    string_cols: list,
) -> None:
    logging.info("Process started for converting .xml to .csv")
    xml_data = ElementTree.parse(source_file)
    root_tag = xml_data.getroot()
    row_tags = list(root_tag)
    logging.info(f"Opening {output_file} in 'w'(write) mode")
    with open(output_file, mode="w") as fb:
        logging.info(
            f"Creating csv writer(DictWriter) object with fieldnames={required_cols}"
        )
        writer = csv.DictWriter(fb, fieldnames=required_cols)
        logging.info(
            f"Writing headers(Renamed Headers) {rename_mappings} to {output_file}"
        )
        writer.writerow(rename_mappings)
        logging.info(f"Reading all xml tags and writing to {output_file}")
        for idx, row_tag in enumerate(row_tags, start=1):
            if not (idx % 100):
                logging.info(
                    f"\t{idx} rows of data cleaned and writing/appending to {output_file}"
                )
            row_entry = get_data_dict(
                row_tag, date_cols, integer_cols, float_cols, string_cols
            )
            writer.writerow(row_entry)
        logging.info(
            f"\t{idx} rows of data cleaned and writing/appending to {output_file}"
        )
    logging.info("Process completed for converting .xml to .csv")


def upload_file_to_gcs(
    target_csv_file: str, target_gcs_bucket: str, target_gcs_path: str
) -> None:
    logging.info(f"Uploading output file to gs://{target_gcs_bucket}/{target_gcs_path}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(target_gcs_bucket)
    blob = bucket.blob(target_gcs_path)
    blob.upload_from_filename(target_csv_file)
    logging.info("Successfully uploaded file to gcs bucket.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main(
        source_url=json.loads(os.environ.get("SOURCE_URL", "")),
        source_file=os.environ.get("SOURCE_FILE", ""),
        required_cols=json.loads(os.environ.get("REQUIRED_COLS", "[]")),
        rename_mappings=json.loads(os.environ.get("RENAME_MAPPINGS", "{}")),
        date_cols=json.loads(os.environ.get("DATE_COLS", "[]")),
        integer_cols=json.loads(os.environ.get("INTEGER_COLS", "[]")),
        float_cols=json.loads(os.environ.get("FLOAT_COLS", "[]")),
        string_cols=json.loads(os.environ.get("STRING_COLS", "[]")),
        output_file=os.environ.get("OUTPUT_FILE", ""),
        gcs_bucket=os.environ.get("GCS_BUCKET", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        pipeline=os.environ.get("PIPELINE", "")
    )
