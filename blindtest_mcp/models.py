from typing import Optional
import pydantic


class Artist(pydantic.BaseModel):
    id: str
    name: str
    genre: Optional[str] = pydantic.Field(default=None)
    isGroup: Optional[bool] = pydantic.Field(default=None)
    # birthname: Optional[str] = pydantic.Field(default=None)
    # dateOfBirth: Optional[str] = pydantic.Field(default=None)
    # dateOfDeath: Optional[str] = pydantic.Field(default=None)
    # spotifyAvatar: Optional[str] = pydantic.Field(default=None)
    # spotifyId: Optional[str] = pydantic.Field(default=None)
    # wikipediaPage: Optional[str] = pydantic.Field(default=None)
    # createdOn: Optional[str] = pydantic.Field(default=None)
    # spotifyId: Optional[str] = pydantic.Field(default=None)
    # songSet: Optional[dict] = pydantic.Field(default=None)


class Song(pydantic.BaseModel):
    id: str | int
    name: str
    artist: Artist
    year: int
    genre: str
    difficulty: int
    youtubeId: str
    createdOn: str


class AllSongs(pydantic.BaseModel):
    allSongs: list[Song]


class AllArtists(pydantic.BaseModel):
    allArtists: list[Artist]


class SearchSongs(pydantic.BaseModel):
    searchSongs: list[Song]
