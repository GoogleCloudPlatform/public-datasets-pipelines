# Changelog

## [2.2.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.1.0...v2.2.0) (2021-08-27)


### Datasets

* Onboard COVID19-Italy dataset ([#148](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/148)) ([f56b5f2](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/f56b5f22ab5ecf350e20684a7ebabc01a0340340))
* Onboard GEOS-FP dataset ([#130](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/130)) ([d32f46b](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d32f46ba70b38c06d1cbe4d9448f65a4daf65671))
* Onboard Google CFE dataset ([#146](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/146)) ([9bca8ef](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/9bca8ef4562d81a3f8bf1353db91276be10c72d6))
* Onboard Google Political Ads dataset ([#149](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/149)) ([5903253](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/590325353878e740c3b86c4e83a6501d8caf1635))
* Onboard IRS 990 dataset ([#150](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/150)) ([1105eed](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/1105eed502abfed9615f3bc1a599a4f17bdb86fc))


### Bug Fixes

* Regenerate Terraform files for Google Political Ads ([#152](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/152)) ([102f8e5](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/102f8e5ef5aa64375eb2a193f2e593454bb96828))
* shared_variables.json should not be reset when deploying ([#147](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/147)) ([a6754df](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/a6754df4abfbfef0ba37e14a997c75b950bf5781))

## [2.1.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.0.0...v2.1.0) (2021-08-13)


### Datasets

* Onboard Google Cloud Release Notes dataset ([#133](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/133)) ([5c98c05](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/5c98c052ea74b7cb474a6bc86ea25e1cffe8cb9a))


### Bug Fixes

* Revised Airflow DB initialization command ([#141](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/141)) ([47b4717](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/47b47172f331b9096a98083dfefe31d81dc79696))

## [2.0.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.11.0...v2.0.0) (2021-08-11)


### ⚠ BREAKING CHANGES

* Pipeline YAML template using Airflow 2 operators (#138)
* Adds support for Airflow 2 Cloud Composer environment and operators (#134)

### Features

* Adds support for Airflow 2 Cloud Composer environment and operators ([#134](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/134)) ([b2749c6](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/b2749c61fc62cfc97b81831f664022c354bc8de9))
* Pipeline YAML template using Airflow 2 operators ([#138](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/138)) ([90ae7cd](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/90ae7cd5a3eec5da2d790233425c4e98530b25ac))

## [1.11.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.10.0...v1.11.0) (2021-07-22)


### Features

* Adds Google license header bot config ([#106](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/106)) ([d587689](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d5876898c96436400d940e754ed2fce4eda8ba4f))
* Use a single file for shared Airflow variables ([#122](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/122)) ([f5d227d](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/f5d227de7d30439e80346612856723292c6f46e7))

## [1.10.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.9.0...v1.10.0) (2021-07-21)


### Datasets

* Onboard USA names dataset ([#96](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/96)) ([eb28f0f](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/eb28f0f0247278febea955ecb4081c09b634e97b))

## [1.9.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.8.0...v1.9.0) (2021-07-15)


### Datasets

* Onboard Vaccination Search Insights dataset ([#113](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/113)) ([ad39cfa](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ad39cfa45fa1d2fecc228874b8b9e8b0fb44236e))


### Features

* Support partitioning, clustering, and protection properties for BQ tables ([#116](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/116)) ([288c5a2](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/288c5a2476f61079f226c2f2c21390489dbab4a6))

## [1.8.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.7.0...v1.8.0) (2021-07-01)


### Features

* Onboard Google Diversity Annual Report 2021 dataset ([#111](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/111)) ([13ebee9](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/13ebee906c52ec60959bbe3f8e0d6190f7934f9d))

## [1.7.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.6.0...v1.7.0) (2021-06-24)


### Datasets

* Onboard BLS - CPSAAT 2020 dataset ([#105](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/105)) ([61f4394](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/61f439493fcf24d8d9a29362a8498b38389686ef))


### Bug Fixes

* Allow newline and quotes for BQ dataset and table descriptions ([#103](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/103)) ([ef01fe6](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ef01fe6c176c5d3cbecd14a173efd6ad45fc2805))

## [1.6.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.5.1...v1.6.0) (2021-06-17)


### Datasets

* Onboard Google Trends dataset for top N terms ([#92](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/92)) ([df96d1d](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/df96d1d2f936bb4c7213cb9a4ef9ec90ff02fbad))


### Bug Fixes

* Allow DAG deploys without `variables.json` ([#91](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/91)) ([8eaaae9](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/8eaaae9e69a8f33086083311efd4cb4359c7ac39))

### [1.5.1](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.5.0...v1.5.1) (2021-06-15)


### Bug Fixes

* Fix BigQuery dataset descriptions for `covid19_tracking` and `ml_datasets`  ([#83](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/83)) ([b5b7640](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/b5b7640bd35534ce64a17e9a0a82b88cbeb9dfd0))

## [1.5.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.4.1...v1.5.0) (2021-06-14)


### Datasets

* Onboard Iowa liquor sales forecasting samples for Vertex AI Forecasting tutorial ([#85](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/85)) ([d832327](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d8323277a96ff0b7c8e032fa823da3d431069fb9))


### Features

* Support BigQueryToBigQueryOperator ([#86](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/86)) ([fd26476](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/fd26476b78bc013d7192a8e6dbd6278be991a0f4))

### [1.4.1](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.4.0...v1.4.1) (2021-06-09)


### Bug Fixes

* Update `covid19_vaccination_access` tables to use `facility_country_region_code` column ([#80](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/80)) ([6d01c95](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/6d01c953bd53f728cf50f2f712be5b442a59e50a))

## [1.4.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.3.0...v1.4.0) (2021-06-08)


### Datasets

* Onboard COVID-19 Vaccination Access dataset ([#74](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/74)) ([e68b4f8](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/e68b4f87c19e1c1d1c370c042861fb17d6d89957))


### Bug Fixes

* Fix issue where Terraform resource names can't start with digits, but BQ tables can ([#70](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/70)) ([7c0f339](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/7c0f339f20ca1384eab96a4a3f9cb784f63ab52d))

## [1.3.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.2.0...v1.3.0) (2021-06-08)


### Features

* Support BigQuery table descriptions ([#59](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/59)) ([4b364a1](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/4b364a1c02fc6abef7d4b7884c14eef14c988fd6))

## [1.2.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.1.0...v1.2.0) (2021-06-02)


### Features

* Configure Renovate ([#36](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/36)) ([d6fd93b](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d6fd93be13de29e83254072e082d20c36e7b4991))
* Support deploying a single pipeline in a dataset ([#46](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/46)) ([8bdb8d7](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/8bdb8d797beaa1f44e0fd6c93864474cd535ab36))
* Support Terraform remote state when generating GCP resources ([#39](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/39)) ([9e01936](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/9e0193695262646a04dabb04a866712a070688d4))

## [1.1.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v1.0.0...v1.1.0) (2021-05-26)


### Features

* Support building and pushing container images shared within a dataset folder ([#27](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/27)) ([de9d1b9](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/de9d1b9550e3986abb4e3b41d634a5b35b872582))
* support user-supplied bucket name prefix ([#23](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/23)) ([610a9b7](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/610a9b76827b3e4562bf6c33422b9274352ca0f2))


### Bug Fixes

* Add missing link to YAML config reference ([#38](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/38)) ([30bfc32](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/30bfc32108007a3c8b2fca87f7b24e9de03590c6))

## 1.0.0 (2021-04-30)


### Datasets

* added [The COVID Tracking Project](https://covidtracking.com/) dataset 
* added Vizgen MERFISH Mouse Brain Map dataset ([#17]([https://github.com/GoogleCloudPlatform/public-datasets-pipelines/pull/17))
* added Penguins dataset for ML tutorial ([#15](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/pull/15))

### Bug Fixes

* removes Makefile ([#18](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/18)) ([97a2f30](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/97a2f30d8009160e9b71abad80c50fdd5bcf1e70))
* use env name as a variable for GCS Terraform resources ([#4](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/pull/4))
