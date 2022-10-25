/**
 * Copyright 2022 Google LLC
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


resource "google_bigquery_table" "ebi_chembl_action_type_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "action_type_30"
  description = "Table storing the distinct list of action types used in the drug_mechanism table, together with a higher-level parent action type."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_action_type_30-table_id" {
  value = google_bigquery_table.ebi_chembl_action_type_30.table_id
}

output "bigquery_table-ebi_chembl_action_type_30-id" {
  value = google_bigquery_table.ebi_chembl_action_type_30.id
}

resource "google_bigquery_table" "ebi_chembl_activities_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "activities_30"
  description = "Activity \u0027values\u0027 or \u0027end points\u0027  that are the results of an assay recorded in a scientific document. Each activity is described by a row."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_activities_30-table_id" {
  value = google_bigquery_table.ebi_chembl_activities_30.table_id
}

output "bigquery_table-ebi_chembl_activities_30-id" {
  value = google_bigquery_table.ebi_chembl_activities_30.id
}

resource "google_bigquery_table" "ebi_chembl_activity_properties_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "activity_properties_30"
  description = "Table storing parameters and properties of Activity_IDs in the ACTIVITIES table - can be either independent variables that do not apply to the whole assay (e.g., compounds \u0027DOSE\u0027), or dependent variables/results that are important in interpreting the activity values (e.g., \u0027HILL_SLOPE\u0027)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_activity_properties_30-table_id" {
  value = google_bigquery_table.ebi_chembl_activity_properties_30.table_id
}

output "bigquery_table-ebi_chembl_activity_properties_30-id" {
  value = google_bigquery_table.ebi_chembl_activity_properties_30.id
}

resource "google_bigquery_table" "ebi_chembl_activity_smid_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "activity_smid_30"
  description = "A join table between ACTIVITY_SUPP_MAP and ACTIVITY_SUPP"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_activity_smid_30-table_id" {
  value = google_bigquery_table.ebi_chembl_activity_smid_30.table_id
}

output "bigquery_table-ebi_chembl_activity_smid_30-id" {
  value = google_bigquery_table.ebi_chembl_activity_smid_30.id
}

resource "google_bigquery_table" "ebi_chembl_activity_stds_lookup_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "activity_stds_lookup_30"
  description = "Table storing details of standardised activity types and units, with permitted value ranges. Used to determine the correct standard_type and standard_units for a range of published types/units."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_activity_stds_lookup_30-table_id" {
  value = google_bigquery_table.ebi_chembl_activity_stds_lookup_30.table_id
}

output "bigquery_table-ebi_chembl_activity_stds_lookup_30-id" {
  value = google_bigquery_table.ebi_chembl_activity_stds_lookup_30.id
}

resource "google_bigquery_table" "ebi_chembl_activity_supp_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "activity_supp_30"
  description = "Supplementary / Supporting Data for ACTIVITIES - can be linked via ACTIVITY_SMID and ACTIVITY_SUPP_MAP tables"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_activity_supp_30-table_id" {
  value = google_bigquery_table.ebi_chembl_activity_supp_30.table_id
}

output "bigquery_table-ebi_chembl_activity_supp_30-id" {
  value = google_bigquery_table.ebi_chembl_activity_supp_30.id
}

resource "google_bigquery_table" "ebi_chembl_activity_supp_map_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "activity_supp_map_30"
  description = "Mapping table, linking supplementary / supporting data from the ACTIVITY_SUPP table to the main ACTIVITIES table"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_activity_supp_map_30-table_id" {
  value = google_bigquery_table.ebi_chembl_activity_supp_map_30.table_id
}

output "bigquery_table-ebi_chembl_activity_supp_map_30-id" {
  value = google_bigquery_table.ebi_chembl_activity_supp_map_30.id
}

resource "google_bigquery_table" "ebi_chembl_assay_class_map_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "assay_class_map_30"
  description = "Mapping table linking assays to classes in the ASSAY_CLASSIFICATION table"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_assay_class_map_30-table_id" {
  value = google_bigquery_table.ebi_chembl_assay_class_map_30.table_id
}

output "bigquery_table-ebi_chembl_assay_class_map_30-id" {
  value = google_bigquery_table.ebi_chembl_assay_class_map_30.id
}

resource "google_bigquery_table" "ebi_chembl_assay_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "assay_classification_30"
  description = "Classification scheme for phenotypic assays e.g., by therapeutic area, phenotype/process and assay type. Can be used to find standard assays for a particular disease area or phenotype e.g., anti-obesity assays. Currently data are available only for in vivo efficacy assays"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_assay_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_assay_classification_30.table_id
}

output "bigquery_table-ebi_chembl_assay_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_assay_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_assay_parameters_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "assay_parameters_30"
  description = "Table storing additional parameters for an assay e.g., dose, administration route, time point"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_assay_parameters_30-table_id" {
  value = google_bigquery_table.ebi_chembl_assay_parameters_30.table_id
}

output "bigquery_table-ebi_chembl_assay_parameters_30-id" {
  value = google_bigquery_table.ebi_chembl_assay_parameters_30.id
}

resource "google_bigquery_table" "ebi_chembl_assay_type_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "assay_type_30"
  description = "Description of assay types (e.g., Binding, Functional, ADMET)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_assay_type_30-table_id" {
  value = google_bigquery_table.ebi_chembl_assay_type_30.table_id
}

output "bigquery_table-ebi_chembl_assay_type_30-id" {
  value = google_bigquery_table.ebi_chembl_assay_type_30.id
}

resource "google_bigquery_table" "ebi_chembl_assays_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "assays_30"
  description = "Table storing a list of the assays that are reported in each document. Similar assays from different publications will appear as distinct assays in this table."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_assays_30-table_id" {
  value = google_bigquery_table.ebi_chembl_assays_30.table_id
}

output "bigquery_table-ebi_chembl_assays_30-id" {
  value = google_bigquery_table.ebi_chembl_assays_30.id
}

resource "google_bigquery_table" "ebi_chembl_atc_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "atc_classification_30"
  description = "WHO ATC Classification for drugs"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_atc_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_atc_classification_30.table_id
}

output "bigquery_table-ebi_chembl_atc_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_atc_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_binding_sites_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "binding_sites_30"
  description = "Table storing details of binding sites for a target. A target may have multiple sites defined in this table."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_binding_sites_30-table_id" {
  value = google_bigquery_table.ebi_chembl_binding_sites_30.table_id
}

output "bigquery_table-ebi_chembl_binding_sites_30-id" {
  value = google_bigquery_table.ebi_chembl_binding_sites_30.id
}

resource "google_bigquery_table" "ebi_chembl_bio_component_sequences_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "bio_component_sequences_30"
  description = "Table storing the sequences for biotherapeutic drugs (e.g., monoclonal antibodies, recombinant proteins, peptides etc. For multi-chain biotherapeutics (e.g., mAbs) each chain is stored here as a separate component."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_bio_component_sequences_30-table_id" {
  value = google_bigquery_table.ebi_chembl_bio_component_sequences_30.table_id
}

output "bigquery_table-ebi_chembl_bio_component_sequences_30-id" {
  value = google_bigquery_table.ebi_chembl_bio_component_sequences_30.id
}

resource "google_bigquery_table" "ebi_chembl_bioassay_ontology_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "bioassay_ontology_30"
  description = "Lookup table providing labels for Bioassay Ontology terms used in assays and activities tables"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_bioassay_ontology_30-table_id" {
  value = google_bigquery_table.ebi_chembl_bioassay_ontology_30.table_id
}

output "bigquery_table-ebi_chembl_bioassay_ontology_30-id" {
  value = google_bigquery_table.ebi_chembl_bioassay_ontology_30.id
}

resource "google_bigquery_table" "ebi_chembl_biotherapeutic_components_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "biotherapeutic_components_30"
  description = "Links each biotherapeutic drug (in the biotherapeutics table) to its component sequences (in the bio_component_sequences table). A biotherapeutic drug can have multiple components and hence multiple rows in this table. Similarly, a particular component sequence can be part of more than one drug."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_biotherapeutic_components_30-table_id" {
  value = google_bigquery_table.ebi_chembl_biotherapeutic_components_30.table_id
}

output "bigquery_table-ebi_chembl_biotherapeutic_components_30-id" {
  value = google_bigquery_table.ebi_chembl_biotherapeutic_components_30.id
}

resource "google_bigquery_table" "ebi_chembl_biotherapeutics_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "biotherapeutics_30"
  description = "Stores sequence information/descriptions for protein therapeutics, including recombinant proteins, peptides and antibodies"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_biotherapeutics_30-table_id" {
  value = google_bigquery_table.ebi_chembl_biotherapeutics_30.table_id
}

output "bigquery_table-ebi_chembl_biotherapeutics_30-id" {
  value = google_bigquery_table.ebi_chembl_biotherapeutics_30.id
}

resource "google_bigquery_table" "ebi_chembl_cell_dictionary_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "cell_dictionary_30"
  description = "Table storing information for cell lines in the target_dictionary (e.g., tissue/species origin). Cell_name should match pref_name in target_dictionary."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_cell_dictionary_30-table_id" {
  value = google_bigquery_table.ebi_chembl_cell_dictionary_30.table_id
}

output "bigquery_table-ebi_chembl_cell_dictionary_30-id" {
  value = google_bigquery_table.ebi_chembl_cell_dictionary_30.id
}

resource "google_bigquery_table" "ebi_chembl_chembl_id_lookup_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "chembl_id_lookup_30"
  description = "Lookup table storing chembl identifiers for different entities in the database (assays, compounds, documents and targets)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_chembl_id_lookup_30-table_id" {
  value = google_bigquery_table.ebi_chembl_chembl_id_lookup_30.table_id
}

output "bigquery_table-ebi_chembl_chembl_id_lookup_30-id" {
  value = google_bigquery_table.ebi_chembl_chembl_id_lookup_30.id
}

resource "google_bigquery_table" "ebi_chembl_component_class_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "component_class_30"
  description = "Links protein components of targets to the protein_family_classification table. A protein can have more than one classification (e.g., Membrane receptor and Enzyme)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_component_class_30-table_id" {
  value = google_bigquery_table.ebi_chembl_component_class_30.table_id
}

output "bigquery_table-ebi_chembl_component_class_30-id" {
  value = google_bigquery_table.ebi_chembl_component_class_30.id
}

resource "google_bigquery_table" "ebi_chembl_component_domains_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "component_domains_30"
  description = "Links protein components of targets to the structural domains they contain (from the domains table). Contains information showing the start and end position of the domain in the component sequence."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_component_domains_30-table_id" {
  value = google_bigquery_table.ebi_chembl_component_domains_30.table_id
}

output "bigquery_table-ebi_chembl_component_domains_30-id" {
  value = google_bigquery_table.ebi_chembl_component_domains_30.id
}

resource "google_bigquery_table" "ebi_chembl_component_go_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "component_go_30"
  description = "Table mapping protein components in the COMPONENT_SEQUENCES table to the GO slim terms stored in the GO_CLASSIFICATION table"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_component_go_30-table_id" {
  value = google_bigquery_table.ebi_chembl_component_go_30.table_id
}

output "bigquery_table-ebi_chembl_component_go_30-id" {
  value = google_bigquery_table.ebi_chembl_component_go_30.id
}

resource "google_bigquery_table" "ebi_chembl_component_sequences_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "component_sequences_30"
  description = "Table storing the sequences for components of molecular targets (e.g., protein sequences), along with other details taken from sequence databases (e.g., names, accessions). Single protein targets will have a single protein component in this table, whereas protein complexes/protein families will have multiple protein components."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_component_sequences_30-table_id" {
  value = google_bigquery_table.ebi_chembl_component_sequences_30.table_id
}

output "bigquery_table-ebi_chembl_component_sequences_30-id" {
  value = google_bigquery_table.ebi_chembl_component_sequences_30.id
}

resource "google_bigquery_table" "ebi_chembl_component_synonyms_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "component_synonyms_30"
  description = "Table storing synonyms for the components of molecular targets (e.g., names, acronyms, gene symbols etc.) Please note: EC numbers are also currently included in this table although they are not strictly synonyms and can apply to multiple proteins."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_component_synonyms_30-table_id" {
  value = google_bigquery_table.ebi_chembl_component_synonyms_30.table_id
}

output "bigquery_table-ebi_chembl_component_synonyms_30-id" {
  value = google_bigquery_table.ebi_chembl_component_synonyms_30.id
}

resource "google_bigquery_table" "ebi_chembl_compound_properties_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "compound_properties_30"
  description = "Table storing calculated physicochemical properties for compounds, now calculated with RDKit and ChemAxon software (note all but FULL_MWT and FULL_MOLFORMULA are calculated on the parent structure)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_compound_properties_30-table_id" {
  value = google_bigquery_table.ebi_chembl_compound_properties_30.table_id
}

output "bigquery_table-ebi_chembl_compound_properties_30-id" {
  value = google_bigquery_table.ebi_chembl_compound_properties_30.id
}

resource "google_bigquery_table" "ebi_chembl_compound_records_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "compound_records_30"
  description = "Represents each compound extracted from scientific documents."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_compound_records_30-table_id" {
  value = google_bigquery_table.ebi_chembl_compound_records_30.table_id
}

output "bigquery_table-ebi_chembl_compound_records_30-id" {
  value = google_bigquery_table.ebi_chembl_compound_records_30.id
}

resource "google_bigquery_table" "ebi_chembl_compound_structural_alerts_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "compound_structural_alerts_30"
  description = "Table showing which structural alerts (as defined in the STRUCTURAL_ALERTS table) are found in a particular ChEMBL compound. It should be noted some alerts/alert sets are more permissive than others and may flag a large number of compounds. Results should be interpreted with care, depending on the use-case, and not treated as a blanket filter (e.g., around 50% of approved drugs have 1 or more alerts from these sets)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_compound_structural_alerts_30-table_id" {
  value = google_bigquery_table.ebi_chembl_compound_structural_alerts_30.table_id
}

output "bigquery_table-ebi_chembl_compound_structural_alerts_30-id" {
  value = google_bigquery_table.ebi_chembl_compound_structural_alerts_30.id
}

resource "google_bigquery_table" "ebi_chembl_compound_structures_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "compound_structures_30"
  description = "Table storing various structure representations (e.g., Molfile, InChI) for each compound"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_compound_structures_30-table_id" {
  value = google_bigquery_table.ebi_chembl_compound_structures_30.table_id
}

output "bigquery_table-ebi_chembl_compound_structures_30-id" {
  value = google_bigquery_table.ebi_chembl_compound_structures_30.id
}

resource "google_bigquery_table" "ebi_chembl_confidence_score_lookup_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "confidence_score_lookup_30"
  description = "Lookup table describing how assay2target confidence scores are assigned depending on the type of target(s) assigned to the assay and the level of confidence in their molecular identity"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_confidence_score_lookup_30-table_id" {
  value = google_bigquery_table.ebi_chembl_confidence_score_lookup_30.table_id
}

output "bigquery_table-ebi_chembl_confidence_score_lookup_30-id" {
  value = google_bigquery_table.ebi_chembl_confidence_score_lookup_30.id
}

resource "google_bigquery_table" "ebi_chembl_curation_lookup_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "curation_lookup_30"
  description = "Lookup table for assays.curated_by column. Shows level of curation that has been applied to the assay to target mapping."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_curation_lookup_30-table_id" {
  value = google_bigquery_table.ebi_chembl_curation_lookup_30.table_id
}

output "bigquery_table-ebi_chembl_curation_lookup_30-id" {
  value = google_bigquery_table.ebi_chembl_curation_lookup_30.id
}

resource "google_bigquery_table" "ebi_chembl_data_validity_lookup_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "data_validity_lookup_30"
  description = "Table storing information about the data_validity_comment values used in the activities table."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_data_validity_lookup_30-table_id" {
  value = google_bigquery_table.ebi_chembl_data_validity_lookup_30.table_id
}

output "bigquery_table-ebi_chembl_data_validity_lookup_30-id" {
  value = google_bigquery_table.ebi_chembl_data_validity_lookup_30.id
}

resource "google_bigquery_table" "ebi_chembl_defined_daily_dose_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "defined_daily_dose_30"
  description = "WHO DDD (defined daily dose) information"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_defined_daily_dose_30-table_id" {
  value = google_bigquery_table.ebi_chembl_defined_daily_dose_30.table_id
}

output "bigquery_table-ebi_chembl_defined_daily_dose_30-id" {
  value = google_bigquery_table.ebi_chembl_defined_daily_dose_30.id
}

resource "google_bigquery_table" "ebi_chembl_docs_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "docs_30"
  description = "Holds all scientific documents (journal articles or patents) from which assays have been extracted."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_docs_30-table_id" {
  value = google_bigquery_table.ebi_chembl_docs_30.table_id
}

output "bigquery_table-ebi_chembl_docs_30-id" {
  value = google_bigquery_table.ebi_chembl_docs_30.id
}

resource "google_bigquery_table" "ebi_chembl_domains_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "domains_30"
  description = "Table storing a non-redundant list of domains found in protein targets (e.g., Pfam domains)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_domains_30-table_id" {
  value = google_bigquery_table.ebi_chembl_domains_30.table_id
}

output "bigquery_table-ebi_chembl_domains_30-id" {
  value = google_bigquery_table.ebi_chembl_domains_30.id
}

resource "google_bigquery_table" "ebi_chembl_drug_indication_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "drug_indication_30"
  description = "Table storing indications for drugs from a variety of sources (e.g., ATC, DailyMed, ClinicalTrials.gov)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_drug_indication_30-table_id" {
  value = google_bigquery_table.ebi_chembl_drug_indication_30.table_id
}

output "bigquery_table-ebi_chembl_drug_indication_30-id" {
  value = google_bigquery_table.ebi_chembl_drug_indication_30.id
}

resource "google_bigquery_table" "ebi_chembl_drug_mechanism_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "drug_mechanism_30"
  description = "Table storing mechanism of action information for FDA-approved drugs and WHO anti-malarials"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_drug_mechanism_30-table_id" {
  value = google_bigquery_table.ebi_chembl_drug_mechanism_30.table_id
}

output "bigquery_table-ebi_chembl_drug_mechanism_30-id" {
  value = google_bigquery_table.ebi_chembl_drug_mechanism_30.id
}

resource "google_bigquery_table" "ebi_chembl_drug_warning_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "drug_warning_30"
  description = "Table storing safety-related information for drugs and clinical candidates"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_drug_warning_30-table_id" {
  value = google_bigquery_table.ebi_chembl_drug_warning_30.table_id
}

output "bigquery_table-ebi_chembl_drug_warning_30-id" {
  value = google_bigquery_table.ebi_chembl_drug_warning_30.id
}

resource "google_bigquery_table" "ebi_chembl_formulations_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "formulations_30"
  description = "Table linking individual ingredients in approved products (and their strengths) to entries in the molecule dictionary. Where products are mixtures of active ingredients they will have multiple entries in this table"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_formulations_30-table_id" {
  value = google_bigquery_table.ebi_chembl_formulations_30.table_id
}

output "bigquery_table-ebi_chembl_formulations_30-id" {
  value = google_bigquery_table.ebi_chembl_formulations_30.id
}

resource "google_bigquery_table" "ebi_chembl_frac_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "frac_classification_30"
  description = "Table showing classification of fungicide mechanism of action according to the Fungicide Resistance Action Committee (FRAC): http://www.frac.info/publication/anhang/FRAC%20Code%20List%202013-final.pdf"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_frac_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_frac_classification_30.table_id
}

output "bigquery_table-ebi_chembl_frac_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_frac_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_go_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "go_classification_30"
  description = "Table storing the ChEMBL Drug Target GO slim (http://www.geneontology.org/ontology/subsets/goslim_chembl.obo)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_go_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_go_classification_30.table_id
}

output "bigquery_table-ebi_chembl_go_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_go_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_hrac_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "hrac_classification_30"
  description = "Table showing classification of herbicide mechanism of action according to the Herbicide Resistance Action Committee (HRAC): http://www.hracglobal.com/Education/ClassificationofHerbicideSiteofAction.aspx"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_hrac_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_hrac_classification_30.table_id
}

output "bigquery_table-ebi_chembl_hrac_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_hrac_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_indication_refs_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "indication_refs_30"
  description = "Table storing references indicating the source of drug indication information"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_indication_refs_30-table_id" {
  value = google_bigquery_table.ebi_chembl_indication_refs_30.table_id
}

output "bigquery_table-ebi_chembl_indication_refs_30-id" {
  value = google_bigquery_table.ebi_chembl_indication_refs_30.id
}

resource "google_bigquery_table" "ebi_chembl_irac_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "irac_classification_30"
  description = "Table showing classification of insecticide mechanism of action according to the Insecticide Resistance Action Committee (IRAC): http://www.irac-online.org/documents/moa-classification/?ext=pdf"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_irac_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_irac_classification_30.table_id
}

output "bigquery_table-ebi_chembl_irac_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_irac_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_ligand_eff_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "ligand_eff_30"
  description = "Contains BEI (Binding Efficiency Index) and SEI (Surface Binding Efficiency Index) for each activity_id where such data can be calculated."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_ligand_eff_30-table_id" {
  value = google_bigquery_table.ebi_chembl_ligand_eff_30.table_id
}

output "bigquery_table-ebi_chembl_ligand_eff_30-id" {
  value = google_bigquery_table.ebi_chembl_ligand_eff_30.id
}

resource "google_bigquery_table" "ebi_chembl_mechanism_refs_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "mechanism_refs_30"
  description = "Table storing references for information in the drug_mechanism table"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_mechanism_refs_30-table_id" {
  value = google_bigquery_table.ebi_chembl_mechanism_refs_30.table_id
}

output "bigquery_table-ebi_chembl_mechanism_refs_30-id" {
  value = google_bigquery_table.ebi_chembl_mechanism_refs_30.id
}

resource "google_bigquery_table" "ebi_chembl_metabolism_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "metabolism_30"
  description = "Table storing drug metabolic pathways, manually curated from a variety of sources"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_metabolism_30-table_id" {
  value = google_bigquery_table.ebi_chembl_metabolism_30.table_id
}

output "bigquery_table-ebi_chembl_metabolism_30-id" {
  value = google_bigquery_table.ebi_chembl_metabolism_30.id
}

resource "google_bigquery_table" "ebi_chembl_metabolism_refs_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "metabolism_refs_30"
  description = "Table storing references for metabolic pathways, indicating the source of the data"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_metabolism_refs_30-table_id" {
  value = google_bigquery_table.ebi_chembl_metabolism_refs_30.table_id
}

output "bigquery_table-ebi_chembl_metabolism_refs_30-id" {
  value = google_bigquery_table.ebi_chembl_metabolism_refs_30.id
}

resource "google_bigquery_table" "ebi_chembl_molecule_atc_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "molecule_atc_classification_30"
  description = "Table mapping drugs in the molecule_dictionary to ATC codes in the atc_classification table"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_molecule_atc_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_molecule_atc_classification_30.table_id
}

output "bigquery_table-ebi_chembl_molecule_atc_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_molecule_atc_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_molecule_dictionary_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "molecule_dictionary_30"
  description = "Non redundant list of compounds/biotherapeutics with associated identifiers"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_molecule_dictionary_30-table_id" {
  value = google_bigquery_table.ebi_chembl_molecule_dictionary_30.table_id
}

output "bigquery_table-ebi_chembl_molecule_dictionary_30-id" {
  value = google_bigquery_table.ebi_chembl_molecule_dictionary_30.id
}

resource "google_bigquery_table" "ebi_chembl_molecule_frac_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "molecule_frac_classification_30"
  description = "Table showing Fungicide Resistance Action Committee (FRAC) mechanism of action classification for known crop protection fungicides."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_molecule_frac_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_molecule_frac_classification_30.table_id
}

output "bigquery_table-ebi_chembl_molecule_frac_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_molecule_frac_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_molecule_hierarchy_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "molecule_hierarchy_30"
  description = "Table storing relationships between parents, salts and active metabolites (for pro-drugs)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_molecule_hierarchy_30-table_id" {
  value = google_bigquery_table.ebi_chembl_molecule_hierarchy_30.table_id
}

output "bigquery_table-ebi_chembl_molecule_hierarchy_30-id" {
  value = google_bigquery_table.ebi_chembl_molecule_hierarchy_30.id
}

resource "google_bigquery_table" "ebi_chembl_molecule_hrac_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "molecule_hrac_classification_30"
  description = "Table showing Herbicide Resistance Action Committee (HRAC) mechanism of action classification for known herbicidal compounds."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_molecule_hrac_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_molecule_hrac_classification_30.table_id
}

output "bigquery_table-ebi_chembl_molecule_hrac_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_molecule_hrac_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_molecule_irac_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "molecule_irac_classification_30"
  description = "Table showing Insecticide Resistance Action Committee (IRAC) mechanism of action classification for known crop protection insecticides."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_molecule_irac_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_molecule_irac_classification_30.table_id
}

output "bigquery_table-ebi_chembl_molecule_irac_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_molecule_irac_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_molecule_synonyms_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "molecule_synonyms_30"
  description = "Stores synonyms for a compound (e.g., common names, trade names, research codes etc)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_molecule_synonyms_30-table_id" {
  value = google_bigquery_table.ebi_chembl_molecule_synonyms_30.table_id
}

output "bigquery_table-ebi_chembl_molecule_synonyms_30-id" {
  value = google_bigquery_table.ebi_chembl_molecule_synonyms_30.id
}

resource "google_bigquery_table" "ebi_chembl_organism_class_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "organism_class_30"
  description = "Simple organism classification (essentially a cut-down version of the NCBI taxonomy for organisms in ChEMBL assay2target and target_dictionary tables), allowing browsing of ChEMBL data by taxonomic groups"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_organism_class_30-table_id" {
  value = google_bigquery_table.ebi_chembl_organism_class_30.table_id
}

output "bigquery_table-ebi_chembl_organism_class_30-id" {
  value = google_bigquery_table.ebi_chembl_organism_class_30.id
}

resource "google_bigquery_table" "ebi_chembl_patent_use_codes_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "patent_use_codes_30"
  description = "Table from FDA Orange Book, showing definitions of different patent use codes (as used in the product_patents table)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_patent_use_codes_30-table_id" {
  value = google_bigquery_table.ebi_chembl_patent_use_codes_30.table_id
}

output "bigquery_table-ebi_chembl_patent_use_codes_30-id" {
  value = google_bigquery_table.ebi_chembl_patent_use_codes_30.id
}

resource "google_bigquery_table" "ebi_chembl_predicted_binding_domains_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "predicted_binding_domains_30"
  description = "Table storing information on the likely binding domain of compounds in the activities table (based on analysis of the domain structure of the target. Note these are predictions, not experimentally determined. See Kruger F, Rostom R and Overington JP (2012), BMC Bioinformatics, 13(S17), S11 for more details."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_predicted_binding_domains_30-table_id" {
  value = google_bigquery_table.ebi_chembl_predicted_binding_domains_30.table_id
}

output "bigquery_table-ebi_chembl_predicted_binding_domains_30-id" {
  value = google_bigquery_table.ebi_chembl_predicted_binding_domains_30.id
}

resource "google_bigquery_table" "ebi_chembl_product_patents_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "product_patents_30"
  description = "Table from FDA Orange Book, showing patents associated with drug products."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_product_patents_30-table_id" {
  value = google_bigquery_table.ebi_chembl_product_patents_30.table_id
}

output "bigquery_table-ebi_chembl_product_patents_30-id" {
  value = google_bigquery_table.ebi_chembl_product_patents_30.id
}

resource "google_bigquery_table" "ebi_chembl_products_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "products_30"
  description = "Table containing information about approved drug products (mainly from the FDA Orange Book), such as trade name, administration route, approval date. Ingredients in each product are linked to the molecule dictionary via the formulations table."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_products_30-table_id" {
  value = google_bigquery_table.ebi_chembl_products_30.table_id
}

output "bigquery_table-ebi_chembl_products_30-id" {
  value = google_bigquery_table.ebi_chembl_products_30.id
}

resource "google_bigquery_table" "ebi_chembl_protein_class_synonyms_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "protein_class_synonyms_30"
  description = "Table storing synonyms for the protein family classifications (from various sources including MeSH, ConceptWiki and UMLS)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_protein_class_synonyms_30-table_id" {
  value = google_bigquery_table.ebi_chembl_protein_class_synonyms_30.table_id
}

output "bigquery_table-ebi_chembl_protein_class_synonyms_30-id" {
  value = google_bigquery_table.ebi_chembl_protein_class_synonyms_30.id
}

resource "google_bigquery_table" "ebi_chembl_protein_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "protein_classification_30"
  description = "Table storing the protein family classifications for protein targets in ChEMBL (formerly in the target_class table)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_protein_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_protein_classification_30.table_id
}

output "bigquery_table-ebi_chembl_protein_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_protein_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_protein_family_classification_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "protein_family_classification_30"
  description = "WARNING! THIS TABLE IS NOW DEPRECATED, PLEASE USE PROTEIN_CLASSIFICATION INSTEAD."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_protein_family_classification_30-table_id" {
  value = google_bigquery_table.ebi_chembl_protein_family_classification_30.table_id
}

output "bigquery_table-ebi_chembl_protein_family_classification_30-id" {
  value = google_bigquery_table.ebi_chembl_protein_family_classification_30.id
}

resource "google_bigquery_table" "ebi_chembl_relationship_type_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "relationship_type_30"
  description = "Lookup table for assay2target.relationship_type column, showing whether assays are mapped to targets of the correct identity and species (\u0027Direct\u0027) or close homologues (\u0027Homologue\u0027)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_relationship_type_30-table_id" {
  value = google_bigquery_table.ebi_chembl_relationship_type_30.table_id
}

output "bigquery_table-ebi_chembl_relationship_type_30-id" {
  value = google_bigquery_table.ebi_chembl_relationship_type_30.id
}

resource "google_bigquery_table" "ebi_chembl_research_companies_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "research_companies_30"
  description = "Table storing a list of pharmaceutical companies (including current and former names) corresponding to each research code stem in the research_stem table. A stem can sometimes be used by more than one company."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_research_companies_30-table_id" {
  value = google_bigquery_table.ebi_chembl_research_companies_30.table_id
}

output "bigquery_table-ebi_chembl_research_companies_30-id" {
  value = google_bigquery_table.ebi_chembl_research_companies_30.id
}

resource "google_bigquery_table" "ebi_chembl_research_stem_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "research_stem_30"
  description = "Table storing a list of stems/prefixes used in research codes."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_research_stem_30-table_id" {
  value = google_bigquery_table.ebi_chembl_research_stem_30.table_id
}

output "bigquery_table-ebi_chembl_research_stem_30-id" {
  value = google_bigquery_table.ebi_chembl_research_stem_30.id
}

resource "google_bigquery_table" "ebi_chembl_site_components_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "site_components_30"
  description = "Table defining the location of the binding sites in the binding_sites table. A binding site could be defined in terms of which protein subunits (components) are involved, the domains within those subunits to which the compound binds, and possibly even the precise residues involved. For a target where the binding site is at the interface of two protein subunits or two domains, there will be two site_components describing each of these subunits/domains."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_site_components_30-table_id" {
  value = google_bigquery_table.ebi_chembl_site_components_30.table_id
}

output "bigquery_table-ebi_chembl_site_components_30-id" {
  value = google_bigquery_table.ebi_chembl_site_components_30.id
}

resource "google_bigquery_table" "ebi_chembl_source_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "source_30"
  description = "Table showing source from which ChEMBL activity data is derived (e.g., literature, deposited datasets etc)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_source_30-table_id" {
  value = google_bigquery_table.ebi_chembl_source_30.table_id
}

output "bigquery_table-ebi_chembl_source_30-id" {
  value = google_bigquery_table.ebi_chembl_source_30.id
}

resource "google_bigquery_table" "ebi_chembl_structural_alert_sets_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "structural_alert_sets_30"
  description = "Table showing list of sets of structural alerts that have been included in COMPOUND_STRUCTURAL_ALERT table. It should be noted some alerts/alert sets are more permissive than others and may flag a large number of compounds. Results should be interpreted with care, depending on the use-case, and not treated as a blanket filter (e.g., around 50% of approved drugs have 1 or more alerts from these sets)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_structural_alert_sets_30-table_id" {
  value = google_bigquery_table.ebi_chembl_structural_alert_sets_30.table_id
}

output "bigquery_table-ebi_chembl_structural_alert_sets_30-id" {
  value = google_bigquery_table.ebi_chembl_structural_alert_sets_30.id
}

resource "google_bigquery_table" "ebi_chembl_structural_alerts_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "structural_alerts_30"
  description = "Table storing a list of structural features (encoded as SMARTS) that are potentially undesirable in drug discovery context. It should be noted some alerts/alert sets are more permissive than others and may flag a large number of compounds. Results should be interpreted with care, depending on the use-case, and not treated as a blanket filter (e.g., around 50% of approved drugs have 1 or more alerts from these sets)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_structural_alerts_30-table_id" {
  value = google_bigquery_table.ebi_chembl_structural_alerts_30.table_id
}

output "bigquery_table-ebi_chembl_structural_alerts_30-id" {
  value = google_bigquery_table.ebi_chembl_structural_alerts_30.id
}

resource "google_bigquery_table" "ebi_chembl_target_components_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "target_components_30"
  description = "Links molecular target from the target_dictionary to the components they consist of (in the component_sequences table). For a protein complex or protein family target, for example, there will be multiple protein components in the component_sequences table."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_target_components_30-table_id" {
  value = google_bigquery_table.ebi_chembl_target_components_30.table_id
}

output "bigquery_table-ebi_chembl_target_components_30-id" {
  value = google_bigquery_table.ebi_chembl_target_components_30.id
}

resource "google_bigquery_table" "ebi_chembl_target_dictionary_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "target_dictionary_30"
  description = "Target Dictionary containing all curated targets for ChEMBL. Includes both protein targets and non-protein targets (e.g., organisms, tissues, cell lines)"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_target_dictionary_30-table_id" {
  value = google_bigquery_table.ebi_chembl_target_dictionary_30.table_id
}

output "bigquery_table-ebi_chembl_target_dictionary_30-id" {
  value = google_bigquery_table.ebi_chembl_target_dictionary_30.id
}

resource "google_bigquery_table" "ebi_chembl_target_relations_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "target_relations_30"
  description = "Table showing relationships between different protein targets based on overlapping protein components (e.g., relationship between a protein complex and the individual subunits)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_target_relations_30-table_id" {
  value = google_bigquery_table.ebi_chembl_target_relations_30.table_id
}

output "bigquery_table-ebi_chembl_target_relations_30-id" {
  value = google_bigquery_table.ebi_chembl_target_relations_30.id
}

resource "google_bigquery_table" "ebi_chembl_target_type_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "target_type_30"
  description = "Lookup table for target types used in the target dictionary"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_target_type_30-table_id" {
  value = google_bigquery_table.ebi_chembl_target_type_30.table_id
}

output "bigquery_table-ebi_chembl_target_type_30-id" {
  value = google_bigquery_table.ebi_chembl_target_type_30.id
}

resource "google_bigquery_table" "ebi_chembl_tissue_dictionary_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "tissue_dictionary_30"
  description = "Table storing information about tissues used in assays."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_tissue_dictionary_30-table_id" {
  value = google_bigquery_table.ebi_chembl_tissue_dictionary_30.table_id
}

output "bigquery_table-ebi_chembl_tissue_dictionary_30-id" {
  value = google_bigquery_table.ebi_chembl_tissue_dictionary_30.id
}

resource "google_bigquery_table" "ebi_chembl_usan_stems_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "usan_stems_30"
  description = "Table storing definitions for stems used in USANs (United States Adopted Names)."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_usan_stems_30-table_id" {
  value = google_bigquery_table.ebi_chembl_usan_stems_30.table_id
}

output "bigquery_table-ebi_chembl_usan_stems_30-id" {
  value = google_bigquery_table.ebi_chembl_usan_stems_30.id
}

resource "google_bigquery_table" "ebi_chembl_variant_sequences_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "variant_sequences_30"
  description = "Table storing information about mutant sequences and other variants used in assays. The sequence provided is a representative sequence incorporating the reported mutation/variant used in the assay - it is not necessarily the exact sequence used in the experiment."
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_variant_sequences_30-table_id" {
  value = google_bigquery_table.ebi_chembl_variant_sequences_30.table_id
}

output "bigquery_table-ebi_chembl_variant_sequences_30-id" {
  value = google_bigquery_table.ebi_chembl_variant_sequences_30.id
}

resource "google_bigquery_table" "ebi_chembl_version_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "version_30"
  description = "Table showing release version and creation date for the database"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_version_30-table_id" {
  value = google_bigquery_table.ebi_chembl_version_30.table_id
}

output "bigquery_table-ebi_chembl_version_30-id" {
  value = google_bigquery_table.ebi_chembl_version_30.id
}

resource "google_bigquery_table" "ebi_chembl_warning_refs_30" {
  project     = var.project_id
  dataset_id  = "ebi_chembl"
  table_id    = "warning_refs_30"
  description = "Table storing references indicating the source of drug warning information"
  depends_on = [
    google_bigquery_dataset.ebi_chembl
  ]
}

output "bigquery_table-ebi_chembl_warning_refs_30-table_id" {
  value = google_bigquery_table.ebi_chembl_warning_refs_30.table_id
}

output "bigquery_table-ebi_chembl_warning_refs_30-id" {
  value = google_bigquery_table.ebi_chembl_warning_refs_30.id
}
