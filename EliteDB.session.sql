SELECT powerdata.system_name, shortcode, state, 
       SQRT(POW(star_systems.latitude - 82.25, 2) + POW(star_systems.longitude - 68.16, 2) + POW(star_systems.height - 48.75 , 2)) AS distance
FROM star_systems
JOIN powerdata ON star_systems.system_name = powerdata.system_name
WHERE powerdata.shortcode = "NAK"
ORDER BY distance DESC;