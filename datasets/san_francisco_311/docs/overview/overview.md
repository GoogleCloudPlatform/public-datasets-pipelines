## Overview
This data includes all San Francisco 311 service requests from July 2008 to the present,
and is updated daily.
311 is a non-emergency number that provides access to non-emergency municipal services.

This public dataset is hosted in Google BigQuery and is included in BigQuery's 1TB/mo
of free tier processing. This means that each user receives 1TB of free BigQuery
processing every month, which can be used to run queries on this public dataset.

## Dataset Details

| Attribute                 | Value         |
|---------------------------|---------------|
| Dataset Type              | Tabular       |
| Category                  | Public safety |
| Dataset source            | DataSF        |
| Cloud service             | BigQuery      |
| Expected update frequency | Daily         |

## Main Columns
This dataset has over 20 columns. Here are some of the main columns in the dataset:

| Column       | Type      | Description                                                       |
|--------------|-----------|-------------------------------------------------------------------|
| created_date | TIMESTAMP | The time and date of when the entry was added to the table        |
| closed_date  | TIMESTAMP | The time and date of when the status was changed to `Closed`      |
| status       | STRING    | Either `Open` or `Closed`                                         |
| category     | STRING    | The call category, e.g. `Abandoned Vehicle` or `Tree Maintenance` |
| neighborhood | STRING    | The the neighborhood name for the incident                        |
| latitude     | FLOAT     | The latitude for the incident                                     |
| longitude    | FLOAT     | The longitude for the incident                                    |


## Terms of Service
This dataset is publicly available for anyone to use under the following terms
provided by the Dataset Source - http://sfgov.org/  - and is provided "AS IS"
without any warranty, express or implied, from Google. Google disclaims all
liability for any damages, direct or indirect, resulting from the use of the dataset.
