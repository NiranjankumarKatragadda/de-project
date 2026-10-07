SELECT
  DATE(pickup_ts) AS day,
  COUNT(*) AS trips,
  ROUND(SUM(total_amount), 2) AS revenue
FROM analytics.trips
GROUP BY day
ORDER BY day;
SELECT
  EXTRACT(HOUR FROM pickup_ts) AS hour,
  ROUND(AVG(fare_amount), 2) AS avg_fare,
  ROUND(100 * SAFE_DIVIDE(SUM(tip_amount), SUM(fare_amount)), 1) AS tip_pct
FROM analytics.trips
GROUP BY hour
ORDER BY hour;