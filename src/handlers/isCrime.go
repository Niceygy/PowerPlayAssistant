package handlers

import (
	"net/http"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/utils"
)

func HandleIsCrime(c *echo.Context) error {
	m := c.Request()
	if m.Method == http.MethodPost {
		return c.Redirect(307, utils.Concat([]string{
			"/results?anarchy=",
			c.FormValue("anarchy"),
			"&system=",
			c.FormValue("system"),
			"&power=",
			c.FormValue("power"),
			"&task=",
			c.FormValue("task"),
		}))
	} else {
		return c.HTML(200, utils.RenderTemplate("templates/is_crime.html", map[string]any{
			"task":   c.QueryParam("task"),
			"power":  c.QueryParam("power"),
			"system": c.QueryParam("system"),
		}))
	}
}
