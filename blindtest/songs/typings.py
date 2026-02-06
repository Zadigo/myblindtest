from typing import Optional, Union, TYPE_CHECKING


if TYPE_CHECKING:
    from songs.logic.base import Player


type SongDictType = Optional[dict[str, Union[str, int]]]

type PlayerType = 'Player'

type PlayersDictType = dict[str, PlayerType]
