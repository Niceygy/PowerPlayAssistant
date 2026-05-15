package handlers

import (
	"slices"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/handlers/tasks"
	"niceygy.net/powerplay-assistant/src/utils"
)

var SPESIFIC_TASK_HANDLERS map[string]echo.HandlerFunc = map[string]echo.HandlerFunc{
	"Bounty hunting":                                tasks.HandleBountyHunting,
	"Scan Megaship Datalinks":                       tasks.HandleMegaship,
	"Deliver PowerPlay Commodities":                 tasks.HandleCommodities,
	"Upload Powerplay Malware":                      tasks.HandleOdyMalware,
	"Transfer Power classified data":                tasks.HandleOdysseyDownloadTasks,
	"Transfer Power association and political data": tasks.HandleOdysseyDownloadTasks,
	"Transfer Power research and Industrial data":   tasks.HandleOdysseyDownloadTasks,
	"Conflict Zones":                                tasks.HandleConflictSearch,
}

func HandleResults(c *echo.Context) error {
	system := c.QueryParam("system")
	task := c.QueryParam("task")
	power := c.QueryParam("power")

	if !database.DoesSystemExist(system) {
		return c.HTML(404, utils.RenderTemplate("templates/errors/noSuchSystem.html", map[any]any{}))
	} else if isTaskIllegal(task, database.IsSystemAnarchy(system)) && len(c.QueryParam("anarchy")) < 1 {
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
	} else if handler, exists := SPESIFIC_TASK_HANDLERS[task]; exists {
		return handler(c)
	} else {
		// default:
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
			"isIllegal":          isTaskIllegal(task, anarchy),
			"isOpposingWeakness": utils.IsOpposingWeakness(task, shortcode),
			"isOwnStrength":      utils.IsOwnStrength(task, shortcode),
			"systemNotes":        database.GetExtraInfo(system),
			"taskDescription":    utils.TASKDESCRIPTIONS[utils.GetTaskCode(task)],
		}))
	}

}
