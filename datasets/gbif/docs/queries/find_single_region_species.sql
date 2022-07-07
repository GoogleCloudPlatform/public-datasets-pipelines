WITH
  intermediate AS (
  SELECT
    species,
    COUNT(*) AS count,
    MAX(decimallatitude) - MIN(decimallatitude) AS latitude_diff,
    MAX(decimallongitude) - MIN(decimallongitude) AS longitude_diff
  FROM
    `bigquery-public-data.gbif.occurrences` TABLESAMPLE SYSTEM (100 PERCENT)
  WHERE
    decimallatitude IS NOT NULL AND decimallongitude IS NOT NULL
  GROUP BY species)
SELECT *
FROM intermediate
WHERE
  latitude_diff < 1 AND
  longitude_diff < 1 AND
  count > 1000
ORDER BY count DESC;
