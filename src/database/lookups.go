package database

import (
	"log"
	"strings"

	"niceygy.net/powerplay-assistant/src/utils"
)

func GetSystemLocation(system_name string) System {
	res := Db.QueryRow("SELECT latitude, longitude, height FROM systems WHERE system_name = ? LIMIT 1;", system_name)
	system := System{}
	res.Scan(&system.Latitude, &system.Longitude, &system.Height)
	return system //[]float64{system.Latitude, system.Longitude, system.Height}
}

func GetExtraInfo(system_name string) string {
	var result strings.Builder

	for _, v := range utils.PERMITLOCKED {
		if system_name == v {
			result.WriteString("This system is permit locked. Check you can get here! ")
		}
	}

	for k, v := range utils.HOMESYSTEMS {
		if k == system_name {
			result.WriteString("This is the home system of " + utils.POWERS[v] + ". Opposing powers will not be welcome here! ")
		}
	}

	state, _ := GetSystemPowerInfo(system_name)
	if state == "Stronghold" {
		result.WriteString("Warning! This is a stronghold system. Opposing powers will not be welcome here. ")
	}

	return result.String()
}

func IsSystemAnarchy(system_name string) bool {
	res, err := Db.Query("SELECT is_anarchy FROM systems WHERE system_name = ? LIMIT 1;", system_name)
	if err != nil {
		log.Panic(err)
	}
	var is_anarchy bool
	res.Scan(&is_anarchy)
	return is_anarchy
}

// Returns system_name, system_coords[]
func GetNearestOwnedSystem(current_system string, needed_system_type string, power_full string) (string, []float64) {
	user_coords := GetSystemLocation(current_system)
	rows, err := Db.Query(`SELECT
	system_name, longitude, latitude, height,
	` + CreateDistanceStatement(user_coords) + `
	FROM systems
	WHERE systems.state = '` + needed_system_type + `' 
		AND systems.shortcode = '` + PowerFullToShort(power_full) + `'
	ORDER BY distance
	LIMIT 1;`)

	if err != nil {
		log.Panic(err.Error())
	}

	var result_system_name string
	var result_system_coords []float64

	for rows.Next() {
		var x float64
		var y float64
		var z float64
		var distance float64
		if err = rows.Scan(&result_system_name, &x, &y, &z, &distance); err != nil {
			log.Panic(err.Error())
		} else {
			result_system_coords = []float64{x, y, z}
		}
	}
	return result_system_name, result_system_coords
}
