SELECT
  SOPInstanceUID,
  SAFE_CAST(SliceThickness AS FLOAT64) AS SliceThickness
FROM
  `PROJECT.DATASET.dicom_metadata` AS dcm
