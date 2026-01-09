import pydantic
from enum import Enum


class GameActions(Enum):
    START_GAME = 'start_game'
    NEXT_SONG = 'next_song'
    GAME_STARTED = 'game_started'
    NEXT_SONG_LOADED = 'next_song_loaded'
    STOP_GAME = 'stop_game'
    SUBMIT_GUESS = 'submit_guess'
    NOT_GUESSED = 'not_guessed'
    RANDOMIZE_GENRE = 'randomize_genre'
    GAME_SETTINGS = 'game_settings'
    PAUSE_GAME = 'pause_game'
    RECONNECT_PLAYER = 'reconnect_player'


class DifficultyLevels(Enum):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'
    ALL = 'All'


