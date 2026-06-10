package logic

import (
	"github.com/Zadigo/gojokers/internal/models"
	"github.com/google/uuid"
)

// TheStealerJoker allows the player who used the joker to steal points
// from another player who has answered correctly. If side effects are
// activated, the player who used this joker will therefore lose points
type TheStealer struct {
	models.JokerProperties
}

func (ts *TheStealer) ApplyEffect(players *models.PlayerRegistry, options models.ApplyEffectOptions) error {
	if ts.UseSideEffects {
		if options.IsWinner {
			options.WinnerOrLooser.Points = options.WinnerOrLooser.Points - options.WinnerOrLooser.Gain
			ts.Owner.Points += options.WinnerOrLooser.Gain
		} else {
			ts.Owner.Points = ts.Owner.Points - options.WinnerOrLooser.Gain
		}
	} else {
		options.WinnerOrLooser.Points = options.WinnerOrLooser.Points - options.WinnerOrLooser.Gain
		ts.Owner.Points += options.WinnerOrLooser.Gain
	}
	options.WinnerOrLooser.Gain = 0
	ts.Owner.Gain = 0
	return nil
}

// ForMankind allows the player who used the joker to steal one point
// from every other player if he answered correctly but makes every other player
// gain one point if he answered wrongly
type ForManking struct {
	models.JokerProperties
}

func (fm *ForManking) ApplyEffect(players *models.PlayerRegistry, options models.ApplyEffectOptions) error {
	for _, player := range players.Players {
		if options.IsWinner {
			if player.Id != options.WinnerOrLooser.Id {
				player.Points = player.Points - 1
				fm.Owner.Points += 1
			}
		} else {
			if player.Id != options.WinnerOrLooser.Id {
				player.Points += 1
				fm.Owner.Points -= 1
			}
		}
	}
	return nil
}

type PerfectCombo struct {
	models.JokerProperties
}

func (pc *PerfectCombo) ApplyEffect(players *models.PlayerRegistry, options models.ApplyEffectOptions) error {
	// Implementation of the effect of Perfect Combo joker
	return nil
}

func NewJoker(jokerType string, owner *models.Player) models.JokerInterface {
	jokerId := uuid.NewString()

	switch jokerType {
	case "the-stealer":
		return &TheStealer{
			JokerProperties: models.JokerProperties{
				Uuid:           jokerId,
				UseSideEffects: false,
				Owner:          owner,
			},
		}
	case "for-manking":
		return &ForManking{
			JokerProperties: models.JokerProperties{
				Uuid:           jokerId,
				UseSideEffects: true,
				Owner:          owner,
			},
		}
	case "perfect-combo":
		return &PerfectCombo{
			JokerProperties: models.JokerProperties{
				Uuid:           jokerId,
				UseSideEffects: false,
				Owner:          owner,
			},
		}
	default:
		return nil
	}
}
