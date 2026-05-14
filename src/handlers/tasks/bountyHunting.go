package tasks

import (
	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

const bounty_task_code string = "BTHT"

func HandleBountyHunting(c *echo.Context) error {
	system := c.QueryParam("system")
	power := c.QueryParam("power")

	if database.IsSystemAnarchy(system) {
		return c.HTML(200, utils.RenderTemplate("templates/does_not_work.html", map[any]any{
			"ERRORDATA": "Bounty hunting cannot be completed in anarchy systems.",
			"ERRORCODE": "INCOMPLETABLE",
		}))
	} else {
		user_power_shortcode := database.PowerFullToShort(power)
		state, controlling_power := database.GetSystemPowerInfo(system)
		return c.HTML(200, utils.RenderTemplate("templates/tasks/general.html", map[any]any{
			"system":             system,
			"power":              power,
			"currentPower":       controlling_power,
			"currentState":       state,
			"isAnarchy":          "NO",
			"taskName":           "Bounty Hunting",
			"isIlligal":          "NO",
			"isOpposingWeakness": utils.IsOpposingWeakness(bounty_task_code, user_power_shortcode),
			"taskDescription":    utils.TASKDESCRIPTIONS[bounty_task_code],
			"systemNotes":        database.GetExtraInfo(system),
			"isOwnStrength":      utils.IsOwnStrength(bounty_task_code, user_power_shortcode),
		}))
	}
}
