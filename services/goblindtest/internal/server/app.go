package server

import (
	"context"
	"fmt"
	"myblindtest/goblindtest/internal/app"
	"myblindtest/goblindtest/internal/logic"
	"myblindtest/goblindtest/internal/models"
	"sync/atomic"
)

type ServerApp struct {
	isStarted atomic.Bool
}

func (s *ServerApp) IsStarted() bool {
	return s.isStarted.Load()
}

func (s *ServerApp) Start(ctx context.Context) {
	serverCtx, cancel := context.WithCancel(ctx)
	defer cancel()

	options := models.CreateServerContext(s)

	gameApp := logic.NewGameApp(serverCtx, options)
	gameApp.Start()

	options.SetGameApp(gameApp)

	httpApp := app.NewApp(serverCtx, options)

	go func() {
		httpApp.Start()
	}()

	s.isStarted.Store(true)

	<-serverCtx.Done()

	fmt.Println("🔴 Stopping server...")
}

func (s *ServerApp) GetServer() models.ServerInterface {
	return s
}

func NewServer(ctx context.Context) models.ServerInterface {
	return &ServerApp{}
}
