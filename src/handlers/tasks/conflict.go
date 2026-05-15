package tasks

import (
	"log"
	"math"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

type conflict_response struct {
	SystemName string
	Power1     string
	Power2     string
	HasCZs     bool
	Cycle      int
	LY         float64
}

func HandleConflictSearch(c *echo.Context) error {
	system := c.QueryParam("system")
	power := c.QueryParam("power")

	user_coords := database.GetSystemLocation(system)
	user_shortcode := database.PowerFullToShort(power)

	rows, err := database.Db.Query(`SELECT
    conflicts.*,
    ` + database.CreateDistanceStatement(user_coords) + `
	FROM conflicts
	JOIN systems
    	ON conflicts.system_name = systems.system_name
	WHERE 
		conflicts.first_place = '` + user_shortcode + `' OR conflicts.second_place = '` + user_shortcode + `'
	ORDER BY distance
	LIMIT 15;`)

	if err != nil {
		log.Panic(err.Error())
	}

	var conflicts []conflict_response

	for rows.Next() {
		c := conflict_response{}
		err = rows.Scan(&c.SystemName, &c.Power1, &c.Power2, &c.HasCZs, &c.Cycle, &c.LY)
		if err != nil {
			log.Panic(err.Error())
		} else {
			c.Power1 = database.PowerShortToFull(c.Power1)
			c.Power2 = database.PowerShortToFull(c.Power2)
			c.LY = math.Round(c.LY)
			conflicts = append(conflicts, c)
		}
	}

	return c.HTML(200, utils.RenderTemplate("templates/conflicts/result.html", map[string]any{
		"systems":    conflicts,
		"systemName": system,
		"power":      power,
	}))

}
