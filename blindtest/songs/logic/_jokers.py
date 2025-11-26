import dataclasses
from typing import TYPE_CHECKING, Any, Optional, Protocol, Union

if TYPE_CHECKING:
    from songs.logic.base import Player

SongType = Optional[dict[str, Union[str, int]]]


class JokerProtocol(Protocol):
    history: list[dict[str, str]]

    def __init__(self, player: 'Player'): ...

    async def __call__(self, song: SongType, players: dict[str, 'Player']):
        ...


class BaseJoker:
    history: list[dict[str, str]] = []
    use_side_effects: bool = False

    def __init__(self, player: 'Player'):
        self.player = player
        # If True, the joker will consider the song difficulty
        self.use_song_difficulty = False
        # If True, the joker will have side effects on the
        # player who has also used the joker

    def __call__(self, song: SongType, **kwargs: Any):
        """Main entry function to be called when a joker is used. The `player` 
        parameter is the id of the player who used the joker.
        """
        raise NotImplementedError

    def __str__(self):
        name = self.__class__.__name__
        return f'<{name}: {self.player}>'


class TheStealerJoker(BaseJoker):
    """This joker allows the player who used the joker to steal points
    from another player who has answered correctly. If side effects are
    activated, the player who used the joker will therefore lose points
    """

    async def __call__(self, song, winner_or_looser: 'Player', is_winner: bool = True):
        if self.use_side_effects:
            if is_winner:
                winner_or_looser.points = winner_or_looser.points - winner_or_looser.gain
                self.player.points += winner_or_looser.gain
                winner_or_looser.gain = 0
            else:
                self.player.points = self.player.points - winner_or_looser.gain
                self.player.gain = 0
        else:
            winner_or_looser.points = winner_or_looser.points - winner_or_looser.gain
            self.player.points += winner_or_looser.gain
            winner_or_looser.gain = 0



class ForMankind(BaseJoker):
    """This joker allows the player who used the joker to steal one point
    from every other player if he answered correctly but makes every other player
    gain one point if he answered wrongly
    """

    use_side_effects = True

    async def __call__(self, song, players: dict[str, 'Player'], is_winner: bool = True):
        for key, player in players.items():
            if is_winner:
                if player.id != self.player.id:
                    player.points -= 1
                    self.player.points += 1
            else:
                if player.id != self.player.id:
                    player.points += 1
                    self.player.points -= 1
