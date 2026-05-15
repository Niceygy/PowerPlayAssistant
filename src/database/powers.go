package database

import (
	"math"
	"time"

	"niceygy.net/powerplay-assistant/src/utils"
)

func PowerFullToShort(power string) string {
	for k, v := range utils.POWERS {
		if v == power {
			return k
		}
	}
	return ""
}

func PowerShortToFull(shortcode string) string {
	return utils.POWERS[shortcode]
}

func DoesSystemExist(system_name string) bool {
	res := Db.QueryRow("SELECT system_name FROM star_systems WHERE system_name = '?' LIMIT 1;", system_name)
	system := StarSystem{}
	res.Scan(&system.System_name)
	return system.System_name == ""
}

// [state, shortcode]
func GetSystemPowerInfo(system_name string) (string, string) {
	if !DoesSystemExist(system_name) {
		return "", ""
	}
	res /*, err*/ := Db.QueryRow("SELECT state, shortcode FROM powerdata WHERE system_name = '" + system_name + "';" /*, system_name*/)
	// if err != nil {
	// 	panic(err)
	// }

	pd := PowerData{}
	err := res.Scan(&pd.State, &pd.Shortcode)
	if err != nil {
		// log.Panic(err.Error())
		//unoccupied
		return "Unoccupied", ""
	}
	return pd.State, pd.Shortcode
}

func GetPowerplayCycle() int {
	start_date := time.Date(2024, 10, 31, 8, 0, 0, 0, time.UTC)
	now := time.Now()

	diff := now.UTC().Sub(start_date)
	return int(math.Round(diff.Hours() / 24))
} //Whats the cycle?
