package tasks

import (
	"log"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

const commodity_task_name string = "Deliver PowerPlay Commodities"
const commodity_task_code string = "TPCD"

func whatCommodityForWhatNWhere(power string, system_controllong_power string) (string, string) {
	user_power_shortcode := database.PowerFullToShort(power)
	if power == system_controllong_power {
		return utils.POWERCOMMODITIES[user_power_shortcode][1], "Stronghold"
	} else if _, exists := utils.POWERS[system_controllong_power]; exists {
		//it is a power, but not the user's. undermine
		return utils.POWERCOMMODITIES[user_power_shortcode][2], "Stronghold"
	} else {
		//uncontrolled system, aquire
		return utils.POWERCOMMODITIES[user_power_shortcode][0], "Fortified"
	}
}

func HandleCommodities(c *echo.Context) error {
	system := c.QueryParam("system")
	power := c.QueryParam("power")
	current_state, current_power := database.GetSystemPowerInfo(system)
	needed_commodity, system_type_for_commodity := whatCommodityForWhatNWhere(power, current_power)

	user_coords := database.GetSystemLocation(system)

	rows, err := database.Db.Query(`SELECT
	system_name, shortcode, state, control_points, points_change,
	` + database.CreateDistanceStatement(user_coords) + `
	FROM systems
	WHERE systems.state = '` + system_type_for_commodity + `' 
		AND systems.shortcode = '` + database.PowerFullToShort(power) + `'
	ORDER BY distance
	LIMIT 1;`)

	if err != nil {
		log.Panic(err.Error())
	}

	var fortifiedSystem systems_location_response

	for rows.Next() {
		if err = rows.Scan(&fortifiedSystem.System_name, &fortifiedSystem.Shortcode, &fortifiedSystem.State, &fortifiedSystem.Control_points, &fortifiedSystem.Points_change, &fortifiedSystem.Distance); err != nil {
			log.Panic(err.Error())
		}
	}

	return c.HTML(200, utils.RenderTemplate("templates/tasks/commodity.html", map[string]any{
		"system":          system,
		"power":           power,
		"currentPower":    current_power,
		"currentState":    current_state,
		"isAnarchy":       database.IsSystemAnarchy(system),
		"taskName":        commodity_task_name,
		"taskDescription": utils.TASK_DESCRIPTIONS[commodity_task_code],
		"isIllegal":       "isn't",
		"isOwnStrength":   utils.IsOwnStrength(commodity_task_code, database.PowerFullToShort(power)),
		"item_system":     fortifiedSystem.System_name,
		"item_name":       needed_commodity,
		"item_dist":       fortifiedSystem.Distance,
	}))
}
