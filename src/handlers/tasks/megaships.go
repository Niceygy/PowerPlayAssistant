package tasks

import (
	"log"
	"math"
	"os"
	"strconv"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

const task_code string = "SDLK"

// float to string
func ftos(f float64) string {
	return strconv.FormatFloat(f, 'g', 5, 64)
}

type megaship struct {
	Name     string
	System   string
	Distance float64
}

func getMegashipCycle() string {
	wd, _ := os.Getwd()
	f, err := os.ReadFile(wd + "/week.txt")
	if err != nil {
		log.Panic(err.Error())
	}

	return string(f)
}

func HandleMegaship(c *echo.Context) error {
	user_system := c.QueryParam("system")
	power := c.QueryParam("power")
	choice := c.QueryParam("choice")
	task := c.QueryParam("task")

	if choice == "" {
		return c.Redirect(307, utils.Concat([]string{
			"handle_choice?system=",
			user_system,
			"&power=",
			power,
			"&task=",
			task,
		}))
	}

	megaship_system_col := getMegashipCycle()
	user_shortcode := database.PowerFullToShort(power)
	user_coords := database.GetSystemLocation(user_system)

	is_opposing_statement := ""
	if choice == "Undermine" {
		is_opposing_statement = "!="
	} else {
		is_opposing_statement = "="
	}

	rows, err := database.Db.Query(`SELECT
    megaships.name, megaships.SYSTEM` + megaship_system_col + `,
    ` + database.CreateDistanceStatement(user_coords) + `
	FROM megaships
	JOIN systems
    	ON megaships.SYSTEM` + megaship_system_col + ` = systems.system_name
	WHERE systems.shortcode ` + is_opposing_statement + ` '` + user_shortcode + `'
	ORDER BY distance
	LIMIT 15;`)

	if err != nil {
		log.Panic(err)
	} else {
		defer rows.Close()
	}

	var megaship_list []megaship

	for rows.Next() {
		m := megaship{}
		if err := rows.Scan(&m.Name, &m.System, &m.Distance); err != nil {
			e_str := err.Error()
			log.Panic(e_str)
		}
		m.Distance = math.Round(m.Distance)
		megaship_list = append(megaship_list, m)
	} //PPA_GO/templates/tasks/megaships.html
	return c.HTML(200, utils.RenderTemplate("templates/tasks/megaships.html", map[string]any{
		"system":             user_system,
		"power":              power,
		"type":               choice,
		"task":               "Scan Megaship Datalinks",
		"taskType":           "Scanning",
		"taskDescription":    utils.TASK_DESCRIPTIONS[task_code],
		"isIllegal":          "is not",
		"isOpposingWeakness": utils.IsOpposingWeakness(task_code, user_shortcode),
		"extraInfo":          database.GetExtraInfo(user_system),
		"megaships":          megaship_list,
	}))
}
