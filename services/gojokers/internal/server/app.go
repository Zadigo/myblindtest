package server

import (
	"context"
	"net/http"

	"github.com/Zadigo/gojokers/internal/models"
	"github.com/go-chi/chi"
	"github.com/redis/go-redis/v9"
)

type App struct {
	ctx            context.Context
	playerRegistry *models.PlayerRegistry
	redisClient    *redis.Client
	router         *chi.Mux
}

func (a *App) Start() error {
	server := &http.Server{
		Addr:    ":8080",
		Handler: a.router,
	}

	if a.redisClient == nil {
		panic("Redis client is not initialized")
	}

	err := a.redisClient.Ping(a.ctx).Err()
	if err != nil {
		return err
	}

	ch := make(chan error, 1)

	go func() {
		err := server.ListenAndServe()
		if err != nil && err != http.ErrServerClosed {
			ch <- err
		}
	}()

	return nil
}

func NewApp() *App {
	client := redis.NewClient(&redis.Options{
		Addr: "localhost:6379",
	})

	app := &App{
		playerRegistry: models.NewPlayerRegistry(),
		redisClient:    client,
	}

	app.setupRoutes()
	return app
}
