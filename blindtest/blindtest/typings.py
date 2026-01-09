from enum import Enum

type TypeContent = dict[str, str | int | bool | list | dict]


class GameActions(Enum):
    """Game actions used in the backend to communicate
    between consumers and the frontend."""

    DEVICE_ACCEPTED = 'device_accepted'
    DEVICE_DISCONNECTED = 'device_disconnected'
    GAME_COMPLETE = 'game_complete'
    GAME_SETTINGS = 'game_settings'
    GAME_STARTED = 'game_started'
    GUESS_CORRECT = 'guess_correct'
    GUESS_INCORRECT = 'guess_incorrect'
    IDLE_RESPONSE = 'idle_response'
    MULTI_CHOICE_UPDATED_SCORES = 'multi_choice_updated_scores'
    NEXT_SONG = 'next_song'
    NEXT_SONG_LOADED = 'next_song_loaded'
    NOT_GUESSED = 'not_guessed'
    PAUSE_GAME = 'pause_game'
    PLAYER_SUBMITTED_ANSWER = 'player_submitted_answer'
    RANDOMIZE_GENRE = 'randomize_genre'
    RECONNECT_PLAYER = 'reconnect_player'
    SONG_NEW = 'song_new'
    START_GAME = 'start_game'
    STOP_GAME = 'stop_game'
    SUBMIT_GUESS = 'submit_guess'
    UPDATE_POSSIBILITIES = 'update_possibilities'


GAME_ACTIONS = [action.value for action in GameActions]


class ChannelActions(Enum):
    """Channel actions used in the backend to communicate
    between different consumers."""

    GAME_STARTED = 'game.started'
    GAME_UPDATES = 'game.updates'
    GAME_STOPPED = 'game.stopped'
    GAME_DISCONNECTED = 'game.disconnected'
    TRY_RECONNECTION = 'try.reconnection'


class DifficultyLevels(Enum):
    """Game difficulty levels."""

    EASY = 'Easy'
    MEDIUM = 'Medium'
    SEMI_PRO = 'Semi-Pro'
    DIFFICULT = 'Difficult'
    EXPERT = 'Expert'
    ALL = 'All'


DIFFICULTY_LEVELS = [level.value for level in DifficultyLevels]
