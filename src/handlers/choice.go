package handlers

import (
	"strings"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/utils"
)

func HandleTaskChoice(c *echo.Context) error {
	if c.Request().Method == "POST" && c.FormValue("choice") != "" {
		system := c.FormValue("system")
		task := c.FormValue("task")
		power := c.FormValue("power")
		choice := c.FormValue("choice")
		return c.Redirect(307, strings.Join([]string{"/results?choice=", choice, "&system=", system, "&task=", task, "&power=", power}, ""))
	} else {
		system := c.QueryParam("system")
		task := c.QueryParam("task")
		power := c.QueryParam("power")
		return c.HTML(200, utils.RenderTemplate("templates/tasks/task_choice.html", map[string]any{
			"system": system,
			"task":   task,
			"power":  power,
		}))
	}
}
