package handlers

import (
	"slices"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

func HandleResults(c *echo.Context) error {
	system := c.QueryParam("system")
	task := c.QueryParam("task")
	power := c.QueryParam("power")

	if !database.DoesSystemExist(system) {
		return c.HTML(404, utils.RenderTemplate("templates/errors/noSuchSystem.html", map[any]any{}))
	} else if isTaskIlligal(task, database.IsSystemAnarchy(system)) && len(c.QueryParam("anarchy")) < 1 {
		return c.Redirect(307, utils.Concat([]string{
			"is_crime?system=",
			system,
			"&power=",
			power,
			"&task=",
			task,
		}))
	} else if slices.Contains(utils.SUSPENDED, task) {
		return c.HTML(200, utils.RenderTemplate("templates/tasks/suspended.html", map[any]any{}))
	}

	switch task {
	case "Scan Megaship Datalinks":
		if c.QueryParam("choice") == "" {
			return c.Redirect(307, utils.Concat([]string{
				"handle_choice?system=",
				system,
				"&power=",
				power,
				"&task=",
				task,
			}))
		} else {
			return HandleMegaship(c)
		}
	case "Sell rare goods":
		return HandleRareGoods(c)
	case "Bounty hunting":
		return HandleBountyHunting(c)
	case "Deliver PowerPlay Commodities":
		return HandleCommodities(c)
	case "Conflict Zones":
		return HandleConflictSearch(c)
	case "Transfer Power classified data",
		"Transfer Power association and political data",
		"Transfer Power research and Industrial data":
		return HandleOdysseyDownloadTasks(c)
	case "Upload Powerplay Malware":
		return HandleOdyMalware(c)

	default:
		sys_state, sys_power := database.GetSystemPowerInfo(system)
		anarchy := database.IsSystemAnarchy(system)
		shortcode := database.PowerFullToShort(power)
		return c.HTML(200, utils.RenderTemplate("templates/tasks/general.html", map[string]any{
			"system":             system,
			"task":               task,
			"power":              power,
			"currentPower":       sys_power,
			"currentState":       sys_state,
			"isAnarchy":          anarchy,
			"taskType":           utils.GetTaskType(task),
			"isIllegal":          isTaskIlligal(task, anarchy),
			"isOpposingWeakness": utils.IsOpposingWeakness(task, shortcode),
			"isOwnStrength":      utils.IsOwnStrength(task, shortcode),
			"systemNotes":        database.GetExtraInfo(system),
			"taskDescription":    utils.TASKDESCRIPTIONS[utils.GetTaskCode(task)],
		}))
		//return c.HTML(404, utils.RenderTemplate("templates/errors/404.html", map[any]any{}))

	}
}
