package handlers

import (
	"encoding/json"
	"log"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
)

func HandleSystemSearch(c *echo.Context) error {
	system := c.QueryParam("query")
	var systems []string
	rows, err := database.Db.Query("SELECT system_name FROM systems WHERE system_name LIKE '%" + system + "%' LIMIT 10;" /*, system*/)
	if err != nil {
		log.Panic(err.Error())
	} else {
		for rows.Next() {
			// var s string
			if err = rows.Scan(&system); err != nil {
				log.Panic(err.Error())
			} else {
				systems = append(systems, system)
			}
		}
	}
	res, err := json.Marshal(systems)
	if err != nil {
		log.Panic(err.Error())
	}

	return c.JSONBlob(200, res)
}
