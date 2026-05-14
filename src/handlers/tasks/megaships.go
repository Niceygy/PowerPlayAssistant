package tasks

import (
	"log"
	"math"
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

func m_CheckInputs(c *echo.Context) error {
	if c.QueryParam("choice") == "" {
		system := c.QueryParam("system")
		power := c.QueryParam("power")
		task := c.QueryParam("task")
		return c.Redirect(307, utils.Concat([]string{
			"handle_choice?system=",
			system,
			"&power=",
			power,
			"&task=",
			task,
		}))
	} else {
		return nil
	}
}

func HandleMegaship(c *echo.Context) error {
	m_CheckInputs(c)
	user_system := c.QueryParam("system")
	power := c.QueryParam("power")
	choice := c.QueryParam("choice")

	megaship_system_col := 1

	// _, system_shortcode := database.GetSystemPowerInfo(system)
	user_shortcode := database.PowerFullToShort(power)
	user_coords := database.GetSystemLocation(user_system)
	is_opposing_statement := ""
	if choice == "Undermine" {
		is_opposing_statement = "!="
	} else {
		is_opposing_statement = "="
	}

	rows, err := database.Db.Query(`SELECT
    megaships.name, megaships.SYSTEM` + strconv.Itoa(megaship_system_col) + `,
    ` + database.CreateDistanceStatement(user_coords) + `
	FROM megaships
	JOIN star_systems
    	ON megaships.SYSTEM` + strconv.Itoa(megaship_system_col) + ` = star_systems.system_name
	JOIN powerdata
    	ON star_systems.system_name = powerdata.system_name
	WHERE powerdata.shortcode ` + is_opposing_statement + ` '` + user_shortcode + `'
	ORDER BY distance
	LIMIT 15;`,
	// /*map[string]any{*/
	// /*"user_longitude": */
	// "SYSTEM"+strconv.Itoa(1),
	// user_coords[0],
	// /*"user_latitide":  */ user_coords[1],
	// /*"user_height":    */ user_coords[2],
	// /*"system_column":  */ "SYSTEM"+strconv.Itoa(1),
	// /*"system_name":    */ user_system,
	// /*"is_opposing":    */ is_opposing_statement,
	// /*"shortcode":      */ user_shortcode,
	/*}*/)

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
		"taskDescription":    utils.TASKDESCRIPTIONS[task_code],
		"isIllegal":          "is not",
		"isOpposingWeakness": utils.IsOpposingWeakness(task_code, user_shortcode),
		"extraInfo":          database.GetExtraInfo(user_system),
		"megaships":          megaship_list,
	}))
}
