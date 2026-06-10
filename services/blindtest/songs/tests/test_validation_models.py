import unittest
from songs.logic.base_models import GameSettingsModel


class TestValidationModels(unittest.TestCase):
    def test_game_settings_model_valid(self):
        data = {
            "difficultyLevel": "All",
            "genreSelected": "All",
            "numberOfChoices": 4,
            "pointValue": 1,
            "songDifficultyBonus": False,
            "soloMode": False,
            "adminPlays": False,
            "timeLimit": None,
            "timeRange": [],
            "multipleChoiceAnswers": False
        }
        # If the data is valid, this should not
        # raise an exception
        GameSettingsModel(**data)

    # def test_game_settings_model_invalid(self):
    #     with self.assertRaises(ValueError):
    #         GameSettingsModel(
    #             difficultyLevel="Invalid",
    #             genreSelected="All",
    #             numberOfChoices=4,
    #             pointValue=1,
    #             songDifficultyBonus=False,
    #             soloMode=False,
    #             adminPlays=False,
    #             timeLimit=None,
    #             timeRange=[],
    #             multipleChoiceAnswers=False
    #         )
