import logging
import os
import pathlib

import dotenv
import httpx
from fastmcp import FastMCP
from fastmcp.client.logging import LogMessage

from models import AllSongs, SearchSongs, Song

BASE_DIR = pathlib.Path(__file__).parent.resolve()

dotenv.load_dotenv(BASE_DIR / '.env')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
LOGGING_LEVEL_MAP = logging.getLevelNamesMapping()


async def log_handler(message: LogMessage):
    """Forward MCP server logs to Python's logging system."""
    msg = message.data.get('msg')
    extra = message.data.get('extra')

    level = LOGGING_LEVEL_MAP.get(message.level.upper(), logging.INFO)
    logger.log(level, msg, extra=extra)

app = FastMCP(
    name="Blindtest Music MCP",
    version="1.0.0"
)


@app.tool(description="Get a list of songs")
async def get_songs() -> list[Song]:
    """Fetches a list of songs from the Django backend API.

    Args:
        None

    Returns:
        list[Song]: A list of Song objects retrieved from the API.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{os.getenv('DJANGO_URL')}/graphql/", data={
                'query': """
                    query {
                        allSongs {
                            id
                            name
                            artist {
                                id
                                name
                                spotifyId
                            }
                            year
                            genre
                            difficulty
                            createdOn
                            youtubeId
                        }
                    }
                """
            })
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Error fetching songs: {e}")
            return []
        else:
            data: GraphqlResponse = response.json()
            validated_data = AllSongs(allSongs=data['data']['allSongs'])
            return validated_data.allSongs


@app.tool(description="Get a single song")
async def get_song(name: str) -> Song | None:
    """Get a single song by its ID from the Django backend API.

    Args:
        None

    Returns:
        list[Song]: A list of Song objects retrieved from the API.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{os.getenv('DJANGO_URL')}/graphql/", data={
                'query': """
                    query {
                        allSongs {
                            id
                            name
                            artist {
                                id
                                name
                                spotifyId
                            }
                            year
                            genre
                            difficulty
                            createdOn
                            youtubeId
                        }
                    }
                """
            })
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"Error fetching songs: {e}")
            return None
        else:
            data: GraphqlResponse = response.json()
            validated_data = SearchSongs(searchSongs=data['data']['allSongs'])

            if len(validated_data.searchSongs) > 1:
                print(
                    f"Warning: Multiple songs found with name '{name}'. Returning the first match.")
                return validated_data.searchSongs[0]
            elif len(validated_data.searchSongs) == 0:
                print(f"No songs found with name '{name}'.")
                return None
            else:
                return validated_data.searchSongs[0]


@app.tool(description="Get a single artist")
async def get_artist():
    pass


@app.tool(description="Get a list of artists")
async def get_artists():
    pass


@app.tool(description="Get a list of genres")
async def get_genres():
    pass


@app.tool(description="Get artists by genres")
async def get_artists_by_genres():
    pass


if __name__ == "__main__":
    try:
        app.run()
    except KeyboardInterrupt:
        print("Shutting down MCP...")
