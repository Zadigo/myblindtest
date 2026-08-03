import pytest

from songs.logic.base_models import GameSettingsModel


@pytest.fixture
def settings():
    return {
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


def test_game_settings_model_valid(settings):
    GameSettingsModel(**settings)


def test_game_settings_model_invalid(settings):
    settings['difficultyLevel'] = 'Invalid'
    with pytest.raises(ValueError):
        GameSettingsModel(**settings)
