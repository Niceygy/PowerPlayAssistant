package handlers

import (
	"log"
	"slices"
	"strings"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/utils"
)

func isTaskIlligal(task string, isAnarchy bool) bool {
	if isAnarchy {
		return false
	} else {
		var taskShortCode string
		for k, v := range utils.TASKSHORTCODES {
			if v == task {
				taskShortCode = k
			}
		}
		return slices.Contains(utils.CRIMINALTASKS, taskShortCode)
	}
}

func HandleIndex(c *echo.Context) error {
	if c.Request().Method == "POST" {
		selected_system := c.Request().FormValue("system")
		selected_task := c.Request().FormValue("mission")
		selected_power := c.Request().FormValue("power")

		var redirectURL string

		if isTaskIlligal(selected_task, false) {
			redirectURL = strings.Join([]string{
				"/is_crime",
				"?task=",
				utils.MakeURLSafe(selected_task),
				"&system=",
				utils.MakeURLSafe(selected_system),
				"&power=",
				utils.MakeURLSafe(selected_power),
			}, "")

		} else {
			redirectURL = strings.Join([]string{
				"/results",
				"?task=",
				utils.MakeURLSafe(selected_task),
				"&system=",
				utils.MakeURLSafe(selected_system),
				"&power=",
				utils.MakeURLSafe(selected_power),
			}, "")
		}
		log.Println(redirectURL)
		return c.Redirect(307, redirectURL)
	} else {
		return c.HTML(200, utils.RenderTemplate("templates/index.html", map[string]any{
			"missions":         utils.TASKNAMES,
			"powers":           utils.POWERNAMES,
			"default_system":   "Sol",
			"status_text":      "test",
			"selected_mission": "",
			"selected_power":   "",
		}))
	}
}
