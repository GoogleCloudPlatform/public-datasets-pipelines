# What is the most likely category corresponding to each complaint source?

WITH source_category_counts AS (
  SELECT
    source,
    category,
    COUNT(1) AS num_instances
  FROM
    `bigquery-public-data`.san_francisco_311.311_service_requests 
  GROUP BY
    source, category
)
SELECT 
  source,
  category, 
  num_instances, 
  num_instances/total AS fraction_of_source
FROM
  (SELECT 
     source,
     category, 
     num_instances,
     ROW_NUMBER() OVER (PARTITION BY source ORDER BY num_instances DESC) AS rank,
     SUM(num_instances) OVER (PARTITION BY source) total
   FROM source_category_counts)
 WHERE
   rank = 1;
