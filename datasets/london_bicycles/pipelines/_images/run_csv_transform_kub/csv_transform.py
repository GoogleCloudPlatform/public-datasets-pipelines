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

import bs4
import csv
import datetime
from io import StringIO
import json
import logging
import os
import pandas as pd
import pathlib
import requests
import typing

from google.cloud import storage
from lxml import etree
import selenium.webdriver as web
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from xml.etree import ElementTree
from webdriver_manager.chrome import ChromeDriverManager


def main(
    source_url: dict,
    source_file: str,
    required_cols: typing.List[str],
    rename_mappings: dict,
    date_cols: typing.List[str],
    integer_cols: typing.List[str],
    float_cols: typing.List[str],
    string_cols: typing.List[str],
    output_file: str,
    output_csv_headers: typing.List[str],
    gcs_bucket: str,
    target_gcs_path: str,
    page_refresh_dummy_element: str,
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
        files_list = https_list_all_file_links(url=source_url["trips"], page_refresh_dummy_element=page_refresh_dummy_element)
        extract_list = [ s for s in files_list if 'JourneyDataExtract' in s]
        df_extract_list = pd.DataFrame(extract_list, columns = ['link_addr'])
        df_extract_list['id'] = df_extract_list['link_addr'].apply(lambda x: os.path.basename(str(x)).split('JourneyDataExtract')[0])
        df_extract_list['date_from_extr'] = df_extract_list['link_addr'].apply(lambda x: int(clean_date(os.path.basename(str(x)).split('JourneyDataExtract')[1].replace('.csv', '').replace('.xlsx', '').split('-')[0])))
        df_extract_list['date_to_extr'] = df_extract_list['link_addr'].apply(lambda x: int(clean_date(os.path.basename(str(x)).split('JourneyDataExtract')[1].replace('.csv', '').replace('.xlsx', '').split('-')[1])))
        download_link_addr = df_extract_list.loc[df_extract_list['date_to_extr'].idxmax()]['link_addr']
        download_file(source_url=download_link_addr, source_file=source_file)
        df_journey = pd.read_csv(source_file, sep=",", quotechar='"')
        rename_headers(df_journey, rename_mappings)
        df_journey = df_journey[output_csv_headers]
        df_journey['start_date'] = df_journey['start_date'].apply(lambda x: x if len(x) < 1 else f'{x}:00')
        df_journey['end_date'] = df_journey['end_date'].apply(lambda x: x if len(x) < 1 else f'{x}:00')
        import pdb; pdb.set_trace()
        logging.info(files_list)
    logging.info(
        f'{pipeline} pipeline process completed at {str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}'
    )


def clean_date(datestr: str) -> str:
    datestr = datestr.strip()
    if len(datestr) < 9:
        datestr = f'{datestr[:-2]}20{datestr[-2:]}'
    if datestr[:-4][-3].isnumeric:
        if datestr[:-4][-2:] == 'Fe':
            datestr = f'{datestr[:-6]}Feb{datestr[-4:]}'
    if len(datestr) == 9:
        datestr = datetime.datetime.strptime(datestr, '%d%b%Y').strftime('%Y%m%d')
    else:
        datestr = datetime.datetime.strptime(datestr, '%d%B%Y').strftime('%Y%m%d')
    return datestr


def https_list_all_file_links(url: str, page_refresh_dummy_element: str) -> typing.List[str]:
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
    driver.get(url)
    driver.refresh()
    try:
        elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, page_refresh_dummy_element))
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


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    logging.info("Renaming headers...")
    df.rename(columns=rename_mappings, inplace=True)


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
        output_csv_headers=json.loads(os.environ.get("OUTPUT_CSV_HEADERS", "[]")),
        gcs_bucket=os.environ.get("GCS_BUCKET", ""),
        page_refresh_dummy_element=os.environ.get("PAGE_REFRESH_DUMMY_ELEMENT", ""),
        target_gcs_path=os.environ.get("TARGET_GCS_PATH", ""),
        pipeline=os.environ.get("PIPELINE", "")
    )
