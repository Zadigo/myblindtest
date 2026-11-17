package models

type AppInterface interface {
	GetID() string
	Start()
}
