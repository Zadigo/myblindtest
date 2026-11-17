package models

import (
	"sync/atomic"

	"github.com/gorilla/websocket"
)

type BaseWsClient struct {
	ID             string
	conn           *websocket.Conn
	Position       int
	Name           string
	Color          string
	Gain           int64
	Team           string
	Speciality     string
	CorrectAnswers CorrectAnswers
	Points         atomic.Int64
}

func (b *BaseWsClient) SetConn(conn *websocket.Conn) {
	b.conn = conn
}

func (b *BaseWsClient) AddPoints(p int64) {
	b.Points.Add(p)
}

func (b *BaseWsClient) SubstractPoints(p int64) int64 {
	return b.Points.Add(-p)
}

func (b *BaseWsClient) GetPoints() int64 {
	return b.Points.Load()
}

type Client struct {
	BaseWsClient
}
