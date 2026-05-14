package database

import (
	"strconv"
	"strings"

	"niceygy.net/powerplay-assistant/src/utils"
)

var SPANSH_ID64_CACHE map[string]float64

func getSystemID64(system_name string) float64 {
	for k, v := range SPANSH_ID64_CACHE {
		if k == system_name {
			return v
		}
	}

	url := "https://www.spansh.co.uk/api/search?q=" + strings.ReplaceAll(system_name, " ", "%20")

	jsonRes := utils.HTTPGetJSON(url)

	SPANSH_ID64_CACHE[system_name] = jsonRes["results"].(map[any]any)[0].(map[any]any)["id64"].(float64)
	return jsonRes["results"].(map[any]any)[0].(map[any]any)["id64"].(float64)
}

func ftos(f float64) string {
	return strconv.FormatFloat(f, 'g', 5, 64)
}

type FormattedSpanshResponse struct {
	SystemName string
}

func GetSystemSpanshInfo(system_name string) {
	// id64 := getSystemID64(system_name)
	// url := "https://www.spansh.co.uk/api/system/" + ftos(id64)

	// jsonRes := utils.HTTPGetJSON(url)

}
