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
from airflow.contrib.operators import bigquery_operator

default_args = {
    "owner": "Google",
    "depends_on_past": False,
    "start_date": "2021-06-01",
}


with DAG(
    dag_id="iowa_liquor_sales_forecasting.2020_sales_train",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="@once",
    catchup=False,
    default_view="graph",
) as dag:

    # Task to run a BigQueryOperator
    sample_iowa_liquor_sales_2020 = bigquery_operator.BigQueryOperator(
        task_id="sample_iowa_liquor_sales_2020",
        sql='SELECT date, store_name, MAX(city) as city, MAX(zip_code) as zip_code, MAX(county) as county, SUM(sale_dollars) AS sale_dollars FROM `bigquery-public-data.iowa_liquor_sales.sales` WHERE REGEXP_CONTAINS(CAST(date AS String), "2020-") GROUP BY date, store_name',
        use_legacy_sql=False,
        destination_dataset_table="iowa_liquor_sales_forecasting.2020_sales_train",
        write_disposition="WRITE_TRUNCATE",
    )

    sample_iowa_liquor_sales_2020
