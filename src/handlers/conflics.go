package handlers

import (
	"log"
	"math"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

type ConflictResult struct {
	System_name string
	Power1      string
	Power2      string
	Has_CZs     bool
	Cycle       int
	LY          float64
}

func HandleConflictsSearch(c *echo.Context) error {
	if c.Request().Method == "GET" {
		return c.HTML(200, utils.RenderTemplate("templates/conflicts/search.html", map[string]any{
			"powers": utils.POWERNAMES,
		}))
	} else {
		system := c.FormValue("system")
		power := database.PowerFullToShort(c.FormValue("power"))

		systemEntry := database.GetSystemLocation(system)

		rows, err := database.Db.Query(`
		SELECT conflicts.system_name, conflicts.first_place, conflicts.second_place, conflicts.has_czs, conflicts.cycle, ` + database.CreateDistanceStatement(systemEntry) + ` 
		FROM conflicts 
		INNER JOIN systems ON conflicts.system_name = systems.system_name 
		WHERE conflicts.first_place = '` + power + `' 
		OR conflicts.second_place = '` + power + `' 
		ORDER BY Distance 
		LIMIT 10; `)
		if err != nil {
			log.Panic(err)
		}

		var systems []ConflictResult

		for rows.Next() {
			s := ConflictResult{}
			if err = rows.Scan(&s.System_name, &s.Power1, &s.Power2, &s.Has_CZs, &s.Cycle, &s.LY); err != nil {
				log.Panic(err.Error())
			} else {
				s.LY = math.Round(s.LY)
				s.Power1 = database.PowerShortToFull(s.Power1)
				s.Power2 = database.PowerShortToFull(s.Power2)
				systems = append(systems, s)
			}
			// godump.Dump(n)
		}

		return c.HTML(200, utils.RenderTemplate("templates/conflicts/result.html", map[string]any{
			"systems":    systems,
			"power":      power,
			"systemName": system,
		}))
	}
}
