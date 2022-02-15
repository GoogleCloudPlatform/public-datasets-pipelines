WITH
    pre_dicom_all
AS (
    SELECT
        aux.idc_webapp_collection_id AS collection_id,
        aux.gcs_url as gcs_url,
        aux.gcs_bucket as gcs_bucket,
        aux.study_uuid as crdc_study_uuid,
        aux.series_uuid as crdc_series_uuid,
        aux.instance_uuid as crdc_instance_uuid,
        aux.idc_case_id as idc_case_id,
        aux.instance_size as instance_size,
        aux.version_hash as version_hash,
        aux.collection_hash as collection_hash,
        aux.patient_hash as patient_hash,
        aux.study_hash as study_hash,
        aux.series_hash as series_hash,
        aux.instance_hash as instance_hash,
        aux.source_doi as Source_DOI,
        dcm.*
    FROM
        `PROJECT.DATASET.auxiliary_metadata` AS aux
    INNER JOIN
        `PROJECT.DATASET.dicom_metadata` AS dcm
    ON
        aux.SOPInstanceUID = dcm.SOPInstanceUID
)

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
