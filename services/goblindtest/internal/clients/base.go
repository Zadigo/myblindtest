package clients

import (
	"myblindtest/goblindtest/internal/models"
	"uuid"

	"github.com/gorilla/websocket"
)

func NewClient(conn *websocket.Conn) *models.Client {
	client := &models.Client{ID: uuid.New().String()}
	client.SetConn(conn)
	return client
}
