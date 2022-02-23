WITH
  pre_dicom_all AS (
  SELECT
    aux.tcia_api_collection_id AS tcia_api_collection_id,
    aux.idc_webapp_collection_id AS collection_id,
    aux.collection_timestamp AS collection_timestamp,
    aux.collection_hash as collection_hash,
    aux.collection_init_idc_version AS collection_init_idc_version,
    aux.collection_revised_idc_version AS collection_revised_idc_version,
    dcm.PatientID as PatientID,
    aux.idc_case_id as idc_case_id,
    aux.patient_hash as patient_hash,
    aux.patient_init_idc_version AS patient_init_idc_version,
    aux.patient_revised_idc_version AS patient_revised_idc_version,
    dcm.StudyInstanceUID AS StudyInstanceUID,
    aux.study_uuid as crdc_study_uuid,
    aux.study_hash as study_hash,
    aux.study_init_idc_version AS study_init_idc_version,
    aux.study_revised_idc_version AS study_revised_idc_version,
    dcm.SeriesInstanceUID AS SeriesInstanceUID,
    aux.series_uuid as crdc_series_uuid,
    aux.series_hash as series_hash,
    aux.series_init_idc_version AS series_init_idc_version,
    aux.series_revised_idc_version AS series_revised_idc_version,
    dcm.SOPInstanceUID AS SOPInstanceUID,
    aux.instance_uuid as crdc_instance_uuid,
    aux.gcs_url as gcs_url,
    aux.instance_size as instance_size,
    aux.instance_hash as instance_hash,
    aux.instance_init_idc_version AS instance_init_idc_version,
    aux.instance_revised_idc_version AS instance_revised_idc_version,
    aux.source_doi as Source_DOI,
    aux.license_url as license_url,
    aux.license_long_name as license_long_name,
    aux.license_short_name as license_short_name,
    dcm.* except(PatientID, StudyInstanceUID, SeriesInstanceUID, SOPInstanceUID)
  FROM
    `PROJECT.DATASET.auxiliary_metadata` AS aux
  INNER JOIN
    `PROJECT.DATASET.dicom_metadata` AS dcm
  ON
    aux.SOPInstanceUID = dcm.SOPInstanceUID)

  SELECT
    data_collections.Location AS tcia_tumorLocation,
    data_collections.Species AS tcia_species,
    data_collections.CancerType AS tcia_cancerType,
    pre_dicom_all.*
  FROM
    pre_dicom_all
  INNER JOIN
    `PROJECT.DATASET.original_collections_metadata` AS data_collections
  ON
    pre_dicom_all.collection_id = data_collections.idc_webapp_collection_id
