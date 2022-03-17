# What is the most likely category by complaint source?

WITH source_category_counts AS (
  SELECT
    source,
    category,
    count(1) num_instances
  FROM
    `bigquery-public-data`.san_francisco_311.311_service_requests 
  GROUP BY
    1, 2
)
SELECT 
  source, category, num_instances, num_instances/total fraction_of_source FROM
  (SELECT source, category, num_instances,
               ROW_NUMBER() OVER (PARTITION BY source ORDER BY num_instances DESC) rank,
               SUM(num_instances) OVER (PARTITION BY source) total
          FROM source_category_counts)
WHERE
  rank = 1;
