package tasks

import (
	"log"
	"math"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

type stronghold_respose struct {
	SystemName  string
	OwningPower string
	Distance    float64
}

func HandleStrongholdCarriers(c *echo.Context) error {
	system := c.QueryParam("system")
	power := c.QueryParam("power")

	user_coords := database.GetSystemLocation(system)
	user_shortcode := database.PowerFullToShort(power)

	rows, err := database.Db.Query(`SELECT system_name, shortcode,
	`+database.CreateDistanceStatement(user_coords)+`
	FROM systems
	WHERE has_stronghold_carrier = TRUE
		AND shortcode != ?
	ORDER BY distance
	LIMIT 10;
	`, user_shortcode)

	if err != nil {
		log.Panic(err.Error())
	}

	var strongholds []stronghold_respose

	for rows.Next() {
		s := stronghold_respose{}
		if err = rows.Scan(&s.SystemName, &s.OwningPower, &s.Distance); err != nil {
			log.Panic(err.Error())
		} else {
			s.Distance = math.Round(s.Distance)
			s.OwningPower = database.PowerShortToFull(s.OwningPower)
		}
		strongholds = append(strongholds, s)
	}

	return c.HTML(200, utils.RenderTemplate("templates/tasks/strongholds.html", map[string]any{
		"system":             system,
		"power":              power,
		"type":               "Combat",
		"task":               "Attack enemy stronghold carrier",
		"taskDescription":    "Head to the enemy stronghold system and attack their carrier group. This can be by destroying ships, damaging the carriers themselves or stealing from the carriers.",
		"isIllegal":          "is",
		"isOpposingWeakness": "isn't",
		"isOwnStrength":      "isn't",
		"extraInfo":          database.GetExtraInfo(system),
		"strongholds":        strongholds,
	}))
}
