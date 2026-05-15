package tasks

import (
	"log"
	"math"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

const rg_task_name string = "Deliver Rare Goods"
const rg_task_code string = ""
const rg_items_limit string = "15"

type rare_good struct {
	Name     string
	System   string
	Station  string
	Distance float64
}

func HandleRareGoods(c *echo.Context) error {
	system := c.QueryParam("system")
	power := c.QueryParam("power")

	user_coords := database.GetSystemLocation(system)
	state, target_sys_owning_power := database.GetSystemPowerInfo(system)

	rows, err := database.Db.Query(`SELECT Raregoods.*, 
	` + database.CreateDistanceStatement(user_coords) + `
	FROM Raregoods
	INNER JOIN systems
		ON Raregoods.system_name = systems.system_name
	ORDER BY distance
	LIMIT ` + rg_items_limit + `;
	`)

	if err != nil {
		log.Panic(err.Error())
	} else {
		defer rows.Close()
	}

	result := []rare_good{}

	for rows.Next() {
		r := rare_good{}
		if err = rows.Scan(&r.Name, &r.System, &r.Station, &r.Distance); err != nil {
			log.Panic(err.Error())
		} else {
			r.Distance = math.Round(r.Distance)
		}
		result = append(result, r)
	}

	return c.HTML(200, utils.RenderTemplate("templates/tasks/raregoods.html", map[string]any{
		"system":             system,
		"power":              power,
		"currentPower":       target_sys_owning_power,
		"currentState":       state,
		"isAnarchy":          database.IsSystemAnarchy(system),
		"taskName":           rg_task_name,
		"taskType":           "Trading",
		"isIlligal":          "isn't",
		"isOpposingWeakness": utils.IsOpposingWeakness(rg_task_code, target_sys_owning_power),
		"taskDescription":    utils.TASK_DESCRIPTIONS[rg_task_code],
		"systemNotes":        database.GetExtraInfo(system),
		"raregoods":          result,
		"isOwnStrength":      utils.IsOwnStrength(rg_task_code, database.PowerFullToShort(power)),
	}))
}
