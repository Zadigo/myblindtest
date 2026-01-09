import dataclasses
from collections import defaultdict
from typing import Annotated, List, Optional, Union

import pydantic
from songs.song_typings import DictAny, ListDictType

from blindtest.typings import DifficultyLevels


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

    pointLimit: int = None

    difficultyLevel: str = 'All'
    genreSelected: str = 'All'

    numberOfRounds: int = None

    pointValue: int = 1
    songDifficultyBonus: bool = False
    speedBonus: bool = False
    # fuzzy_matcher = FuzzyMatcher()

    connectionToken: str = None
    soloMode: bool = False
    adminPlays: bool = False
    timeLimit: int = None
    timeRange: List[int] = dataclasses.field(default_factory=list)

    multipleChoiceAnswers: bool = False
    numberOfChoices: int = 4

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

    player_count: int = 0
    _players: defaultdict[str, Player] = dataclasses.field(
        default_factory=lambda: defaultdict(Player))

    @property
    def is_active(self):
        """Returns whether the game is active and 
        is ready to play songs, receive answers, etc."""
        return all([self.is_started, not self.paused, self.current_song is not None])

    @property
    def player_names(self):
        return [player.name for player in self._players.values()]

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

    def reset(self):
        self.current_round = 0
        self.current_song = None
        self.played_songs.clear()
        self.paused = False
        self.player_count = 0
        self._players.clear()

    def has_player(self, player_id: str) -> bool:
        """Checks if a player ID exists in the current game state"""
        return player_id in self._players

    def add_player(self, data: dict[str, DictAny]) -> Player:
        """Adds a player to the current game settings"""
        player = Player(**data)
        self._players[player.id] = player
        self.player_count += 1
        return player

    def increase_round(self) -> None:
        self.current_round += 1

    def add_played_song(self, song_id: int) -> None:
        self.played_songs.add(song_id)

    def has_name(self, name: str):
        """Checks if a player name exists in the current game state"""
        return name in self.player_names

    def remove_player(self, player_id: str) -> bool:
        """Removes a player from the current game state"""
        if player_id in self._players:
            del self._players[player_id]
            self.player_count -= 1
            return True
        return False


@dataclasses.dataclass
class SongPossibilities():
    currentChoiceAnswers: ListDictType = dataclasses.field(
        default_factory=list)
    playerChoices: ListDictType = dataclasses.field(default_factory=list)


def validate_connection_token(token: str) -> bool:
    return True


class GameSettingsModel(pydantic.BaseModel):
    """Model representing game settings coming from Firebase
    and used to validate settings in the backend."""

    pointLimit: int = pydantic.Field(default=0, ge=0)

    difficultyLevel: str = pydantic.Field(default=DifficultyLevels.ALL.value)
    genreSelected: str = pydantic.Field(default='All')

    numberOfRounds: int = None

    pointValue: int = pydantic.Field(default=1, ge=1)
    songDifficultyBonus: bool = pydantic.Field(default=False)
    speedBonus: bool = pydantic.Field(default=False)

    connectionToken: Annotated[
        str,
        pydantic.AfterValidator(validate_connection_token)
    ] = None

    soloMode: bool = False
    adminPlays: bool = False
    timeLimit: int = None
    timeRange: list[int] = pydantic.Field(default_factory=list)

    multipleChoiceAnswers: bool = False
    numberOfChoices: int = pydantic.Field(default=4, ge=2, le=10)

    @pydantic.model_validator(mode='after')
    def check_time_range(self):
        return self


def validate_action(action: str) -> bool:
    """Function to validate if the action is valid."""
    from blindtest.typings import GAME_ACTIONS
    if action is None:
        return None

    if action not in GAME_ACTIONS:
        raise ValueError(f'Invalid action: {action}')

    return action


class ContentModel(pydantic.BaseModel):
    """Model for the content parameter in websocket consumers."""

    action: Annotated[str, pydantic.AfterValidator(validate_action)] = None
    team_or_player_id: Optional[str] = None
    title_match: Optional[bool] = False
    artist_match: Optional[bool] = False
    temporary_genre: Optional[str] = None
    settings: Optional[GameSettingsModel] = None
    player_id: Optional[str] = None
    session_id: Optional[str] = None
    device_name: Optional[str] = None
