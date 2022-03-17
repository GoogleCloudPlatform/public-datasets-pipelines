# What is the most common category for each complaint source?

WITH source_category_counts AS (
  SELECT
    source,
    category,
    COUNT(1) AS num_complaints
  FROM
    `bigquery-public-data`.san_francisco_311.311_service_requests 
  GROUP BY
    source, category
)
SELECT 
  source,
  category, 
  num_complaints, 
  num_complaints/total AS fraction_of_source
FROM
  (SELECT 
     source,
     category, 
     num_complaints,
     # Within each source, rank the categories by number of complaints in descending order. 
     ROW_NUMBER() OVER (PARTITION BY source ORDER BY num_complaints DESC) AS rank,
     # Compute the total number of complaints reported per source
     SUM(num_complaints) OVER (PARTITION BY source) total
   FROM source_category_counts)
 WHERE
   # Extract the most common category of complaint
   rank = 1;
