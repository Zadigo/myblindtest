import dataclasses
from typing import List


@dataclasses.dataclass
class GameSettings():
    """Encapsulates the game settings
    for the current bindtest. This is
    voluntary duplicate of the firebase
    structure from the frontend

    Attributes:
        pointLimit (int): The point limit for the game. If None, there is no limit.
        difficultyLevel (str): The difficulty level for the game. Can be 'Easy', 'Medium', 'Hard' or 'All'.
        genreSelected (str): The genre selected for the game. Can be 'All' or any of the genres in the database.
        numberOfRounds (int): The number of rounds for the game. If None, there is no limit.
        pointValue (int): The base point value for each correct answer.
        songDifficultyBonus (bool): Use the song difficulty as a multiplier for points
        speedBonus (bool): Use the speed of the song as a multiplier for points
        connectionToken (str): The connection token for the game.
        soloMode (bool): Whether the game is in solo mode.
        adminPlays (bool): Whether the admin can play.
        timeLimit (int): The time limit for each round. If None, there is no limit.
        timeRange (List[int]): The range of time for each round. If empty, there is no limit.
        multipleChoiceAnswers (bool): Whether the game uses multiple choice answers.
        numberOfChoices (int): The number of choices for multiple choice answers.
    """

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
