package main

import (
	"log"
	"log/slog"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"

	"niceygy.net/powerplay-assistant/src/handlers"
	"niceygy.net/powerplay-assistant/src/utils"
)

func main() {
	// Echo instance
	e := echo.New()

	// Middleware
	limiterStore := middleware.NewRateLimiterMemoryStore(10)
	e.Use(middleware.RateLimiter(limiterStore))
	// e.Use(middleware.Gzip())
	e.Use(middleware.Secure())
	e.Use(middleware.Decompress())
	// e.Use(middleware.RequestLoggerWithConfig(middleware.RequestLoggerConfig{
	// 	LogValuesFunc: func(c *echo.Context, v middleware.RequestLoggerValues) error {
	// 		log.Println("Route = " + c.Path() + ", Method = " + c.Request().Method)
	// 		return nil
	// 	},
	// }))
	// e.Use(middleware.RequestLogger()) // use the RequestLogger middleware with slog logger
	e.Use(middleware.Recover()) // recover panics as errors for proper error handling
	e.Static("/static/", "static", e.Middlewares()...)
	e.RouteNotFound("/*", func(c *echo.Context) error {
		log.Println("[404] Not Found: " + c.Path())
		return c.HTML(404, utils.RenderTemplate("templates/errors/404.html", map[string]any{}))
	})

	e.HTTPErrorHandler = func(c *echo.Context, err error) {
		c.HTML(500, utils.RenderTemplate("templates/errors/500.html", map[string]any{
			"info":  err.Error(),
			"stack": "Whoopsie. Looks like there is nothing here. Ironic, really. An error in the error handler. Anyways, how are you? Doing well I hope?",
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
		slog.Error("failed to start server", "error", err)
	}
}
