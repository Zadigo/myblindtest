package logic

import (
	"context"
	"myblindtest/goblindtest/internal/models"
	"sync"
	"uuid"
)

type GameApp struct {
	ID         string
	options    *models.ServerContext
	blindtests sync.Map
}

func (g *GameApp) GetID() string {
	return g.ID
}

func (g *GameApp) Start() {

}

func (g *GameApp) GetOptions() *models.ServerContext {
	return g.options
}

func (g *GameApp) CreateBlindtest() {
	blindtest := &models.Blindtest{ID: uuid.New().String()}
	g.blindtests.Store(blindtest.ID, blindtest)
}

func (g *GameApp) GetBlindtest(id string) (*models.Blindtest, bool) {
	v, ok := g.blindtests.Load(id)
	return v.(*models.Blindtest), ok
}

func NewGameApp(ctx context.Context, options *models.ServerContext) *GameApp {
	if options.GetServer() == nil {
		panic("Server is nil")
	}

	return &GameApp{
		ID:         uuid.New().String(),
		options:    options,
		blindtests: sync.Map{},
	}
}
