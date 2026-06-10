from abc import ABC, abstractmethod
from typing import Any, Protocol

from songs.typings import PlayersDictType, PlayerType, SongDictType


class JokerProtocol(Protocol):
    history: list[dict[str, str]]

    def __init__(self, player: PlayerType): ...

    async def __call__(self, song: SongDictType, players: PlayersDictType):
        ...


class BaseJoker(ABC):
    """Base class for all jokers. All jokers should inherit from 
    this class and implement the `__call__` method.

    The `__call__` method should be the main entry point for the joker and 
    will be called when the joker is used. The `player` parameter is the id of 
    the player who used the joker.

    Args:
        player (PlayerType): The player who used the joker.
    """

    history: list[dict[str, str]] = []
    # If True, the joker will have side effects on the
    # player who has also used the joker
    use_side_effects: bool = False

    def __init__(self, player: PlayerType):
        self.player = player
        # If True, the joker will consider the song difficulty
        self.use_song_difficulty = False

    def __str__(self):
        name = self.__class__.__name__
        return f'<{name}: {self.player}>'

    @abstractmethod
    def __call__(self, song: SongDictType, **kwargs: Any):
        """Main entry function to be called when a joker is used. The `player` 
        parameter is the id of the player who used the joker.
        """
        raise NotImplementedError


class TheStealerJoker(BaseJoker):
    """TheStealerJoker allows the player who used the joker to steal points
    from another player who has answered correctly. If side effects are
    activated, the player who used this joker will therefore lose points
    """

    async def __call__(self, song: SongDictType, winner_or_looser: PlayerType, is_winner: bool = True):
        """
        Args:
            song (SongDictType): The song for which the joker is being used.
            winner_or_looser (PlayerType): The player who answered the question (either correctly or wrongly depending on the value of `is_winner`).
            is_winner (bool): Whether the player who used the joker answered correctly or not. Defaults to True.
        """
        if self.use_side_effects:
            if is_winner:
                winner_or_looser.points = winner_or_looser.points - winner_or_looser.gain
                self.player.points += winner_or_looser.gain
            else:
                self.player.points = self.player.points - winner_or_looser.gain
        else:
            winner_or_looser.points = winner_or_looser.points - winner_or_looser.gain
            self.player.points += winner_or_looser.gain

        self.player.gain = 0
        winner_or_looser.gain = 0


class ForMankind(BaseJoker):
    """ForMankind allows the player who used the joker to steal one point
    from every other player if he answered correctly but makes every other player
    gain one point if he answered wrongly
    """

    use_side_effects = True

    async def __call__(self, song: SongDictType, players: PlayersDictType, is_winner: bool = True):
        """
        Args:
            song (SongDictType): The song for which the joker is being used.
            players (PlayersDictType): The players in the current game state.
            is_winner (bool): Whether the player who used the joker answered correctly or not. Defaults to True.
        """
        for _, other_player in players.items():
            if is_winner:
                if other_player.id != self.other_player.id:
                    other_player.points -= 1
                    self.player.points += 1
            else:
                if other_player.id != self.player.id:
                    other_player.points += 1
                    self.player.points -= 1
