package __test

import (
	"log"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/labstack/echo/v5"
	"niceygy.net/powerplay-assistant/src/handlers"
	"niceygy.net/powerplay-assistant/src/utils"
)

// const server_address string = "http://localhost:8080"
const test_system string = "64 Ceti"
const test_power string = "Li Yong-Rui"

var routes map[string]echo.HandlerFunc = map[string]echo.HandlerFunc{
	"/": handlers.HandleIndex,
}

// var recorders map[*http.Request]*httptest.ResponseRecorder = make(map[*http.Request]*httptest.ResponseRecorder)

func TestPages(t *testing.T) {
	e := echo.New()

	for route, handler := range routes {

		// Register the same handler
		e.Any(route, handler)

		// Create a request
		req := httptest.NewRequest(http.MethodGet, "/", nil)
		rec := httptest.NewRecorder()

		e.ServeHTTP(rec, req)

		// Assert status code
		if rec.Code != http.StatusOK {
			t.Fatalf("expected 200, got %d", rec.Code)
		} else {
			log.Println("200 OK for " + route)
		}
	}

	e.Any("/results", handlers.HandleResults)

	for i := range utils.TASK_NAMES {
		task := utils.TASK_NAMES[i]
		url := strings.ReplaceAll(utils.Concat([]string{
			"/results?system=",
			test_system,
			"&power=",
			test_power,
			"&task=",
			task,
		}), " ", "%20")

		// Create a request
		req := httptest.NewRequest(http.MethodGet, url, nil)
		// req.SetPathValue("system", test_system)
		// req.SetPathValue("power", test_power)
		// req.SetPathValue("task", task)
		// log.Println(req.RequestURI)
		rec := httptest.NewRecorder()

		e.ServeHTTP(rec, req)

		// Assert status code
		if rec.Code != http.StatusOK {
			t.Errorf("expected 200, got %d for %s", rec.Code, url)
		} else {
			log.Println("200 OK for Task=" + task + ", Sys=" + test_system + ", Power=" + test_power)
		}
		time.Sleep(time.Millisecond * 250)
	}
}
