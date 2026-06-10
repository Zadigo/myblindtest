package main

import "github.com/Zadigo/gojokers/internal/server"

func main() {
	app := server.NewApp()
	err := app.Start()
	if err != nil {
		// Handle the error
	}
}
