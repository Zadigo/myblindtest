package backend

import (
	"context"

	"github.com/Zadigo/gojokers/internal/models"
	"github.com/redis/go-redis/v9"
)

type JokerRedis struct {
	ctx         context.Context
	redisClient *redis.Client
}

func (r *JokerRedis) LinkToPlayer(player *models.Player, joker models.JokerInterface) error {
	return r.redisClient.HSet(r.ctx, models.GetKey("jokers"), player.Id, joker).Err()
}

func (r *JokerRedis) UseJoker(players *models.PlayerRegistry, playerId string) (models.JokerInterface, error) {
	var joker models.JokerInterface

	err := r.redisClient.HGet(r.ctx, models.GetKey("jokers"), playerId).Scan(&joker)
	if err != nil {
		return nil, err
	}

	joker.ApplyEffect(players, models.ApplyEffectOptions{
		WinnerOrLooser: nil,   // You need to provide the appropriate player here
		IsWinner:       false, // You need to provide the appropriate value here
	})

	r.redisClient.HDel(r.ctx, models.GetKey("jokers"), playerId)
	return joker, nil
}

func (r *JokerRedis) HasJoker(playerId string) error {
	return r.redisClient.HExists(r.ctx, models.GetKey("jokers"), playerId).Err()
}

func NewJokerRedis(redisClient *redis.Client) *JokerRedis {
	return &JokerRedis{
		redisClient: redisClient,
	}
}
