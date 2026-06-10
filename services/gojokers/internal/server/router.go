package server

import (
	"time"

	"github.com/Zadigo/gojokers/internal/handlers"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
)

func (a *App) setupRoutes() {
	router := chi.NewRouter()
	router.Use(middleware.RealIP)
	router.Use(middleware.RequestID)
	router.Use(middleware.Recoverer)
	router.Use(middleware.Timeout(60 * time.Second))
	router.Use(middleware.AllowContentType("application/json"))
	router.Use(middleware.Heartbeat("/health"))
	router.Use(middleware.Logger)
	router.Route("/", a.loadBaseRoutes)
	a.router = router
}

func (a *App) loadBaseRoutes(r chi.Router) {
	handler := handlers.NewConnectionHandler()
	r.Get("/ws/connect", handler.GetConnection)
}
