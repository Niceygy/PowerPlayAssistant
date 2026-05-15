package tasks

import (
	"log"
	"math"
	"slices"
	"strings"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/database"
	"niceygy.net/powerplay-assistant/src/utils"
)

//https://forums.frontier.co.uk/threads/powerplay-2-0-activities.629227/

type powerdata_location_response struct {
	System_name    string
	Shortcode      string
	State          string
	Control_points float64
	Points_change  float64
	Distance       float64
}

//Download from settlments in target system and return to nearby control system

const ody_html_template string = "templates/tasks/odyssey.html"
const (
	RESEARCH_INDUSTRY_SHORTCODE     string = "TPRD"
	ASSOCIATION_POLITICAL_SHORTCODE string = "TPAD"
	CLASSIFIED_SHORTCODE            string = "TPCL"
	MALWARE_SHORTCODE               string = "UPMW"

	TASK_UNDERMINE string = "Undermine"
	TASK_AQUIRE    string = "Aquire"
	TASK_REINFORCE string = "Reinforce"

	//aqusition
	STRONGHOLD_DATA_LIMIT float64 = 30 //LY
	FORTIFIED_DATA_LIMIT  float64 = 20 //LY
)

/*
Aqusition - You are in a unoccupied system, so you need to download <data> from an odyssey settlement here and hand it into a power contact in <owned system>, which is <distance> LY away.
			or: Your power does not control a system within 20 LY, so this task is not possible here. Sorry about that.
Undermine - You are in an enemy system, so you need to download <data> from an odyssey settlement here and hand it into a power contact in <owned system>, which is <distance> LY away.
Reinforce -You are in a friendly system, so you need to download <data> from an odyssey settlement here and hand it into a local power contact.
*/

// Aquire, undermine or reinforce
func whatActivityType(system_power string, user_power string) string {
	if system_power == user_power {
		return TASK_REINFORCE
	} else if slices.Contains(utils.POWERNAMES, system_power) {
		return TASK_UNDERMINE
	} else {
		return TASK_AQUIRE
	}
}

func HandleOdysseyDownloadTasks(c *echo.Context) error {
	system := c.QueryParam("system")
	power := c.QueryParam("power")
	task := c.QueryParam("task")

	var data_type string
	var task_shortcode string
	switch task {
	case "Transfer Power classified data":
		data_type = "'Power Classified'"
		task_shortcode = CLASSIFIED_SHORTCODE
	case "Transfer Power association and political data":
		data_type = "'Power Association' or 'Power Political'"
		task_shortcode = ASSOCIATION_POLITICAL_SHORTCODE
	case "Transfer Power research and Industrial data":
		data_type = "'Power Research' or 'Power Industrial'"
		task_shortcode = RESEARCH_INDUSTRY_SHORTCODE
	}

	user_shortcode := database.PowerFullToShort(power)
	user_coords := database.GetSystemLocation(system)

	var query string
	var information string = "You are in "

	//is the user in a system their power owns?
	system_state, system_power_shortcode := database.GetSystemPowerInfo(system)
	activity_type := whatActivityType(database.PowerShortToFull(system_power_shortcode), power)
	switch activity_type {
	case TASK_UNDERMINE:
		//hostile system, find friendly one to give data to
		query = `SELECT powerdata.*,
		` + database.CreateDistanceStatement(user_coords) + `
		FROM powerdata
		INNER JOIN systems
			ON systems.system_name = powerdata.system_name
		WHERE powerdata.shortcode = '` + user_shortcode + `'
			AND powerdata.state != ''
		ORDER BY distance
		LIMIT 1;`
		information += "an enemy system, so you need to download " + data_type + " from an odyssey settlement here and hand it into a power contact in <owned system>, which is <distance> LY away"
	case TASK_AQUIRE:
		//unoccupied system, find friendly one to give data to
		query = `SELECT powerdata.*,
		` + database.CreateDistanceStatement(user_coords) + `
		FROM powerdata
		INNER JOIN systems
			ON systems.system_name = powerdata.system_name
		WHERE powerdata.shortcode = '` + user_shortcode + `'
			AND powerdata.state != ''
		ORDER BY distance
		LIMIT 1;`
		information += "a unoccupied system, so you need to download " + data_type + " from an odyssey settlement here and hand it into a power contact in <owned system>, which is <distance> LY away"

	case TASK_REINFORCE:
		//user in friendly system, find nearby one to undermine
		//You are in a friendly system
		query = `SELECT powerdata.*,
		` + database.CreateDistanceStatement(user_coords) + `
		FROM powerdata
		INNER JOIN systems
			ON systems.system_name = powerdata.system_name
		WHERE powerdata.shortcode != '` + user_shortcode + `'
			AND powerdata.state != ''
		ORDER BY distance
		LIMIT 1;`
		information += "a friendly system, so you need to download " + data_type + " from an odyssey settlement here and hand it into a local power contact "

	}

	rows, err := database.Db.Query(query)
	if err != nil {
		log.Panic(err.Error())
	}

	s := powerdata_location_response{}

	for rows.Next() {

		err = rows.Scan(&s.System_name, &s.Shortcode, &s.State, &s.Control_points, &s.Points_change, &s.Distance)
		if err != nil {
			log.Panic(err.Error())
		}
	}

	information = strings.Replace(information, "<owned system>", s.System_name, 1)
	information = strings.Replace(information, "<distance>", ftos(math.Round(s.Distance)), 1)

	if activity_type == TASK_AQUIRE && ((s.Distance > STRONGHOLD_DATA_LIMIT && s.State == "Stronghold") || (s.Distance > FORTIFIED_DATA_LIMIT && s.State == "Fortified")) {
		//system out of range
		information = "Your power does not control a fortified system within 20 LY or stronghold within 30 LY, so this task is not possible here. Sorry about that."
	} else if activity_type == TASK_REINFORCE {
		s.System_name = system
	}

	return c.HTML(200, utils.RenderTemplate(ody_html_template, map[string]any{
		"system":             system,
		"power":              power,
		"task":               task,
		"currentPower":       database.PowerShortToFull(system_power_shortcode),
		"currentState":       system_state,
		"isAnarchy":          database.IsSystemAnarchy(system),
		"systemNotes":        database.GetExtraInfo(system),
		"taskName":           task,
		"taskType":           "Odyssey",
		"taskDescription":    utils.TASK_DESCRIPTIONS[task_shortcode], // + " " + information,
		"isIllegal":          "is",
		"isOpposingWeakness": utils.IsOpposingWeakness(task_shortcode, system_power_shortcode),
		"isOwnStrength":      utils.IsOwnStrength(task_shortcode, system_power_shortcode),
		"information":        information,
		"targetSystem":       s.System_name,
	}))

}

