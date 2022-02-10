WITH
  contentSequenceLevel3 AS (
  SELECT
    PatientID,
    SOPInstanceUID,
    measurementGroup_number,
    segmentationInstanceUID,
    segmentationSegmentNumber,
    sourceSegmentedSeriesUID,
    trackingIdentifier,
    trackingUniqueIdentifier,
    contentSequence.ConceptNameCodeSequence [
  OFFSET
    (0)] AS ConceptNameCodeSequence,
    contentSequence.ConceptCodeSequence [
  OFFSET
    (0)] AS ConceptCodeSequence
  FROM
    `PROJECT.DATASET.measurement_groups`
  CROSS JOIN
    UNNEST (contentSequence.ContentSequence) AS contentSequence
  WHERE
    contentSequence.ValueType = "CODE" ),
  findingsAndFindingSites AS (
  WITH
    findings AS (
    SELECT
      PatientID,
      SOPInstanceUID,
      measurementGroup_number,
      segmentationInstanceUID,
      segmentationSegmentNumber,
      sourceSegmentedSeriesUID,
      trackingIdentifier,
      trackingUniqueIdentifier,
      ConceptCodeSequence AS finding
    FROM
      contentSequenceLevel3
    WHERE
      ConceptNameCodeSequence.CodeValue = "121071"
      AND ConceptNameCodeSequence.CodingSchemeDesignator = "DCM" ),
    findingSites AS (
    SELECT
      PatientID,
      SOPInstanceUID,
      measurementGroup_number,
      ConceptCodeSequence AS findingSite
    FROM
      contentSequenceLevel3
    WHERE
      ConceptNameCodeSequence.CodeValue = "G-C0E3"
      AND ConceptNameCodeSequence.CodingSchemeDesignator = "SRT" )
  SELECT
    findings.PatientID,
    findings.SOPInstanceUID,
    findings.finding,
    findings.segmentationInstanceUID,
    findings.segmentationSegmentNumber,
    findings.sourceSegmentedSeriesUID,
    findings.trackingIdentifier,
    findings.trackingUniqueIdentifier,
    findingSites.findingSite,
    findingSites.measurementGroup_number
  FROM
    findings
  JOIN
    findingSites
  ON
    findings.SOPInstanceUID = findingSites.SOPInstanceUID
    AND findings.measurementGroup_number = findingSites.measurementGroup_number )
SELECT
  contentSequenceLevel3.PatientID,
  contentSequenceLevel3.SOPInstanceUID,
  findingsAndFindingSites.measurementGroup_number,
  findingsAndFindingSites.segmentationInstanceUID,
  findingsAndFindingSites.segmentationSegmentNumber,
  findingsAndFindingSites.sourceSegmentedSeriesUID,
  findingsAndFindingSites.trackingIdentifier,
  findingsAndFindingSites.trackingUniqueIdentifier,
  contentSequenceLevel3.ConceptNameCodeSequence AS Quantity,
  contentSequenceLevel3.ConceptCodeSequence AS Value,
  findingsAndFindingSites.finding,
  findingsAndFindingSites.findingSite
FROM
  contentSequenceLevel3
JOIN
  findingsAndFindingSites
ON
  contentSequenceLevel3.SOPInstanceUID = findingsAndFindingSites.SOPInstanceUID
  AND contentSequenceLevel3.measurementGroup_number = findingsAndFindingSites.measurementGroup_number
WHERE
  # exclude
  ( ConceptNameCodeSequence.CodeMeaning <> "121071"
    AND ConceptNameCodeSequence.CodingSchemeDesignator <> "DCM" ) AND # Finding
  ( ConceptNameCodeSequence.CodeMeaning <> "G-C0E3"
    AND ConceptNameCodeSequence.CodingSchemeDesignator <> "SRT" ) # Finding Site
  # correctness check: adding the below should result in a 36 rows column (4 segmented lesions, with 9 evaluations per each)
  #    AND
  #  contentSequenceLevel3.PatientID = "LIDC-IDRI-0001"
