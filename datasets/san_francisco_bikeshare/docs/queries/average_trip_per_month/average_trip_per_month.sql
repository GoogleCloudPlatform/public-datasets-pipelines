SELECT
  EXTRACT(MONTH FROM start_date) AS month,
  CAST(AVG(duration_sec) AS INT64) AS average_trip_as_seconds
FROM
  bigquery-public-data.san_francisco_bikeshare.bikeshare_trips
GROUP BY
  month
  order by MONTH;
