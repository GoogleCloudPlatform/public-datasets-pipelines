WITH
  segs AS (
  SELECT
    PatientID,
    SOPInstanceUID,
    FrameOfReferenceUID,
    SegmentSequence
  FROM
    `PROJECT.DATASET.dicom_metadata`
  WHERE
    # more reliable than Modality = "SEG"
    SOPClassUID = "1.2.840.10008.5.1.4.1.1.66.4" )
SELECT
  PatientID,
  SOPInstanceUID,
  FrameOfReferenceUID,
  CASE ARRAY_LENGTH(unnested.AnatomicRegionSequence)
    WHEN 0 THEN NULL
  ELSE
  STRUCT( unnested.AnatomicRegionSequence [
  OFFSET
    (0)].CodeValue AS CodeValue,
    unnested.AnatomicRegionSequence [
  OFFSET
    (0)].CodingSchemeDesignator AS CodingSchemeDesignator,
    unnested.AnatomicRegionSequence [
  OFFSET
    (0)].CodeMeaning AS CodeMeaning )
END
  AS AnatomicRegion,
  CASE ( ARRAY_LENGTH(unnested.AnatomicRegionSequence) > 0
    AND ARRAY_LENGTH( unnested.AnatomicRegionSequence [
    OFFSET
      (0)].AnatomicRegionModifierSequence ) > 0 )
    WHEN TRUE THEN unnested.AnatomicRegionSequence [ OFFSET (0)].AnatomicRegionModifierSequence [ OFFSET (0)] #unnested.AnatomicRegionSequence[OFFSET(0)].AnatomicRegionModifierSequence,
  ELSE
  NULL
END
  AS AnatomicRegionModifier,
  CASE ARRAY_LENGTH(unnested.SegmentedPropertyCategoryCodeSequence)
    WHEN 0 THEN NULL
  ELSE
  unnested.SegmentedPropertyCategoryCodeSequence [
OFFSET
  (0)]
END
  AS SegmentedPropertyCategory,
  CASE ARRAY_LENGTH(unnested.SegmentedPropertyTypeCodeSequence)
    WHEN 0 THEN NULL
  ELSE
  unnested.SegmentedPropertyTypeCodeSequence [
OFFSET
  (0)]
END
  AS SegmentedPropertyType,
  #unnested.SegmentedPropertyTypeCodeSequence,
  #unnested.SegmentedPropertyTypeModifierCodeSequence,
  unnested.SegmentAlgorithmType,
  unnested.SegmentNumber,
  unnested.TrackingUID,
  unnested.TrackingID
FROM
  segs
CROSS JOIN
  UNNEST(SegmentSequence) AS unnested # correctness check: there should be 4 segmented nodules for this subject
  #where PatientID = "LIDC-IDRI-0001"
  # Note that it is possible to have some of those sequences empty!
  # Debug:
  #WHERE
  #  ARRAY_LENGTH(unnested.AnatomicRegionSequence) = 0
  # Debug:
  #    )
#SELECT
#  DISTINCT SegmentedPropertyTypeCodeSequence[
#OFFSET
#  (0)].CodeMeaning
#FROM
#  segs_details
#WHERE
#  ARRAY_LENGTH(SegmentedPropertyTypeCodeSequence) <> 0
