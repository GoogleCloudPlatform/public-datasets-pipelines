# Changelog

## [5.0.0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v4.2.0...v5.0.0) (2022-07-11)


### ⚠ BREAKING CHANGES

* Upgrade to Airflow 2.2.5 and Python 3.8.12 (#394)

### Datasets

* Onboard Carbon-Free Energy Calculator dataset ([#391](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/391)) ([f3a9447](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/f3a944703c7d53b2d145ddf370fd861825331726))
* Onboard Census Bureau ACS Dataset ([#399](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/399)) ([98e0179](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/98e01799bd47493f3fee18b8e0075b61ff45b007))
* Onboard Fashion MNIST dataset ([#387](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/387)) ([91b7f6a](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/91b7f6ac71a2f5fb569ce1b0c423d683f6c3c447))
* Onboard IMDb dataset ([#406](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/406)) ([2559838](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/25598380b0353c9bba9b6d08c0164691815d2bc1))
* Optimize tests for DAG and Terraform generation ([#395](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/395)) ([ffcd18c](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ffcd18cb2e26f30622f3d1f71832d6c164b2b819))
* Remove co2e columns from Travel Impact Model dataset. ([#400](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/400)) ([d7179ce](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d7179ce9779de978c77c77c96d63fe64e2891e20))


### Bug Fixes

* NOAA - Resolve table field name issue. ([#402](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/402)) ([51860eb](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/51860eb593da8b58b8f9ca69bd30df0e3a506c08))
* Use specific Python version for Airflow 1 tests ([#401](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/401)) ([6fa94a7](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/6fa94a73966440ba26749c539b28a8219b910b60))

## [4.2.0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v4.1.1...v4.2.0) (2022-06-25)


### Datasets

* Onboard COVID-19 dataset from The New York Times ([#383](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/383)) ([9aac451](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/9aac4519bd732fa903113846b6438ffe2ab77e5c))
* Onboard NOAA dataset ([#378](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/378)) ([02cc038](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/02cc038bc108ee96f33ff4b476de282cb9341fb9))
* Onboard San Jose Translation dataset ([#377](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/377)) ([63ea9b9](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/63ea9b9e62bf74f1ebb9e70f52cb8a5298e85753))
* Onboarding MIMIC-III dataset ([#389](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/389)) ([baf6b8d](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/baf6b8d2535f11743de30b462b84811070d50857))
* [datasets/gbif] Add a query to uncover species found in one region only ([#388](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/388)) ([bd5a135](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/bd5a135ef3d67374ea15ebbb6a9f29472fedf79a))


### Features

* Manage local and remote Airflow variables during deployment ([#392](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/392)) ([f26db3a](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/f26db3a30806b17e8386e72b440a7909022f798a))

## [4.1.1](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v4.1.0...v4.1.1) (2022-06-16)


### Datasets

* Onboard IMDB dataset ([#382](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/382)) ([8bf7065](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/8bf7065699ef9519778e640c5168fc876e1f8081))
* Onboard MNIST dataset ([#379](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/379)) ([9809935](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/9809935936866332e425f278ec97b935bdf4a65d))
* Onboard New York Taxi Trips dataset ([#381](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/381)) ([897ac3f](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/897ac3f3352e5dc40e08c5c80e223f877a406394))


### Bug Fixes

* Fixed variable reference to container images for New York dataset ([#380](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/380)) ([e4a6718](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/e4a671850d0eb2512f904d508d739c1aefa16e8c))

## [4.1.0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v4.0.0...v4.1.0) (2022-06-10)


### Datasets

* Onboard City Health Dashboard dataset ([#374](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/374)) ([c7cd9dd](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/c7cd9dd0fd715f04d14f9d183d3b0c7facfcdd14))
* Onboard Cloud Storage Geo Index ([#367](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/367)) ([63cdb2a](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/63cdb2aef0c840bca85de71f2268547468da1606))
* Onboard EPA Historical Air Quality ([#373](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/373)) ([4f4c87e](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/4f4c87edae252059062ba479b80559e7675a885f))
* Onboard IDC v9 dataset ([#364](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/364)) ([bfb9f23](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/bfb9f239368494b7842c0ccde3351a979a77e11c))
* Onboard NOAA datasets ([#353](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/353)) ([0f1c696](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/0f1c696c73a1ccc16ded61de39db6aa8d06806e3))
* Onboard The General Index Dataset ([#342](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/342)) ([67d7216](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/67d7216829ee738e96a92c3d56f3fa0712d10c94))
* Revised COVID-19 Google Mobility dataset ([#363](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/363)) ([ddd3dac](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ddd3dac5d6a9a22bd70f47b10194d6f3d1291c34))


### Documentation Set

* Adds a simple mapping tutorial for the GBIF dataset ([#360](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/360)) ([e7a726a](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/e7a726a486928964042956849124bb1ee12153f1))

## [4.0.0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v3.0.0...v4.0.0) (2022-05-23)


### ⚠ BREAKING CHANGES

* Unified variables and adds support for IAM policies (#341)
* Use poetry over pipenv (#337)

### Datasets

* Onboard Census Opportunity Atlas Dataset ([#263](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/263)) ([13ce71d](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/13ce71d33d60688d2ffbb7c470f4db5bdbd72076))
* Onboard deps.dev (Open Source Insights) dataset ([#356](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/356)) ([12143af](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/12143af2556e84c25c56c61f6bd27b74f3235d92))
* Onboard Diversity Annual Report and complementary datasets ([#358](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/358)) ([4a8a2cd](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/4a8a2cd3fdb7a817b77bff96c958ff3cc97571c8))
* Onboard EPA Historical Air Quality dataset ([#301](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/301)) ([214a56f](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/214a56ff6a60c09eb2cdbd344acbfc06cc6db822))
* Onboard GBIF dataset ([#355](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/355)) ([ab4e208](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ab4e208193d143b6582e662409a4ac14b8a38c83))
* Onboard IDC v8 dataset ([#319](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/319)) ([0f112e0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/0f112e0fa39ee8353f7761f261a382445b22e3e3))
* Onboard International Search Terms for Google Trends ([#323](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/323)) ([855aa7f](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/855aa7fb987944e07b680b08adafab4b85ca67e2))
* Onboard NASA wildfire ([#275](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/275)) ([f593161](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/f5931612c03f13d21f55967349c399de6e2a2780))
* Onboard New York Trees dataset ([#265](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/265)) ([2905308](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/2905308e04b130dde04f870490377251ecfb55f1))
* Onboard Open Targets Genetics dataset  ([#318](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/318)) ([03b4f89](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/03b4f8964127f20a4db34136224ec9e315c8bfbc))
* Onboard Open Targets Platform dataset ([#313](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/313)) ([c5adce6](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/c5adce6ff66ea36545e6611b51fb8183421fb8fd))
* Onboard SEC Failure to Deliver dataset ([#309](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/309)) ([afa6492](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/afa6492c40a8a0f09d67a694c07a2d8841ae3f84))
* Rename Travel Sustainability to Travel Impact Model ([#351](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/351)) ([83df285](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/83df285f0b47041832a138516596953846c12b30))
* Retrieve Composer bucket name when deploying DAGs ([#312](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/312)) ([220f1d5](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/220f1d54f8104ce5c67bd7e0df5f84ec28ebd54a))
* Update BLS - CPSAAT18 with 2021 data ([#357](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/357)) ([a8f8856](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/a8f8856250a6e47565cf1867a2c637976412d9a4))


### Features

* Added functionality to support a data folder to store schema files ([#354](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/354)) ([f893dff](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/f893dffc9a1ecc4294a7def84ffa6b9e151e0048))
* Unified variables and adds support for IAM policies ([#341](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/341)) ([c4a45a0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/c4a45a055437bc860954c0daeb15587537eeaa42))
* Use poetry over pipenv ([#337](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/337)) ([ca43066](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ca43066a64f5ca3a7b32a6c1bd6c461958329ab0))


### Bug Fixes

* Adds packages for docs dependency group ([#339](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/339)) ([6721490](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/6721490f29d18eb0434d48e8722bb3e249e60f0e))
* bump black version due to `click` dependency issue ([#320](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/320)) ([cac6f18](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/cac6f182177cbd24d0068677145e779c6a512878))
* Fix generating BQ views for IDC dataset ([#324](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/324)) ([5896865](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/58968650090975a96510c57342a21bc99ced7a7d))
* Removed unecessary pathlib param from test_deploy_dag ([#345](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/345)) ([45dd0b2](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/45dd0b2c15821e38f0b7b511c253025fc7497ad0))
* thelook_ecommerce - increase # of customers and revised order_items ([#352](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/352)) ([ed1570d](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ed1570d736babf926a6aec1421e3f7b57eb3139b))

## [3.0.0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.8.0...v3.0.0) (2022-03-24)


### ⚠ BREAKING CHANGES

* Reorganize pipelines and infra files into their respective folders (#292)

### Features

* Reorganize pipelines and infra files into their respective folders ([#292](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/292)) ([7408d44](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/7408d4439715907fef63dccc31df51b838e365da))
* Upgrade some pipelines to Airflow 2 and explicitly set pod storage ([#283](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/283)) ([cbc3278](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/cbc3278cbc5cde0ead7f20a475d8b76818658a2e))


### Datasets

* Onboard Broad Genome References dataset ([#316](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/316)) ([4f1f6db](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/4f1f6db5122554355312268acd777924ed43f248))
* Onboard Imaging Data Commons (IDC) v7 dataset ([#287](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/287)) ([dfda5d9](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/dfda5d99e244e7111a8ae9bb5bb361b11046e829))
* Onboard ML dataset ([#276](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/276)) ([48e51af](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/48e51af09bdb5204afbbc1dddb0651dac86c544d))
* Onboard Travel Sustainability dataset ([#280](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/280)) ([8e9731a](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/8e9731a190701452d6fc71f5c58353a0197057d1))
* Onboard Travel Sustainability dataset (schema update) ([#298](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/298)) ([7a13daa](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/7a13daa3a0bd229d86258a775f7388e2e8d7641e))
* Onboarding TheLook E-Commerce dataset ([#294](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/294)) ([15f663a](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/15f663a12edbb6b316c369795ff31ae7f3719336))
* Revise Google Political Ads due to new dataset version ([#317](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/317)) ([6ffb0d0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/6ffb0d0d17aacfc8d72ec3ee55840b51568fdb14))
* Update "location" to GEOGRAPHY type for `datasets/google_trends` schema ([#297](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/297)) ([9d9d3bd](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/9d9d3bd567525eef8cc083ac107321b79dcffaf1))


### Docs

* Docs: Add SF 311 example ([#310](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/310)) ([844a7fb](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/844a7fb5b0045c8d2fdc24a3221140f8546d9cd1))
* Docs: Add a query snippet to calculate the monthly average bike trips for `san_francisco_bikeshare` ([#284](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/284)) ([7a009f6](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/7a009f6ba3b188b4e12cae4afc626d7ae06c212a))
* Docs: Added a template for tutorials ([#299](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/299)) ([ae23d4b](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ae23d4bf4e3692e55eda255802cad88290660081))
* Docs: SF 311 Calls - Predicting the number of calls per category using LSTM ([#293](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/293)) ([88637ca](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/88637cab72125498cdf03d348c05ee15792b3c4a))


### Bug Fixes

* Allow other JSON files to be checked in (such as `schema.json`) ([#281](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/281)) ([2c94b79](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/2c94b79b69046fb8f9c824581393228923da5442))
* Update and fix `city_health_dashboard` dataset ([#285](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/285)) ([4767fed](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/4767fed68e681e8ad9d43e198a716c62d1578e03))

## [2.8.0](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.7.0...v2.8.0) (2022-01-27)


### Features

* Onboard America Health Rankings dataset ([#244](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/244)) ([8ecbfda](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/8ecbfda2ce4dfd279e85606aa8a7d0a3405dbdb3))
* Onboard American Community Survey dataset ([#222](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/222)) ([861d0e6](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/861d0e6bd54acdd3944826b72b7bcf13af839552))
* Onboard Census Opportunity Atlas dataset ([#248](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/248)) ([0e62f27](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/0e62f27d71b8dc8b735b68035e6f63a130b6dc14))
* Onboard Census tract 2019 dataset ([#272](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/272)) ([d2b5e52](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d2b5e527d9d2dcc8e01f5209e7b9409dfe2b62a8))
* Onboard CFPB Complaints dataset ([#225](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/225)) ([9051773](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/90517735463eeee79ce39b2b69e9c8e47e99f4d7))
* Onboard Chronic Disease Indicators dataset ([#242](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/242)) ([48c96f2](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/48c96f2b227c2bb854fefcfeafa0c458afee5372))
* Onboard City Health Dashboard dataset ([#250](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/250)) ([8cc5286](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/8cc528620140e1224348432dbae3ea513f16887c))
* Onboard COVID-19 CDS EU dataset ([#261](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/261)) ([d710dec](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d710dec388bdbfe55a98530274818086df7dd814))
* Onboard EUMETSAT Solar Forecasting dataset ([#273](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/273)) ([db479cf](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/db479cf80002af0714649c69b45336b0e7e3fabe))
* Onboard FDA Drug Enforcement dataset  ([#245](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/245)) ([53c98ac](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/53c98ac3852721434a15fad79f7e4b241a33d2ed))
* Onboard gnomAD dataset ([#264](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/264)) ([804b440](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/804b440b70a203f9d767e94b85501207775e421c))
* Onboard MLCommons Multilingual Spoken Words Corpus (MSWC) dataset ([#252](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/252)) ([ec93997](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ec93997100ef9e85f32df1e1acaf30a73a51cc37))
* Onboard News Hate Crimes dataset ([#238](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/238)) ([9b242ef](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/9b242ef2be005ac37577045099a9a9f5e67fa23a))
* Onboard Race and Economic Opportunity dataset ([#236](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/236)) ([fe6c826](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/fe6c82630a259a294b36a9f881a345725e3dada0))
* Onboarding COVID-19 (UK) Government Response dataset ([#262](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/262)) ([914d39c](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/914d39cdf50ea0b05e2a77d468369ef80037e1b4))
* Update IDC dataset with new views and `v6` version ([#266](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/266)) ([02cae2b](https://github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/02cae2b1d55218b651abac161fe18f6fed8f5842))

## [2.7.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.6.0...v2.7.0) (2021-12-14)


### Datasets

* Onboard CDC Places Dataset ([#241](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/241)) ([e2fcb0c](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/e2fcb0c40c647af918e46c6c0c2cabedcdb4ba58))
* Onboard Cloud Storage Geo Index Dataset ([#219](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/219)) ([27a2c8e](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/27a2c8e356cac8c51aa7b65fae508ad1d7202e9e))
* Onboard EPA historical air quality dataset ([#221](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/221)) ([6267b82](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/6267b828d490ff9d3340320e5ce894d4f29df247))
* Onboard FDA food dataset ([#223](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/223)) ([f0ced96](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/f0ced963ddeeb58313d3e5c777ea6383bb163863))
* Onboard IDC PDP datasets ([#230](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/230)) ([3f944df](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/3f944df14b428ba4e156695237563debbee67b57))


### Features

* Support CloudDataTransferServiceGCSToGCSOperator ([#229](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/229)) ([977b687](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/977b687afc4d66ba2fc3cc68bc8a21dd8c46787e))


### Bug Fixes

* Namespace Terraform resources under dataset names ([#227](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/227)) ([a3f4b34](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/a3f4b34e9fda61ae4bab6bc48c68d0b620ea2c7e))
* Renamed dataset from `sunroof` to `sunroof_solar`  ([#226](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/226)) ([0780df8](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/0780df8c39a53da8b32ff4724f8f51a73938d335))

## [2.6.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.5.0...v2.6.0) (2021-11-04)


### Datasets

* Onboard Austin Waste dataset ([#200](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/200)) ([79dbf5d](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/79dbf5dd406151fd62174f72de2627b9241fd9e9))
* Onboard BLS dataset ([#201](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/201)) ([c7cdd82](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/c7cdd82a55344f5fea68c887a97720e58880b170))
* Onboard Chicago Crime dataset ([#199](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/199)) ([d766547](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d766547c8393c284084641fab113b1f36959ee32))
* Onboard Sunroof Solar dataset ([#166](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/166)) ([375cbae](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/375cbaea0009d56d08b32bddaed274a933e4b781))
* Onboard World Bank Intl Education dataset ([#182](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/182)) ([ff384fd](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/ff384fda3d99512fb03a8f19bff7554811231e05))
* Onboard World Bank WDI dataset ([#198](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/198)) ([cbad321](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/cbad3211ada15d830139328405045a44cdbfb2fe))


### Bug Fixes

* Set `location` field as required for GCS buckets ([#224](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/224)) ([bd8a3db](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/bd8a3dbc95e3fd0244d84d28be8415e98825c586))

## [2.5.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.4.0...v2.5.0) (2021-10-14)


### Datasets

* Onboard Iowa Liquor Sales dataset ([#193](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/193)) ([06848c8](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/06848c899f1efc32f548a5de534ab1f758b6ca2b))
* Onboard San Francisco Bikeshare Station dataset ([#191](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/191)) ([0707012](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/0707012832fdb6995e99563b12815c7de4d88fb7))
* Onboard San Francisco Bikeshare Status dataset ([#192](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/192)) ([e4e1f26](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/e4e1f26f7a2339d5ae5692bdb4608a6958120a36))
* Onboard San Francisco Film Locations dataset ([#190](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/190)) ([2284e09](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/2284e09d7c775d3d9826037f0c8cebd572090f8d))


### Bug Fixes

* Combine `san_francisco_bikeshare_*` folders into `san_francisco_bikeshare` ([#211](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/211)) ([50e4e6d](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/50e4e6d9204dc4c8fa3a427799501687550f9cce))
* Rename `san_francisco_311_service_requests` folder to `san_francisco_311` ([#209](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/209)) ([697f7be](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/697f7be18a4b9376f989b1c8682efdd2c5d239ad))

## [2.4.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.3.1...v2.4.0) (2021-10-08)


### Datasets

* Onboard Austin Crime dataset ([#174](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/174)) ([b4fbaad](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/b4fbaad99e94a052d039c99bc8ca9ad842461e4a))
* Onboard CMS Medicare dataset ([#185](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/185)) ([d0425cd](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d0425cd95a7c56cd788ff5330a791f3677767862))
* Onboard COVID-19 Google Mobility dataset ([#177](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/177)) ([1653a8e](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/1653a8e93f35767e11e4c417a7ee8bcdb953aab4))
* Onboard New York datasets: 311 Service Requests, Citibike Stations, and Tree Census ([#167](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/167)) ([d1f1d7c](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/d1f1d7c00ea8572af91bd2e62e8165c838d67a57))
* Onboard San Francisco 311 Service Requests dataset ([#184](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/184)) ([a8ba2e9](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/a8ba2e99d0a0019c00c0e1759861135ff084a306))
* Onboard San Francisco Street Trees dataset ([#176](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/176)) ([7da5061](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/7da5061cd86c11e6bf8ac87c0ba9b7ab6b48c811))
* Onboard World Bank Health Population dataset ([#178](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/178)) ([4aba767](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/4aba767c13257a078311d53391ac982303546632))
* Onboard World Bank International Debt dataset ([#179](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/179)) ([5ebbabb](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/5ebbabb159f8fd776d92d43c7e0983a9da4c55d2))


### Features

* Support specifying an alternate BQ dataset_id for BQ tables ([#203](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/203)) ([9115e82](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/9115e82502fb1664023870cb332454900f41d008))

### [2.3.1](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.3.0...v2.3.1) (2021-09-28)


### Bug Fixes

* Delete temp GCS objects generated by gsutil's parallel composite upload for `geos_fp` dataset ([#195](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/195)) ([f307cce](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/f307ccefbe60895e8eced4c5040d1629c8486f9e))
* Use patched `flask-openid` version to fix failing builds ([#188](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/188)) ([1ea15a0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/1ea15a08ddf41babe5ef145571ebd5fbba4eb657))

## [2.3.0](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/compare/v2.2.0...v2.3.0) (2021-09-10)


### Datasets

* Onboard `google_political_ads.advertiser_geo_spend` dataset ([#154](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/154)) ([2201ebe](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/2201ebe017ed1419bee3cd1403622c92d832ef78))
* Onboard Austin Bikeshare dataset ([#156](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/156)) ([0bd5659](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/0bd5659b2c6467eb28244b14eb73cddfdabd9f86))
* Onboard NOAA's GSOD Stations and Lightning Strikes datasets ([#158](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/158)) ([8371856](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/83718569b7094bdf48fa9e8c9504368f17ceda94))


### Features

* Support Dataflow operator and job requirements ([#153](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/issues/153)) ([119f8fb](https://www.github.com/GoogleCloudPlatform/public-datasets-pipelines/commit/119f8fb9bcc747b3f544150864f3a22164da708e))

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
