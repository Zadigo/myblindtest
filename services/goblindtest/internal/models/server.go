package models

import (
	"context"
)

type ServerInterface interface {
	Start(ctx context.Context)
	GetServer() ServerInterface
}

type ServerContext struct {
	server  ServerInterface
	gameApp AppInterface
}

func (s *ServerContext) GetServer() ServerInterface {
	return s.server
}

func (s *ServerContext) GetGameApp() AppInterface {
	return s.gameApp
}

func (s *ServerContext) SetGameApp(app AppInterface) {
	s.gameApp = app
}

func CreateServerContext(server ServerInterface) *ServerContext {
	return &ServerContext{
		server: server,
	}
}
