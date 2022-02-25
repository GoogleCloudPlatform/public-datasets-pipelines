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
import os
import pathlib
import typing
from datetime import datetime

import bs4
import requests

CSV_HEADERS = [
    "state",
    "state_name",
    "date",
    "source_type",
    "time_of_day",
    "source_url",
    "google_cloud_storage_uri",
]


def main(source_url: str, csv_output_path: pathlib.Path, screenshots_gcs_prefix: str):
    response = requests.get(source_url)

    if response.status_code == 200:
        html = bs4.BeautifulSoup(response.text, "html.parser")
    else:
        raise requests.exceptions.HTTPError

    csv_rows = generate_csv_data_from_html(source_url, html, screenshots_gcs_prefix)
    write_to_csv(csv_rows, csv_output_path)


def generate_csv_data_from_html(
    domain: str, html: bs4.BeautifulSoup, screenshots_gcs_prefix: str
) -> typing.List[dict]:
    rows = []

    # Skip the first <a> tag because it's not a state-related link
    for link in html.find_all("a")[1:]:
        rows += generate_csv_rows(domain + link["href"], screenshots_gcs_prefix)

    return rows


def generate_csv_rows(url: str, gcs_path_prefix: str) -> typing.List[dict]:
    response = requests.get(url)

    if response.status_code == 200:
        page = bs4.BeautifulSoup(response.text, "html.parser")
    else:
        raise requests.exceptions.HTTPError(
            f"HTTP GET for {url} failed: {response.text}"
        )

    # Example `url`:
    # https://screenshots.covidtracking.com/alabama
    state_name = url.split("/")[-1]

    # Skip the headers row at index 0
    tr_tags = page.find_all("tr")[1:]

    rows = []
    current_date = None
    # Only get screenshots for the last 30 days
    for tr in tr_tags[:30]:
        td_date, td_source_type, td_screenshots = tr.find_all("td")

        if td_date.text:
            current_date = datetime.strptime(td_date.text, "%B %d, %Y").date()

        # Only get the last screenshot taken for the day
        for link in td_screenshots.find_all("a")[-1:]:
            # Example:
            # https://covidtracking.com/screenshots/AL/AL-20200315-163235.png
            screenshot_url = link["href"]
            *_, state, filename = screenshot_url.split("/")

            # Example: "4:22 pm"
            time_of_day = link.text

            rows.append(
                {
                    "state": state,
                    "state_name": state_name,
                    "date": str(current_date),
                    "source_type": td_source_type.text,
                    "time_of_day": time_of_day,
                    "source_url": screenshot_url,
                    "google_cloud_storage_uri": f"{gcs_path_prefix}/{state}/{str(current_date)}/{filename}",
                }
            )

    return rows


def write_to_csv(rows: typing.List[dict], output_path: pathlib.Path):
    with open(output_path, "w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        csv_writer.writeheader()
        for row in rows:
            csv_writer.writerow(row)


if __name__ == "__main__":
    assert os.environ["SOURCE_URL"]
    assert os.environ["GCS_PATH_PREFIX"]
    assert os.environ["CSV_OUTPUT_PATH"]
    main(
        source_url=os.environ["SOURCE_URL"],
        csv_output_path=pathlib.Path(os.environ["CSV_OUTPUT_PATH"]).expanduser(),
        screenshots_gcs_prefix=os.environ["GCS_PATH_PREFIX"],
    )
