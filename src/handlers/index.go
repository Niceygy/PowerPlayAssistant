package handlers

import (
	"math/rand/v2"
	"slices"
	"strings"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/utils"
)

func isTaskIllegal(task string, isAnarchy bool) bool {
	if isAnarchy {
		return false
	} else {
		var taskShortCode string
		for k, v := range utils.TASK_SHORTCODES {
			if v == task {
				taskShortCode = k
			}
		}
		return slices.Contains(utils.TASKS_CRIMINAL, taskShortCode)
	}
}

var subtexts []string = []string{
	"V2!!",
	"Now with added basking",
	"What do you mean, 'its on fire'?!",
	"k5elite.com is cool too",
	"It turns out, very hard indeed",
	"Made with Echo " + echo.Version,
	"Made with 🩷 & 💥, by Niceygy",
}

func HandleIndex(c *echo.Context) error {
	if c.Request().Method == "POST" {
		selected_system := c.Request().FormValue("system")
		selected_task := c.Request().FormValue("mission")
		selected_power := c.Request().FormValue("power")

		var redirectURL string

		if isTaskIllegal(selected_task, false) {
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
		// log.Println(redirectURL)
		return c.Redirect(307, redirectURL)
	} else {
		return c.HTML(200, utils.RenderTemplate("templates/index.html", map[string]any{
			"missions":         utils.TASK_NAMES,
			"powers":           utils.POWERNAMES,
			"default_system":   "Sol",
			"selected_mission": "",
			"selected_power":   "",
			"subtext":          subtexts[rand.IntN(len(subtexts)-1)],
			"status_text":      utils.GetStatus(),
		}))
	}
}
