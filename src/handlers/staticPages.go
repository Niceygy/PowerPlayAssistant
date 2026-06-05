package handlers

import (
	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/utils"
)

func HandleChangelog(c *echo.Context) error {
	return c.HTML(200, utils.RenderTemplate("templates/changelog.html", map[any]any{}))
}

func HandleAbout(c *echo.Context) error {
	return c.HTML(200, utils.RenderTemplate("templates/about.html", map[any]any{}))
}
