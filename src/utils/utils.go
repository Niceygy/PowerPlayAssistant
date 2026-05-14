package utils

import (
	"encoding/json"
	"log"
	"net/http"
	"slices"
	"strings"
	"time"
)

func Concat(parts []string) string {
	return strings.Join(parts, "")
}

// use shortcodes
func IsOpposingWeakness(task string, power_shortcode string) string {
	for k := range POWERWEAKNESSES {
		if k == power_shortcode {
			if slices.Contains(POWERWEAKNESSES[k], task) {
				return "is"
			}
		}
	}
	return "isn't"
}

func IsOwnStrength(task_code string, power_shortcode string) string {
	for k, v := range POWER_RENFORCE_PREFERENCES {
		if k == power_shortcode {
			if slices.Contains(v, task_code) {
				return "is"
			}
		}
	}
	return "isn't"
}

func HTTPGetJSON(url string) map[any]any {
	res, err := http.Get(url)

	if err != nil {
		log.Panic(err)
	}

	var jsonRes map[any]any
	var bytesRes []byte

	_, err = res.Body.Read(bytesRes)

	if err = json.Unmarshal(bytesRes, &jsonRes); err != nil {
		log.Panic(err)
	}
	return jsonRes
}

func GetPowerplayCycle() int {
	powerplay_startdate := time.Date(2024, 10, 31, 8, 0, 0, 0, time.UTC)
	now := time.Now().UTC()

	days := now.Sub(powerplay_startdate).Hours() / 24
	weeks := days / 7

	return int(weeks)
}

func GetTaskType(task string) string {
	taskShortCode := ""
	for key, value := range TASKSHORTCODES {
		if task == value {
			taskShortCode = key
		}
	}
	for taskType, tasks := range TASKTYPES {
		if slices.Contains(tasks, taskShortCode) {
			return taskType
		}
	}
	return ""
}

func GetTaskCode(task string) string {
	for k, v := range TASKSHORTCODES {
		if v == task {
			return k
		}
	}

	return ""
}
