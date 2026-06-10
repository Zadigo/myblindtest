from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from youtube_search.query import Query, QueryList
    from youtube_search.base import BaseSearch
    from youtube_search.models.videos import VideoModel, ThumbnailModel
    from youtube_search.models.channels import ChannelModel
    from youtube_search.models.videos import VideoModel, ThumbnailModel

type TypeVideoModel = VideoModel

type TypeBaseSearch = BaseSearch

type TypeQuery = Query
