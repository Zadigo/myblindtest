import dataclasses
from collections import defaultdict
from typing import List, Optional, Union

from songs.song_typings import DictAny


@dataclasses.dataclass
class Player:
    id: str = None
    position: int = 0
    name: str = None
    color: str = None
    points: int = 0
    team: Optional[str] = None
    correctAnswers: List[int] = dataclasses.field(default_factory=list)
    speciality: Optional[str] = None

    def __hash__(self):
        return hash((self.name, self.id, self.position))

    def __eq__(self, value: Union[str, 'Player']):
        if isinstance(value, str):
            return any([
                self.name == value,
                self.id == value,
                str(self.position) == value
            ])

        return any([
            self.name == value.name,
            self.id == value.id,
            self.position == value.position
        ])


@dataclasses.dataclass
class GameSettings():
    """Encapsulates the game settings
    for the current bindtest. This is
    voluntary duplicate of the firebase
    structure from the frontend"""

    difficulty = 'All'
    genre = 'All'

    numberOfRounds = None

    pointValue: int = 1
    difficultyBonus = False
    timeBonus = False

    # fuzzy_matcher = FuzzyMatcher()

    connectionToken = None

    soloMode = False
    adminPlays = False
    timeLimit = None
    timeRange: List[int] = []

    multipleChoiceAnswers: bool = False
    numberOfChoices: int = 4
    currentChoiceAnswers: List[dict[str, Union[str, int]]] = []
    playerChoices: list[dict[str, Union[str, int]]] = []

    def config_from_dict(self, config: dict) -> list[str]:
        """Configures the game settings from a dictionary."""
        skipped_keys = []

        for key, value in config.items():
            if hasattr(self, key):
                setattr(self, key, value)
                continue
            skipped_keys.append(key)
        return skipped_keys


@dataclasses.dataclass
class GameState():
    """Initiates the game state for 
    the current blindtest"""

    is_started: bool = False
    current_round: int = 0
    current_song: Optional[dict[str, Union[str, int]]] = None
    played_songs: set[int] = dataclasses.field(default_factory=set)
    paused: bool = False

    _players: defaultdict[str, Player] = defaultdict(Player)
    playerCount: int = 0

    def increase_round(self) -> None:
        self.current_round += 1

    def add_played_song(self, song_id: int) -> None:
        self.played_songs.add(song_id)

    @property
    def players(self) -> list[Player]:
        """Returns a list of player dataclasses"""
        return list(self._players.values())

    @property
    def current_song_id(self) -> Optional[int]:
        """Returns the current song ID if available"""
        if self.current_song is not None:
            return self.current_song.get('id', None)
        return None

    @property
    def player_values(self) -> dict[str, dict[str, str | int]]:
        """Returns a dictionary representation of players"""
        return {key: dataclasses.asdict(player) for key, player in self._players.items()}

    def add_player(self, data: dict[str, DictAny]):
        """Adds a player to the current game settings"""
        player_id = data.get('id')
        if player_id is None:
            return False

        if player_id not in self._players:
            self.player_count += 1
            data['position'] = self.player_count
            player = Player(**data)
            self._players[player_id] = player
