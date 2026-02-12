from mcp_server import MCPToolset, ModelQueryToolset
from tvshows.models import ThemeSong, TVShow


class TVShowQueryTool(ModelQueryToolset):
    model = TVShow
    search_fields = [
        'title',
        'title_fr',
        'imdb_id'
    ]


class ThemeSongQueryTool(ModelQueryToolset):
    model = ThemeSong
    search_fields = [
        'series__name',
        'name',
        'artist__name'
    ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('series', 'artist').all()


class TVShowTools(MCPToolset):
    def create_tv_show(self, title: str, title_fr: str = None, imdb_id: str = None, image_url: str = None) -> TVShow:
        """Create a new TV show with the given title and optional details.

        Args:
            title (str): The title of the TV show.
            title_fr (str, optional): The French title of the TV show. Defaults to None.
            imdb_id (str, optional): The IMDB identifier for the TV show. Defaults to None.
            image_url (str, optional): URL to an image representing the TV show. Defaults to None.

        Returns:
            TVShow: The created TV show instance.
        """
        tv_show = TVShow.objects.create(
            title=title,
            title_fr=title_fr,
            imdb_id=imdb_id,
            image_url=image_url
        )
        return tv_show

    def update_tv_show(self, title: str, title_fr: str = None, imdb_id: str = None, image_url: str = None) -> TVShow:
        """Update an existing TV show with the given title and optional details.

        Args:
            title (str): The title of the TV show to update.
            title_fr (str, optional): The new French title of the TV show. Defaults to None.
            imdb_id (str, optional): The new IMDB identifier for the TV show. Defaults to None.
            image_url (str, optional): The new URL to an image representing the TV show. Defaults to None.

        Returns:
            TVShow: The updated TV show instance.
        """
        try:
            tv_show = TVShow.objects.get(title=title)
        except TVShow.DoesNotExist:
            raise ValueError(f"TV show with title '{title}' does not exist.")
        else:
            if title_fr is not None:
                tv_show.title_fr = title_fr

            if imdb_id is not None:
                tv_show.imdb_id = imdb_id
            
            if image_url is not None:
                tv_show.image_url = image_url
            
            tv_show.save()
            return tv_show
