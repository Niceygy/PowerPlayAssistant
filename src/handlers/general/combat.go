package general

import "github.com/labstack/echo/v5"

func HandleCombat(c *echo.Context) error

func HandleCombatReinforce(c *echo.Context) error

/*
Find the x closest:
	- Combat Zones
	- Res Sites
	- Installations under pirate attack
*/

func HandleComabatUndermine(c *echo.Context) error
