package main

import (
	"embed"
	"log"
	"os"

	"github.com/goforj/godump"
	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"

	"niceygy.net/powerplay-assistant/src/handlers"
	"niceygy.net/powerplay-assistant/src/utils"
)

//go:embed templates/*
var htmlTemplates embed.FS

//go:embed static/*
var staticFiles embed.FS

var isDebugMode bool = os.Getenv("DEBUG") == "true"

func main() {
	utils.HTMLTemplates = htmlTemplates
	// Echo instance
	e := echo.New()

	d := godump.NewDumper(godump.WithoutColor())

	// Middleware
	limiterStore := middleware.NewRateLimiterMemoryStore(10)
	e.Use(middleware.RateLimiter(limiterStore))
	e.Use(middleware.Secure())
	e.Use(middleware.Decompress())
	if !isDebugMode {
		e.Use(middleware.RecoverWithConfig(middleware.RecoverConfig{
			DisablePrintStack: true,
		})) // recover panics as errors for proper error handling
	} else {
		log.Println("PowerPlayAssistant in debug mode, error recovery inactive.")
	}
	fs := echo.MustSubFS(staticFiles, "static")
	e.StaticFS("/static", fs, e.Middlewares()...)
	e.RouteNotFound("/*", func(c *echo.Context) error {
		return c.HTML(404, utils.RenderTemplate("templates/errors/404.html", map[string]any{}))
	})
	e.RouteNotFound("/static", func(c *echo.Context) error {
		return c.HTML(404, utils.RenderTemplate("templates/errors/404.html", map[string]any{}))
	})

	e.HTTPErrorHandler = func(c *echo.Context, err error) {
		c.HTML(500, utils.RenderTemplate("templates/errors/500.html", map[string]any{
			"info":  d.DumpStr(err.Error()),
			"stack": d.DumpStr(c.Request()), //"Whoopsie. Looks like there is nothing here. Ironic, really. An error in the error handler. Anyways, how are you? Doing well I hope?",
		}))
	}

	// Routes
	e.Any("/", handlers.HandleIndex)
	e.Any("/results", handlers.HandleResults)
	e.Any("/handle_choice", handlers.HandleTaskChoice)
	e.Any("/search_systems", handlers.HandleSystemSearch)
	e.Any("/is_crime", handlers.HandleIsCrime)

	// Start server
	if err := e.Start(":8080"); err != nil {
		log.Panic("failed to start server", "error", err)
	}
}
