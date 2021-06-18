# Changelog

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
