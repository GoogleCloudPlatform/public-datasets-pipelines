/**
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


resource "google_bigquery_table" "census_opportunity_atlas_tract_outcomes" {
  project    = var.project_id
  dataset_id = "census_opportunity_atlas"
  table_id   = "tract_outcomes"

  description = "tract_outcomesspc"



  schema = <<EOF
    [
  {
    "name": "state"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "county"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "tract"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_natam_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_natam_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_asian_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_asian_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_black_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_black_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_hisp_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_hisp_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_other_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_other_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_pooled_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_pooled_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_white_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_white_female"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_natam_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_natam_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_asian_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_asian_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_black_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_black_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_hisp_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_hisp_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_other_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_other_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_pooled_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_pooled_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_white_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_white_male"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_natam_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_natam_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_asian_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_asian_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_black_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_black_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_hisp_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_hisp_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_other_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_other_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_pooled_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_pooled_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_below_median_white_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "frac_years_xw_white_pooled"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_p1"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_p25"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_p50"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_p75"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_p100"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_mean"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_p10"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_hisp_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_hisp_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_white_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_white_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_black_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_black_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_natam_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_natam_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_asian_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_asian_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_pooled_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_pooled_male_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_pooled_female_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_white_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_black_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_asian_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_hisp_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_natam_pooled_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_pooled_pooled_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_white_pooled_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_black_pooled_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_hisp_pooled_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_asian_pooled_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_natam_pooled_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_pooled_male_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_white_male_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_black_male_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_hisp_male_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_asian_male_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_natam_male_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_pooled_female_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_white_female_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_black_female_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_hisp_female_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_asian_female_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kid_natam_female_blw_p50_n"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "cz"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "czname"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_p25_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_p75_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_asian_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_black_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_hisp_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_natam_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_other_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_pooled_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "teenbrth_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_white_female_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_asian_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_black_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_hisp_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_natam_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_other_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_pooled_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_white_male_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_asian_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_black_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_hisp_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_natam_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_other_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_pooled_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_24_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_24_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_24_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_26_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_26_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_26_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_29_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_29_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_29_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "marr_32_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_32_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_26_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_29_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "work_24_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top20_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top20_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_top01_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_top01_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "married_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "lpov_nbh_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "two_par_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_dad_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "has_mom_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "jail_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staytract_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "staycz_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "stayhome_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "working_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kir_stycz_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "kfr_stycz_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "spouse_rk_white_pooled_mean_se"
    "type": "INTEGER"
    "mode": "NULLABLE"
  },
  {
    "name": "par_rank_white_pooled_mean_e"
    "type": "INTEGER"
    "mode": "NULLABLE"
  }
]
    EOF
  depends_on = [
    google_bigquery_dataset.census_opportunity_atlas
  ]
}

output "bigquery_table-census_opportunity_atlas_tract_outcomes-table_id" {
  value = google_bigquery_table.census_opportunity_atlas_tract_outcomes.table_id
}

output "bigquery_table-census_opportunity_atlas_tract_outcomes-id" {
  value = google_bigquery_table.census_opportunity_atlas_tract_outcomes.id
}
