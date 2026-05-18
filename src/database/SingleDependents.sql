-- SELECT e.system_name,
--   e.shortcode,
--   (
--     SELECT COUNT(*)
--     FROM systems AS f
--     WHERE f.system_name != e.system_name
--       AND f.shortcode = e.shortcode -- Bounding box - performance etc
--       AND f.latitude BETWEEN e.latitude - 20 AND e.latitude + 20
--       AND f.longitude BETWEEN e.longitude - 20 AND e.longitude + 20
--       AND f.height BETWEEN e.height - 20 AND e.height + 20
--       AND (
--         (f.latitude - e.latitude) * (f.latitude - e.latitude) + (f.longitude - e.longitude) * (f.longitude - e.longitude) + (f.height - e.height) * (f.height - e.height)
--       ) < 20 * 20
--   ) AS neighbour_count
-- FROM systems AS e
-- WHERE e.state = "Stronghold";


-- SET @fortified_range := 20;
-- SET @fortified_range_squared := @fortified_range * @fortified_range;
-- SET @stronghold_range := 30;
-- SET @stronghold_range_squared := @stronghold_range * @stronghold_range;
-- SELECT
--     q.system_name,
--     q.shortcode,
--     q.fort_count,
--     q.strong_count
-- FROM (
--     SELECT
--         e.system_name AS system_name,
--         e.shortcode   AS shortcode,
--         -- Count fortified neighbors within 20 ly
--         (
--             SELECT COUNT(*)
--             FROM systems f
--             WHERE f.state = 'Fortified'
--               AND f.shortcode = e.shortcode
--               AND f.system_name <> e.system_name
--               AND (
--                     (f.latitude  - e.latitude ) * (f.latitude  - e.latitude ) +
--                     (f.longitude - e.longitude) * (f.longitude - e.longitude) +
--                     (f.height    - e.height   ) * (f.height    - e.height   )
--                   ) <= @fortified_range_squared
--         ) AS fort_count,
--         -- Count stronghold neighbors within 30 ly
--         (
--             SELECT COUNT(*)
--             FROM systems s
--             WHERE s.state = 'Stronghold'
--               AND s.shortcode = e.shortcode
--               AND s.system_name <> e.system_name
--               AND (
--                     (s.latitude  - e.latitude ) * (s.latitude  - e.latitude ) +
--                     (s.longitude - e.longitude) * (s.longitude - e.longitude) +
--                     (s.height    - e.height   ) * (s.height    - e.height   )
--                   ) <= @stronghold_range_squared
--         ) AS strong_count
--         -- (
--         --     q.strong_count + q.fort_count
--         -- ) as dependents
--     FROM systems e
--     WHERE e.state = 'Exploited'
--       AND e.shortcode <> ''
-- ) AS q
-- -- Exactly ONE dependency total
-- WHERE (q.fort_count + q.strong_count) = 1;

---the number of solely dependent exploited systems there are for a given stronghold or fortified
---wanted to know which fortified or stronghold to target to knock out as many exploited as possible.
---
---For every strongold, get 
---
---

SET @fortified_range := 20;
SET @fortified_range_squared := @fortified_range * @fortified_range;
SET @stronghold_range := 30;
SET @stronghold_range_squared := @stronghold_range * @stronghold_range;


SELECT
    q.system_name,
    q.shortcode,
    q.fort_count,
    q.strong_count,
    
    (
        SELECT d.system_name
        FROM systems d
        WHERE d.shortcode = q.shortcode
          AND d.system_name <> q.system_name
          AND (
                (d.latitude  - q.latitude ) * (d.latitude  - q.latitude ) +
                (d.longitude - q.longitude) * (d.longitude - q.longitude) +
                (d.height    - q.height   ) * (d.height    - q.height   )
              ) <= 
              CASE 
                WHEN d.state = 'Fortified' THEN @fortified_range_squared
                WHEN d.state = 'Stronghold' THEN @stronghold_range_squared
              END
          AND d.state IN ('Fortified', 'Stronghold')
        LIMIT 1
    ) AS dependency_system,
    (
        SELECT d.state
        FROM systems d
        WHERE d.shortcode = q.shortcode
          AND d.system_name <> q.system_name
          AND (
                (d.latitude  - q.latitude ) * (d.latitude  - q.latitude ) +
                (d.longitude - q.longitude) * (d.longitude - q.longitude) +
                (d.height    - q.height   ) * (d.height    - q.height   )
              ) <= 
              CASE 
                WHEN d.state = 'Fortified' THEN @fortified_range_squared
                WHEN d.state = 'Stronghold' THEN @stronghold_range_squared
              END
          AND d.state IN ('Fortified', 'Stronghold')
        LIMIT 1
    ) AS dependency_type
FROM (
    SELECT
        e.system_name,
        e.shortcode,
        e.latitude,
        e.longitude,
        e.height,
        -- Count fortified neighbors within 20
        (
            SELECT COUNT(*)
            FROM systems f
            WHERE f.state = 'Fortified'
              AND f.shortcode = e.shortcode
              AND f.system_name <> e.system_name
              AND (
                    (f.latitude  - e.latitude ) * (f.latitude  - e.latitude ) +
                    (f.longitude - e.longitude) * (f.longitude - e.longitude) +
                    (f.height    - e.height   ) * (f.height    - e.height   )
                  ) <= @fortified_range_squared
        ) AS fort_count,
        -- Count stronghold neighbors within 30
        (
            SELECT COUNT(*)
            FROM systems s
            WHERE s.state = 'Stronghold'
              AND s.shortcode = e.shortcode
              AND s.system_name <> e.system_name
              AND (
                    (s.latitude  - e.latitude ) * (s.latitude  - e.latitude ) +
                    (s.longitude - e.longitude) * (s.longitude - e.longitude) +
                    (s.height    - e.height   ) * (s.height    - e.height   )
                  ) <= @stronghold_range_squared
        ) AS strong_count
    FROM systems e
    WHERE e.state = 'Exploited'
      AND e.shortcode <> ''
      -- AND e.shortcode = "LYR"
) AS q
-- Exactly one dependency total
WHERE (q.fort_count + q.strong_count) = 1;