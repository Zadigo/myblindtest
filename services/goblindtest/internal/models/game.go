package models

import (
	"strings"
	"sync"
	"sync/atomic"
)

const (
	All       string = "all"
	Easy      string = "easy"
	Medium    string = "medium"
	SemiPro   string = "semi-pro"
	Difficult string = "difficult"
	Expert    string = "expert"
)

type BaseAnswer struct{}

type CorrectAnswers struct {
	BaseAnswer
}

type Song struct {
	ID    int
	Genre string
}

type Blindtest struct {
	ID                    string
	Difficulty            string
	GameDuration          int
	CurrentSong           *Song
	PlayedSongs           []*Song
	IsStarted             atomic.Bool
	CurrentRound          atomic.Int32
	PointLimit            int
	GenreSelected         string
	NumberOfRounds        int
	PointValue            int
	SongDifficultyBonus   bool
	SpeedBonus            bool
	ConnectionToken       string
	SoloMode              bool
	AdminPlays            bool
	TimeLimit             int
	TimeRange             []int
	MultipleChoiceAnswers bool
	NumberOfChoices       int
	Pause                 atomic.Bool
	songs                 []*Song
	clients               sync.Map
	send                  chan []byte
	mu                    sync.RWMutex
}

func (b *Blindtest) GetID() string {
	return b.ID
}

func (b *Blindtest) GetClients() *sync.Map {
	return &b.clients
}

func (b *Blindtest) GetCurrentSong() *Song {
	return b.CurrentSong
}

func (b *Blindtest) AddPlayer(client *Client) {
	b.clients.Store(client.ID, client)
}

func (b *Blindtest) RemovePlayer(client *Client) {
	b.clients.Delete(client.ID)
}

func (b *Blindtest) Reset() {
	b.mu.Lock()
	defer b.mu.Unlock()

	b.CurrentRound.Store(0)
	b.Pause.Store(false)
	b.PlayedSongs = nil
}

func (b *Blindtest) IncreaseRound() {
	b.CurrentRound.Add(1)
}

func (b *Blindtest) CurrentSongID() int {
	if b.CurrentSong == nil {
		return 0
	} else {
		return b.CurrentSong.ID
	}
}

func (b *Blindtest) AddClient(client *Client) {
	b.clients.Store(client.ID, client)
}

func (b *Blindtest) GetSong(id int) *Song {
	return nil
}

func (b *Blindtest) GetSongs(temporaryGenre string) []*Song {
	filteredSongs := []*Song{}
	for _, s := range b.songs {
		if s.Genre == temporaryGenre {
			filteredSongs = append(filteredSongs, s)
		}
	}
	return filteredSongs
}

func (b *Blindtest) GetSongIds() []int {
	ids := []int{}
	for _, s := range b.songs {
		ids = append(ids, s.ID)
	}
	return ids
}

func (b *Blindtest) NextSong() {

}

func (b *Blindtest) calculateMultipleChoicePoints() {

}

func (b *Blindtest) calculateSimplePoints() {

}

func (b *Blindtest) calculateLoosersLoosesPoints() {

}

func (b *Blindtest) CalculatePoints(titleMatch bool, artistMatch bool) {
	if titleMatch {
		b.calculateSimplePoints()
	}

	if artistMatch {
		b.calculateMultipleChoicePoints()
	}
}

func (b *Blindtest) HandleGuess() {
	strings.Trim("", " ")
}
