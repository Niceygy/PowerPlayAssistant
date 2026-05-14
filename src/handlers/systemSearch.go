package handlers

import (
	"log"
	"strings"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
)

func HandleSystemSearch(c *echo.Context) error {
	system := c.QueryParam("query")
	var systems string
	rows, err := database.Db.Query("SELECT system_name FROM star_systems WHERE system_name LIKE '%?%'", system)
	if err != nil {
		log.Panic(err.Error())
	} else {
		for rows.Next() {
			var s string
			if err = rows.Scan(&system); err != nil {
				log.Panic(err.Error())
			} else {
				systems = systems + "'" + s + "',"
			}
		}
		systems = strings.TrimSuffix(systems, ",")
	}

	return c.JSON(200, "["+systems+"]")
}