/*
Undermine - Obtain Tracker Malware from control system, upload to settlement data port in undermine
Aqusition - Obtain Injection Malware from control system and upload to settlement data port in aqusition
Reinforce - N/A
*/
func HandleOdysseyMalware(c *echo.Context) error {
	system := c.QueryParam("system")
	power := c.QueryParam("power")
	task := c.QueryParam("task")

	task_shortcode := utils.GetTaskCode(task)
	user_shortcode := database.PowerFullToShort(power)
	system_state, system_power_shortcode := database.GetSystemPowerInfo(power)
	user_coords := database.GetSystemLocation(system)

	var information string
	var s powerdata_location_response

	if user_shortcode == system_power_shortcode {
		//in friendly sys, find nearby enemy or unoccupied sys
		rows, err := database.Db.Query(`SELECT powerdata.*,
		` + database.CreateDistanceStatement(user_coords) + `
		FROM powerdata
		INNER JOIN systems
			ON systems.system_name = powerdata.system_name
		WHERE powerdata.shortcode != '` + user_shortcode + `'
		ORDER BY distance
		LIMIT 1;`)
		if err != nil {
			log.Panic(err.Error())
		}

		err = rows.Scan(&s.System_name, &s.Shortcode, &s.State, &s.Control_points, &s.Points_change, &s.Distance)
		if err != nil {
			log.Panic(err.Error())
		}
		if s.State != "Unoccupied" {
			//Aqusition - needs injection malware
			information = "You will need 'Power Injection Malware', which can be found at a power contact in this system. "
		} else {
			//Undermining - needs tracker malware
			information = "You will need 'Power Tracker Malware', which can be found at a power contact in this system. "
		}
		information += "Then head to '" + s.System_name + "', and upload it to a data port at any odyssey settlement."
	} else if slices.Contains(utils.POWERNAMES, database.PowerShortToFull(system_power_shortcode)) {
		//enemy sys, find nearby friendly sys to obtain tracker malware
	} else {
		//unoccupied sys, find nearby freindly sys to obtain injection malware
	}

	return c.HTML(200, utils.RenderTemplate(ody_html_template, map[string]any{
		"system":             system,
		"power":              power,
		"task":               task,
		"currentPower":       database.PowerShortToFull(system_power_shortcode),
		"currentState":       system_state,
		"isAnarchy":          database.IsSystemAnarchy(system),
		"systemNotes":        database.GetExtraInfo(system),
		"taskName":           task,
		"taskType":           "Odyssey",
		"taskDescription":    utils.TASK_DESCRIPTIONS[task_shortcode], // + " " + information,
		"isIllegal":          "is",
		"isOpposingWeakness": utils.IsOpposingWeakness(task_shortcode, system_power_shortcode),
		"isOwnStrength":      utils.IsOwnStrength(task_shortcode, system_power_shortcode),
		"information":        information,
		"targetSystem":       s.System_name,
	}))
}
