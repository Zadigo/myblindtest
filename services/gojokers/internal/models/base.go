package models

type ApplyEffectOptions struct {
	Song           Song    `json:"song"`
	WinnerOrLooser *Player `json:"winner_or_looser"`
	IsWinner       bool    `json:"is_winner"`
}

type PlayerRegistry struct {
	Players []*Player `json:"players"`
}

func NewPlayerRegistry() *PlayerRegistry {
	return &PlayerRegistry{
		Players: []*Player{},
	}
}

type Player struct {
	Id     string `json:"id"`
	Points uint   `json:"points"`
	Gain   uint   `json:"gain"`
}

type Song struct{}

type JokerProperties struct {
	Uuid string `json:"uuid"`
	// If True, the joker will have side effects on the
	// player who has also used the joker
	UseSideEffects bool `json:"use_side_effects"`
	// The player who owns the joker
	Owner *Player `json:"owner"`
}

type JokerInterface interface {
	ApplyEffect(players *PlayerRegistry, options ApplyEffectOptions) error
}
