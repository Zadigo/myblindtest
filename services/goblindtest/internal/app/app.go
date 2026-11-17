package app

import (
	"context"
	"fmt"
	"myblindtest/goblindtest/internal/models"
	"sync"
)

type App struct {
	clients       sync.Map
	serverOptions *models.ServerContext
}

func (a *App) AddClient(client *models.Client) {
	a.clients.Store(client.ID, client)
}

func (a *App) RemoveClient(client *models.Client) {
	a.clients.Delete(client.ID)
}

func (a *App) Start() {
	fmt.Println("⚡️ Start HTTP application...")

}

func NewApp(ctx context.Context, options *models.ServerContext) *App {
	if options.GetServer() == nil {
		panic("server is nil")
	}

	app := &App{serverOptions: options}
	return app
}
