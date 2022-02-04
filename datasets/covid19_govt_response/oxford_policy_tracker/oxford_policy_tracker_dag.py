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


from airflow import DAG
from airflow.providers.cncf.kubernetes.operators import kubernetes_pod
from airflow.providers.google.cloud.transfers import gcs_to_bigquery

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-03-01",
}


with DAG(
    dag_id="covid19_govt_response.oxford_policy_tracker",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@daily",
    catchup=False,
    default_view="graph",
) as dag:

    # Run CSV transform within kubernetes pod
    oxford_policy_tracker_transform_csv = kubernetes_pod.KubernetesPodOperator(
        task_id="oxford_policy_tracker_transform_csv",
        startup_timeout_seconds=600,
        name="oxford_policy_tracker",
        namespace="composer",
        service_account_name="datasets",
        image_pull_policy="Always",
        image="{{ var.json.covid19_govt_response.container_registry.run_csv_transform_kub }}",
        env_vars={
            "SOURCE_URL": "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv",
            "SOURCE_FILE": "files/data.csv",
            "TARGET_FILE": "files/data_output.csv",
            "TARGET_GCS_BUCKET": "{{ var.value.composer_bucket }}",
            "TARGET_GCS_PATH": "data/covid19_govt_response/oxford_policy_tracker/data_output.csv",
            "PIPELINE_NAME": "oxford_policy_tracker",
            "CSV_HEADERS": '["country_name","alpha_3_code","region_name","region_code","date","school_closing","school_closing_flag","school_closing_notes","workplace_closing","workplace_closing_flag","workplace_closing_notes","cancel_public_events","cancel_public_events_flag","cancel_public_events_notes","restrictions_on_gatherings","restrictions_on_gatherings_flag","restrictions_on_gatherings_notes","close_public_transit","close_public_transit_flag","close_public_transit_notes","stay_at_home_requirements","stay_at_home_requirements_flag","stay_at_home_requirements_notes","restrictions_on_internal_movement","restrictions_on_internal_movement_flag","restrictions_on_internal_movement_notes","international_travel_controls","international_travel_controls_notes","income_support","income_support_flag","income_support_notes","debt_contract_relief","debt_contract_relief_notes","fiscal_measures","fiscal_measures_notes","international_support","international_support_notes","public_information_campaigns","public_information_campaigns_flag","public_information_campaigns_notes","testing_policy","testing_policy_notes","contact_tracing","contact_tracing_notes","emergency_healthcare_investment","emergency_healthcare_investment_notes","vaccine_investment","vaccine_investment_notes","misc_wildcard","misc_wildcard_notes","confirmed_cases","deaths","strintgency_index"]',
            "RENAME_MAPPINGS": '{"CountryName":"country_name","CountryCode":"alpha_3_code","RegionName":"region_name","RegionCode":"region_code","Date":"date","C1_School closing":"school_closing","C1_Flag":"school_closing_flag","C1_Notes":"school_closing_notes","C2_Workplace closing":"workplace_closing","C2_Flag":"workplace_closing_flag","C2_Notes":"workplace_closing_notes","C3_Cancel public events":"cancel_public_events","C3_Flag":"cancel_public_events_flag","C3_Notes":"cancel_public_events_notes","C4_Restrictions on gatherings":"restrictions_on_gatherings","C4_Flag":"restrictions_on_gatherings_flag","C4_Notes":"restrictions_on_gatherings_notes","C5_Close public transport":"close_public_transit","C5_Flag":"close_public_transit_flag","C5_Notes":"close_public_transit_notes","C6_Stay at home requirements":"stay_at_home_requirements","C6_Flag":"stay_at_home_requirements_flag","C6_Notes":"stay_at_home_requirements_notes","C7_Restrictions on internal movement":"restrictions_on_internal_movement","C7_Flag":"restrictions_on_internal_movement_flag","C7_Notes":"restrictions_on_internal_movement_notes","C8_International travel controls":"international_travel_controls","C8_Notes":"international_travel_controls_notes","E1_Income support":"income_support","E1_Flag":"income_support_flag","E1_Notes":"income_support_notes","E2_Debt/contract relief":"debt_contract_relief","E2_Notes":"debt_contract_relief_notes","E3_Fiscal measures":"fiscal_measures","E3_Notes":"fiscal_measures_notes","E4_International support":"international_support","E4_Notes":"international_support_notes","H1_Public information campaigns":"public_information_campaigns","H1_Flag":"public_information_campaigns_flag","H1_Notes":"public_information_campaigns_notes","H2_Testing policy":"testing_policy","H2_Notes":"testing_policy_notes","H3_Contact tracing":"contact_tracing","H3_Notes":"contact_tracing_notes","H4_Emergency investment in healthcare":"emergency_healthcare_investment","H4_Notes":"emergency_healthcare_investment_notes","H5_Investment in vaccines":"vaccine_investment","H5_Notes":"vaccine_investment_notes","M1_Wildcard":"misc_wildcard","M1_Notes":"misc_wildcard_notes","ConfirmedCases":"confirmed_cases","ConfirmedDeaths":"deaths","StringencyIndexForDisplay":"strintgency_index"}',
        },
        resources={"request_memory": "2G", "request_cpu": "1"},
    )

    # Task to load CSV data to a BigQuery table
    load_oxford_policy_tracker_to_bq = gcs_to_bigquery.GCSToBigQueryOperator(
        task_id="load_oxford_policy_tracker_to_bq",
        bucket="{{ var.value.composer_bucket }}",
        source_objects=[
            "data/covid19_govt_response/oxford_policy_tracker/data_output.csv"
        ],
        source_format="CSV",
        destination_project_dataset_table="covid19_govt_response.oxford_policy_tracker",
        skip_leading_rows=1,
        allow_quoted_newlines=True,
        write_disposition="WRITE_TRUNCATE",
        schema_fields=[
            {
                "name": "country_name",
                "type": "string",
                "description": "Name of the country",
                "mode": "nullable",
            },
            {
                "name": "alpha_3_code",
                "type": "string",
                "description": "3-letter alpha code abbreviation of the country/region. See `bigquery-public-data.utility_us.country_code_iso` for more details",
                "mode": "nullable",
            },
            {
                "name": "region_name",
                "type": "string",
                "description": "Name of the region within the country",
                "mode": "nullable",
            },
            {
                "name": "region_code",
                "type": "string",
                "description": "Code of the region within the country",
                "mode": "nullable",
            },
            {
                "name": "date",
                "type": "date",
                "description": "Date of the measured policy action status",
                "mode": "nullable",
            },
            {
                "name": "school_closing",
                "type": "string",
                "description": "C1 - Ordinal scale record closings of schools and universities; 0 - No measures 1 - recommend closing 2 - Require closing (only some levels or categories eg just high school or just public schools) 3 - Require closing all levels No data - blank",
                "mode": "nullable",
            },
            {
                "name": "school_closing_flag",
                "type": "string",
                "description": "Are C1 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
                "mode": "nullable",
            },
            {
                "name": "school_closing_notes",
                "type": "string",
                "description": "Additional details about C1 policy actions",
                "mode": "nullable",
            },
            {
                "name": "workplace_closing",
                "type": "string",
                "description": "C2 - Ordinal scale record closings of workplace; 0 - No measures 1 - recommend closing (or work from home) 2 - require closing (or work from home) for some sectors or categories of workers 3 - require closing (or work from home) all-but-essential workplaces (eg grocery stores doctors) No data - blank",
                "mode": "nullable",
            },
            {
                "name": "workplace_closing_flag",
                "type": "string",
                "description": "Are C2 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
                "mode": "nullable",
            },
            {
                "name": "workplace_closing_notes",
                "type": "string",
                "description": "Additional details about C2 policy actions",
                "mode": "nullable",
            },
            {
                "name": "cancel_public_events",
                "type": "string",
                "description": "C3 - Ordinal scale record cancellations of public events;0- No measures 1 - Recommend cancelling 2 - Require cancelling No data - blank",
                "mode": "nullable",
            },
            {
                "name": "cancel_public_events_flag",
                "type": "string",
                "description": "Are C3 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
                "mode": "nullable",
            },
            {
                "name": "cancel_public_events_notes",
                "type": "string",
                "description": "Additional details about C3 policy actions",
                "mode": "nullable",
            },
            {
                "name": "restrictions_on_gatherings",
                "type": "string",
                "description": "C4 - Ordinal scale to record the cut-off size for bans on private gatherings;  0 - No restrictions 1 - Restrictions on very large gatherings (the limit is above 1000 people) 2 - Restrictions on gatherings between 100-1000 people 3 - Restrictions on gatherings between 10-100 people 4 - Restrictions on gatherings of less than 10 people No data - blank",
                "mode": "nullable",
            },
            {
                "name": "restrictions_on_gatherings_flag",
                "type": "string",
                "description": "Are C4 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
                "mode": "nullable",
            },
            {
                "name": "restrictions_on_gatherings_notes",
                "type": "string",
                "description": "Additional details about C4 policy actions",
                "mode": "nullable",
            },
            {
                "name": "close_public_transit",
                "type": "string",
                "description": "C5 - Ordinal scale to record closing of public transportation; 0 - No measures 1 - Recommend closing (or significantly reduce volume/route/means of transport available) 2 - Require closing (or prohibit most citizens from using it)",
                "mode": "nullable",
            },
            {
                "name": "close_public_transit_flag",
                "type": "string",
                "description": "Are C5 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
                "mode": "nullable",
            },
            {
                "name": "close_public_transit_notes",
                "type": "string",
                "description": "Additional details about C5 policy actions",
                "mode": "nullable",
            },
            {
                "name": "stay_at_home_requirements",
                "type": "string",
                "description": "C6 - Ordinal scale record of orders to “shelter-in- place” and otherwise confine to home.",
                "mode": "nullable",
            },
            {
                "name": "stay_at_home_requirements_flag",
                "type": "string",
                "description": 'Are C6 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank"\\',
                "mode": "nullable",
            },
            {
                "name": "stay_at_home_requirements_notes",
                "type": "string",
                "description": "Additional details about C6 policy actions",
                "mode": "nullable",
            },
            {
                "name": "restrictions_on_internal_movement",
                "type": "string",
                "description": "C7 - Ordinal scale of restrictions on internal movement;  0 - No measures 1 - Recommend closing (or significantly reduce volume/route/means of transport) 2 - Require closing (or prohibit most people from using it)",
                "mode": "nullable",
            },
            {
                "name": "restrictions_on_internal_movement_flag",
                "type": "string",
                "description": "Are C7 actions targeted at specific areas or general:0 - Targeted 1- General No data - blank",
                "mode": "nullable",
            },
            {
                "name": "restrictions_on_internal_movement_notes",
                "type": "string",
                "description": "Additional details about C7 policy actions",
                "mode": "nullable",
            },
            {
                "name": "international_travel_controls",
                "type": "string",
                "description": "C8 - Ordinal scale record of restrictions on international travel; 0 - No measures 1 - Screening 2 - Quarantine arrivals from high-risk regions 3 - Ban on high-risk regions 4 - Total border closure No data - blank",
                "mode": "nullable",
            },
            {
                "name": "international_travel_controls_notes",
                "type": "string",
                "description": "Additional details about C8 policy actions",
                "mode": "nullable",
            },
            {
                "name": "income_support",
                "type": "string",
                "description": "E1 - Ordinal scale record if the government is covering the salaries or providing direct cash payments universal basic income or similar of people who lose their jobs or cannot work. (Includes payments to firms if explicitly linked to payroll/ salaries)",
                "mode": "nullable",
            },
            {
                "name": "income_support_flag",
                "type": "string",
                "description": "Sector scope of E1 actions;  0 - formal sector workers only 1 - transfers to informal sector workers too No data - blank",
                "mode": "nullable",
            },
            {
                "name": "income_support_notes",
                "type": "string",
                "description": "Additional details about E1 policy actions",
                "mode": "nullable",
            },
            {
                "name": "debt_contract_relief",
                "type": "string",
                "description": "E2 - Record if govt. is freezing financial obligations (eg stopping loan repayments preventing services like water from stopping or banning evictions)",
                "mode": "nullable",
            },
            {
                "name": "debt_contract_relief_notes",
                "type": "string",
                "description": "Additional details about E2 policy actions",
                "mode": "nullable",
            },
            {
                "name": "fiscal_measures",
                "type": "float",
                "description": "E3 - What economic stimulus policies are adopted (in USD); Record monetary value USD of fiscal stimuli including spending or tax cuts NOT included in S10 (see below) -If none enter 0 No data - blank Please use the exchange rate of the date you are coding not the current date.",
                "mode": "nullable",
            },
            {
                "name": "fiscal_measures_notes",
                "type": "string",
                "description": "Additional details about E3 policy actions",
                "mode": "nullable",
            },
            {
                "name": "international_support",
                "type": "float",
                "description": "E4 - Announced offers of COVID-19 related aid spending to other countries (in USD);  Record monetary value announced if additional to previously announced spending -if none enter 0 No data - blank Please use the exchange rate of the date you are coding not the current date.",
                "mode": "nullable",
            },
            {
                "name": "international_support_notes",
                "type": "string",
                "description": "Additional details about E4 policy actions",
                "mode": "nullable",
            },
            {
                "name": "public_information_campaigns",
                "type": "string",
                "description": "H1 - Ordinal scale record presence of public info campaigns;  0 -No COVID-19 public information campaign 1 - public officials urging caution about COVID-19 2 - coordinated public information campaign (e.g. across traditional and social media) No data - blank",
                "mode": "nullable",
            },
            {
                "name": "public_information_campaigns_flag",
                "type": "string",
                "description": "Sector scope of H1 actions;  0 - formal sector workers only 1 - transfers to informal sector workers too No data - blank",
                "mode": "nullable",
            },
            {
                "name": "public_information_campaigns_notes",
                "type": "string",
                "description": "Additional details about H1 policy actions",
                "mode": "nullable",
            },
            {
                "name": "testing_policy",
                "type": "string",
                "description": "H2 - Ordinal scale record of who can get tested;  0 – No testing policy 1 – Only those who both (a) have symptoms AND (b) meet specific criteria (eg key workers admitted to hospital came into contact with a known case returned from overseas) 2 – testing of anyone showing COVID-19 symptoms 3 – open public testing (eg “drive through” testing available to asymptomatic people) No data Nb we are looking for policies about testing for having an infection (PCR tests) - not for policies about testing for immunity (antibody tests).",
                "mode": "nullable",
            },
            {
                "name": "testing_policy_notes",
                "type": "string",
                "description": "Additional details about H2 policy actions",
                "mode": "nullable",
            },
            {
                "name": "contact_tracing",
                "type": "string",
                "description": "H3 - Ordinal scale record if governments doing contact tracing; 0 - No contact tracing 1 - Limited contact tracing - not done for all cases 2 - Comprehensive contact tracing - done for all cases No data",
                "mode": "nullable",
            },
            {
                "name": "contact_tracing_notes",
                "type": "string",
                "description": "Additional details about H3 policy actions",
                "mode": "nullable",
            },
            {
                "name": "emergency_healthcare_investment",
                "type": "float",
                "description": "H4 - Short-term spending on e.g hospitals masks etc in USD; Record monetary value in USD of new short-term spending on health. If none enter 0. No data - blank Please use the exchange rate of the date you are coding not the current date.",
                "mode": "nullable",
            },
            {
                "name": "emergency_healthcare_investment_notes",
                "type": "string",
                "description": "Additional details about H4 policy actions",
                "mode": "nullable",
            },
            {
                "name": "vaccine_investment",
                "type": "float",
                "description": "H5 - Announced public spending on vaccine development in USD; Record monetary value in USD of new short-term spending on health. If none enter 0. No data - blank Please use the exchange rate of the date you are coding not the current date.",
                "mode": "nullable",
            },
            {
                "name": "vaccine_investment_notes",
                "type": "string",
                "description": "Additional details about H5 policy actions",
                "mode": "nullable",
            },
            {
                "name": "misc_wildcard",
                "type": "string",
                "description": "M1 - Record policy announcements that do not fit anywhere else",
                "mode": "nullable",
            },
            {
                "name": "misc_wildcard_notes",
                "type": "string",
                "description": "Additional details about M1 policy actions",
                "mode": "nullable",
            },
            {
                "name": "confirmed_cases",
                "type": "integer",
                "description": "Number of confirmed COVID-19 cases",
                "mode": "nullable",
            },
            {
                "name": "deaths",
                "type": "integer",
                "description": "Number of confirmed COVID-19 deaths",
                "mode": "nullable",
            },
            {
                "name": "stringency_index",
                "type": "float",
                "description": "Used after April 28 2020. Nine-point aggregation of the eight containment and closure indicators as well as H1 (public information campaigns). It reports a number between 0 to 100 that reflects the overall stringency of the governments response. This is a measure of how many of the these nine indicators (mostly around social isolation) a government has acted upon and to what degree.",
                "mode": "nullable",
            },
        ],
    )

    oxford_policy_tracker_transform_csv >> load_oxford_policy_tracker_to_bq
