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


import datetime
import json
import logging
import os
import pathlib
import typing

import numpy as np
import pandas as pd
import requests
from google.cloud import storage


def main(
    source_url: str,
    year_report: str,
    api_naming_convention: str,
    target_file: pathlib.Path,
    target_gcs_bucket: str,
    target_gcs_path: str,
    headers: typing.List[str],
    rename_mappings: dict,
    pipeline_name: str,
    geography: str,
    report_level: str,
    concat_col: typing.List[str],
) -> None:

    logging.info(
        f"ACS {pipeline_name} process started at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    logging.info("Creating 'files' folder")
    pathlib.Path("./files").mkdir(parents=True, exist_ok=True)

    group_id = {
        "B25001001": "housing_units",
        "B25003001": "occupied_housing_units",
        "B25003003": "housing_units_renter_occupied",
        "B25070011": "rent_burden_not_computed",
        "B25070010": "rent_over_50_percent",
        "B25070009": "rent_40_to_50_percent",
        "B25070008": "rent_35_to_40_percent",
        "B25070007": "rent_30_to_35_percent",
        "B25070006": "rent_25_to_30_percent",
        "B25070005": "rent_20_to_25_percent",
        "B25070004": "rent_15_to_20_percent",
        "B25070003": "rent_10_to_15_percent",
        "B25070002": "rent_under_10_percent",
        "B11001001": "households",
        "B01003001": "total_pop",
        "B01001002": "male_pop",
        "B01001026": "female_pop",
        "B01002001": "median_age",
        "B03002003": "white_pop",
        "B03002004": "black_pop",
        "B03002005": "amerindian_pop",
        "B03002006": "asian_pop",
        "B03002008": "other_race_pop",
        "B03002009": "two_or_more_races_pop",
        "B03002002": "not_hispanic_pop",
        "B03002012": "hispanic_pop",
        "B05001006": "not_us_citizen_pop",
        "B08006001": "workers_16_and_over",
        "B08006002": "commuters_by_car_truck_van",
        "B08006003": "commuters_drove_alone",
        "B08006004": "commuters_by_carpool",
        "B08201002": "no_cars",
        "B08201003": "one_car",
        "B08201004": "two_cars",
        "B08201005": "three_cars",
        "B08201006": "four_more_cars",
        "B08301010": "commuters_by_public_transportation",
        "B08006009": "commuters_by_bus",
        "B08006011": "commuters_by_subway_or_elevated",
        "B08006015": "walked_to_work",
        "B08006017": "worked_at_home",
        "B09001001": "children",
        "B09005005": "children_in_single_female_hh",
        "B11001003": "married_households",
        "B11009003": "male_male_households",
        "B11009005": "female_female_households",
        "B14001001": "population_3_years_over",
        "B14001002": "in_school",
        "B14001005": "in_grades_1_to_4",
        "B14001006": "in_grades_5_to_8",
        "B14001007": "in_grades_9_to_12",
        "B14001008": "in_undergrad_college",
        "B15003001": "pop_25_years_over",
        "B07009002": "less_than_high_school_graduate",
        "B15003017": "high_school_diploma",
        "B07009003": "high_school_including_ged",
        "B15003019": "less_one_year_college",
        "B15003020": "one_year_more_college",
        "B15003021": "associates_degree",
        "B07009004": "some_college_and_associates_degree",
        "B15003022": "bachelors_degree",
        "B07009005": "bachelors_degree_2",
        "B15003023": "masters_degree",
        "B07009006": "graduate_professional_degree",
        "B16001001": "pop_5_years_over",
        "B16001002": "speak_only_english_at_home",
        "B16001003": "speak_spanish_at_home",
        "B16001005": "speak_spanish_at_home_low_english",
        "B17001001": "pop_determined_poverty_status",
        "B17001002": "poverty",
        "B19013001": "median_income",
        "B19083001": "gini_index",
        "B19301001": "income_per_capita",
        "B25002003": "vacant_housing_units",
        "B25004002": "vacant_housing_units_for_rent",
        "B25004004": "vacant_housing_units_for_sale",
        "B25058001": "median_rent",
        "B25071001": "percent_income_spent_on_rent",
        "B25075001": "owner_occupied_housing_units",
        "B25075025": "million_dollar_housing_units",
        "B25081002": "mortgaged_housing_units",
        "B25024002": "dwellings_1_units_detached",
        "B25024003": "dwellings_1_units_attached",
        "B25024004": "dwellings_2_units",
        "B25024005": "dwellings_3_to_4_units",
        "B25024006": "dwellings_5_to_9_units",
        "B25024007": "dwellings_10_to_19_units",
        "B25024008": "dwellings_20_to_49_units",
        "B25024009": "dwellings_50_or_more_units",
        "B25024010": "mobile_homes",
        "B25034002": "housing_built_2005_or_later",
        "B25034003": "housing_built_2000_to_2004",
        "B25034010": "housing_built_1939_or_earlier",
        "B23008002": "families_with_young_children",
        "B23008003": "two_parent_families_with_young_children",
        "B23008004": "two_parents_in_labor_force_families_with_young_children",
        "B23008005": "two_parents_father_in_labor_force_families_with_young_children",
        "B23008006": "two_parents_mother_in_labor_force_families_with_young_children",
        "B23008007": "two_parents_not_in_labor_force_families_with_young_children",
        "B23008008": "one_parent_families_with_young_children",
        "B23008009": "father_one_parent_families_with_young_children",
        "B23008010": "father_in_labor_force_one_parent_families_with_young_children",
        "B23025001": "pop_16_over",
        "B23025002": "pop_in_labor_force",
        "B23025003": "civilian_labor_force",
        "B23025004": "employed_pop",
        "B23025005": "unemployed_pop",
        "B23025006": "armed_forces",
        "B23025007": "not_in_labor_force",
        "C24050002": "employed_agriculture_forestry_fishing_hunting_mining",
        "C24050003": "employed_construction",
        "C24050004": "employed_manufacturing",
        "C24050005": "employed_wholesale_trade",
        "C24050006": "employed_retail_trade",
        "C24050007": "employed_transportation_warehousing_utilities",
        "C24050008": "employed_information",
        "C24050009": "employed_finance_insurance_real_estate",
        "C24050010": "employed_science_management_admin_waste",
        "C24050011": "employed_education_health_social",
        "C24050012": "employed_arts_entertainment_recreation_accommodation_food",
        "C24050013": "employed_other_services_not_public_admin",
        "C24050014": "employed_public_administration",
        "C24050015": "occupation_management_arts",
        "C24050029": "occupation_services",
        "C24050043": "occupation_sales_office",
        "C24050057": "occupation_natural_resources_construction_maintenance",
        "C24050071": "occupation_production_transportation_material",
        "B01001003": "male_under_5",
        "B01001004": "male_5_to_9",
        "B01001005": "male_10_to_14",
        "B01001006": "male_15_to_17",
        "B01001007": "male_18_to_19",
        "B01001008": "male_20",
        "B01001009": "male_21",
        "B01001010": "male_22_to_24",
        "B01001011": "male_25_to_29",
        "B01001012": "male_30_to_34",
        "B01001013": "male_35_to_39",
        "B01001014": "male_40_to_44",
        "B01001020": "male_65_to_66",
        "B01001021": "male_67_to_69",
        "B01001022": "male_70_to_74",
        "B01001023": "male_75_to_79",
        "B01001024": "male_80_to_84",
        "B01001025": "male_85_and_over",
        "B01001027": "female_under_5",
        "B01001028": "female_5_to_9",
        "B01001029": "female_10_to_14",
        "B01001030": "female_15_to_17",
        "B01001031": "female_18_to_19",
        "B01001032": "female_20",
        "B01001033": "female_21",
        "B01001034": "female_22_to_24",
        "B01001035": "female_25_to_29",
        "B01001036": "female_30_to_34",
        "B01001037": "female_35_to_39",
        "B01001038": "female_40_to_44",
        "B01001039": "female_45_to_49",
        "B01001040": "female_50_to_54",
        "B01001041": "female_55_to_59",
        "B01001042": "female_60_to_61",
        "B01001043": "female_62_to_64",
        "B01001044": "female_65_to_66",
        "B01001045": "female_67_to_69",
        "B01001046": "female_70_to_74",
        "B01001047": "female_75_to_79",
        "B01001048": "female_80_to_84",
        "B01001049": "female_85_and_over",
        "B02001002": "white_including_hispanic",
        "B02001003": "black_including_hispanic",
        "B02001004": "amerindian_including_hispanic",
        "B02001005": "asian_including_hispanic",
        "B03001003": "hispanic_any_race",
        "B15001027": "male_45_to_64",
        "B01001015": "male_45_to_49",
        "B01001016": "male_50_to_54",
        "B01001017": "male_55_to_59",
        "B01001018": "male_60_to_61",
        "B01001019": "male_62_to_64",
        "B01001B012": "black_male_45_54",
        "B01001B013": "black_male_55_64",
        "B01001I012": "hispanic_male_45_54",
        "B01001I013": "hispanic_male_55_64",
        "B01001H012": "white_male_45_54",
        "B01001H013": "white_male_55_64",
        "B01001D012": "asian_male_45_54",
        "B01001D013": "asian_male_55_64",
        "B15001028": "male_45_64_less_than_9_grade",
        "B15001029": "male_45_64_grade_9_12",
        "B15001030": "male_45_64_high_school",
        "B15001031": "male_45_64_some_college",
        "B15001032": "male_45_64_associates_degree",
        "B15001033": "male_45_64_bachelors_degree",
        "B15001034": "male_45_64_graduate_degree",
        "B12005001": "pop_15_and_over",
        "B12005002": "pop_never_married",
        "B12005005": "pop_now_married",
        "B12005008": "pop_separated",
        "B12005012": "pop_widowed",
        "B12005015": "pop_divorced",
        "B08134001": "commuters_16_over",
        "B08134002": "commute_less_10_mins",
        "B08303003": "commute_5_9_mins",
        "B08303004": "commute_10_14_mins",
        "B08303005": "commute_15_19_mins",
        "B08303006": "commute_20_24_mins",
        "B08303007": "commute_25_29_mins",
        "B08303008": "commute_30_34_mins",
        "B08303009": "commute_35_39_mins",
        "B08303010": "commute_40_44_mins",
        "B08134008": "commute_35_44_mins",
        "B08303011": "commute_45_59_mins",
        "B08134010": "commute_60_more_mins",
        "B08303012": "commute_60_89_mins",
        "B08303013": "commute_90_more_mins",
        "B08135001": "aggregate_travel_time_to_work",
        "B19001002": "income_less_10000",
        "B19001003": "income_10000_14999",
        "B19001004": "income_15000_19999",
        "B19001005": "income_20000_24999",
        "B19001006": "income_25000_29999",
        "B19001007": "income_30000_34999",
        "B19001008": "income_35000_39999",
        "B19001009": "income_40000_44999",
        "B19001010": "income_45000_49999",
        "B19001011": "income_50000_59999",
        "B19001012": "income_60000_74999",
        "B19001013": "income_75000_99999",
        "B19001014": "income_100000_124999",
        "B19001015": "income_125000_149999",
        "B19001016": "income_150000_199999",
        "B19001017": "income_200000_or_more",
        "B19058002": "households_public_asst_or_food_stamps",
        "B19059002": "households_retirement_income",
        "B25064001": "renter_occupied_housing_units_paying_cash_median_gross_rent",
        "B25076001": "owner_occupied_housing_units_lower_value_quartile",
        "B25077001": "owner_occupied_housing_units_median_value",
        "B25078001": "owner_occupied_housing_units_upper_value_quartile",
        "B07204001": "population_1_year_and_over",
        "B07204004": "different_house_year_ago_same_city",
        "B07204007": "different_house_year_ago_different_city",
        "B26001001": "group_quarters",
        "B08014002": "no_car",
        "C24060004": "sales_office_employed",
        "C24060002": "management_business_sci_arts_employed",
        "B23006001": "pop_25_64",
        "B23006023": "bachelors_degree_or_higher_25_64",
        "B11001007": "nonfamily_households",
        "B11001002": "family_households",
        "B25035001": "median_year_structure_built",
    }

    state_code = {
        "01": "Alabama",
        "02": "Alaska",
        "04": "Arizona",
        "05": "Arkansas",
        "06": "California",
        "08": "Colorado",
        "09": "Connecticut",
        "10": "Delaware",
        "11": "District of Columbia",
        "12": "Florida",
        "13": "Georgia",
        "15": "Hawaii",
        "16": "Idaho",
        "17": "Illinois",
        "18": "Indiana",
        "19": "Iowa",
        "20": "Kansas",
        "21": "Kentucky",
        "22": "Louisiana",
        "23": "Maine",
        "24": "Maryland",
        "25": "Massachusetts",
        "26": "Michigan",
        "27": "Minnesota",
        "28": "Mississippi",
        "29": "Missouri",
        "30": "Montana",
        "31": "Nebraska",
        "32": "Nevada",
        "33": "New Hampshire",
        "34": "New Jersey",
        "35": "New Mexico",
        "36": "New York",
        "37": "North Carolina",
        "38": "North Dakota",
        "39": "Ohio",
        "40": "Oklahoma",
        "41": "Oregon",
        "42": "Pennsylvania",
        "44": "Rhode Island",
        "45": "South Carolina",
        "46": "South Dakota",
        "47": "Tennessee",
        "48": "Texas",
        "49": "Utah",
        "50": "Vermont",
        "51": "Virginia",
        "53": "Washington",
        "54": "West Virginia",
        "55": "Wisconsin",
        "56": "Wyoming",
        "60": "American Samoa",
        "66": "Guam",
        "69": "Commonwealth of the Northern Mariana Islands",
        "72": "Puerto Rico",
        "78": "United States Virgin Islands",
    }

    logging.info("Extracting the data from API and loading into dataframe...")
    if report_level == "national_level":
        df = extract_data_and_convert_to_df_national_level(
            group_id, year_report, api_naming_convention, source_url
        )
    elif report_level == "state_level":
        df = extract_data_and_convert_to_df_state_level(
            group_id, state_code, year_report, api_naming_convention, source_url
        )

    logging.info("Replacing values...")
    df = df.replace(to_replace={"KPI_Name": group_id})

    logging.info("Renaming headers...")
    rename_headers(df, rename_mappings)

    logging.info("Creating column geo_id...")
    if geography == "censustract":
        df["tract"] = df["tract"].apply(change_length, args=("6"))
        df["state"] = df["state"].apply(change_length, args=("2"))
        df["county"] = df["county"].apply(change_length, args=("3"))

    # This part needs confirmation from Shane
    df = create_geo_id(df, concat_col)

    logging.info("Pivoting the dataframe...")
    df = df[["geo_id", "KPI_Name", "KPI_Value"]]
    df = df.pivot_table(
        index="geo_id", columns="KPI_Name", values="KPI_Value", aggfunc=np.sum
    ).reset_index()

    logging.info("Reordering headers...")
    df = df[headers]

    logging.info(f"Saving to output file.. {target_file}")
    try:
        save_to_new_file(df, file_path=str(target_file))
    except Exception as e:
        logging.error(f"Error saving output file: {e}.")

    logging.info(
        f"Uploading output file to.. gs://{target_gcs_bucket}/{target_gcs_path}"
    )
    upload_file_to_gcs(target_file, target_gcs_bucket, target_gcs_path)

    logging.info(
        f"ACS {pipeline_name} process completed at "
        + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def string_replace(source_url, replace: dict) -> str:
    for k, v in replace.items():
        source_url = source_url.replace(k, v)
    return source_url


def extract_data_and_convert_to_df_national_level(
    group_id: dict, year_report: str, api_naming_convention: str, source_url: str
) -> pd.DataFrame:
    list_temp = []
    for key in group_id:
        logging.info(f"reading data from API for KPI {key}...")
        replece = {
            "+year_report+": year_report,
            "+key[0:-3]+": key[0:-3],
            "+key[-3:]+": key[-3:],
            "+api_naming_convention+": api_naming_convention,
        }
        source_url = string_replace(source_url, replece)
        try:
            r = requests.get(source_url, stream=True)
            if r.status_code == 200:
                text = r.json()
                frame = pd.DataFrame(text)
                frame = frame.iloc[1:, :]
                frame["KPI_Name"] = key
                list_temp.append(frame)
        except OSError as e:
            logging.info(f"error : {e}")
    logging.info("creating the dataframe...")
    df = pd.concat(list_temp)
    return df


def extract_data_and_convert_to_df_state_level(
    group_id: dict,
    state_code: dict,
    year_report: str,
    api_naming_convention: str,
    source_url: str,
) -> pd.DataFrame:
    list_temp = []
    for key in group_id:
        for sc in state_code:
            logging.info(f"reading data from API for KPI {key}...")
            logging.info(f"reading data from API for KPI {sc}...")
            replece = {
                "+year_report+": year_report,
                "+key[0:-3]+": key[0:-3],
                "+key[-3:]+": key[-3:],
                "+api_naming_convention+": api_naming_convention,
                "+sc+": sc,
            }
            source_url = string_replace(source_url, replece)
            try:
                r = requests.get(source_url, stream=True)
                if r.status_code == 200:
                    text = r.json()
                    frame = pd.DataFrame(text)
                    frame = frame.iloc[1:, :]
                    frame["KPI_Name"] = key
                    list_temp.append(frame)
            except OSError as e:
                logging.info(f"error : {e}")
    logging.info("creating the dataframe...")
    df = pd.concat(list_temp)
    return df


def create_geo_id(df: pd.DataFrame, concat_col: str) -> pd.DataFrame:
    df["geo_id"] = ""
    for col in concat_col:
        df["geo_id"] = df["geo_id"] + df[col]
    return df


def change_length(val: str, length: int) -> str:
    if len(str(val)) < int(length):
        return ("0" * (int(length) - len(str(val)))) + str(val)
    else:
        return str(val)


def rename_headers(df: pd.DataFrame, rename_mappings: dict) -> None:
    rename_mappings = {int(k): str(v) for k, v in rename_mappings.items()}
    df.rename(columns=rename_mappings, inplace=True)


def save_to_new_file(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


def upload_file_to_gcs(file_path: pathlib.Path, gcs_bucket: str, gcs_path: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    main(
        source_url=os.environ["SOURCE_URL"],
        # source_file=pathlib.Path(os.environ["SOURCE_FILE"]).expanduser(),
        year_report=os.environ["YEAR_REPORT"],
        api_naming_convention=os.environ["API_NAMING_CONVENTION"],
        target_file=pathlib.Path(os.environ["TARGET_FILE"]).expanduser(),
        target_gcs_bucket=os.environ["TARGET_GCS_BUCKET"],
        target_gcs_path=os.environ["TARGET_GCS_PATH"],
        headers=json.loads(os.environ["CSV_HEADERS"]),
        rename_mappings=json.loads(os.environ["RENAME_MAPPINGS"]),
        pipeline_name=os.environ["PIPELINE_NAME"],
        geography=os.environ["GEOGRAPHY"],
        report_level=os.environ["REPORT_LEVEL"],
        concat_col=json.loads(os.environ["CONCAT_COL"]),
    )
