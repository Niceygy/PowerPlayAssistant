package database

import "strconv"

func CreateSystemDependenciesLookup() string {
	fortified_range := 20
	fortified_range_squared := fortified_range * fortified_range

	stronghold_range := 30
	stronghold_range_squared := stronghold_range * stronghold_range

	shortcode := "LYR"

	query := `SELECT
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
                WHEN d.state = 'Fortified' THEN ` + strconv.Itoa(fortified_range_squared) + `
                WHEN d.state = 'Stronghold' THEN ` + strconv.Itoa(stronghold_range_squared) + `
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
                WHEN d.state = 'Fortified' THEN ` + strconv.Itoa(fortified_range_squared) + `
                WHEN d.state = 'Stronghold' THEN ` + strconv.Itoa(stronghold_range_squared) + `
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
                  ) <= ` + strconv.Itoa(fortified_range_squared) + `
        ) AS fort_count,

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
                  ) <= ` + strconv.Itoa(stronghold_range_squared) + `
        ) AS strong_count

    FROM systems e
    WHERE e.state = 'Exploited'
      AND e.shortcode <> ''
      AND e.shortcode = "` + shortcode + `"
) AS q


WHERE (q.fort_count + q.strong_count) = 1;
`

	return query
}
