from typing import Any

from django.conf import settings
import httpx
import time
from django.core.cache import cache


class Spotify:
    """Class to handle Spotify API interactions, including authentication and requests."""

    request_url: str = 'https://api.spotify.com/v1/'
    query: dict[str, Any] = {}

    @property
    def access_token(self):
        credentials = cache.get('spotify_credentials')

        if credentials is None:
            self.get_access_token()
            credentials = cache.get('spotify_credentials')

        return credentials['access_token']

    @staticmethod
    def get_access_token(force_refresh: bool = False):
        credentials = cache.get('spotify_credentials')

        if credentials is None or force_refresh:
            with httpx.Client() as client:
                try:
                    response = client.post(
                        'https://accounts.spotify.com/api/token',
                        headers={
                            'Content-Type': 'application/x-www-form-urlencoded'},
                        data={
                            'grant_type': 'client_credentials',
                            'client_id': settings.SPOTIFY_CLIENT_ID,
                            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
                        }
                    )
                    response.raise_for_status()
                except httpx.HTTPError as e:
                    raise Exception(
                        f"Failed to obtain Spotify access token: {e}")
                else:
                    credentials = response.json()
                    cache.set(
                        'spotify_credentials',
                        credentials,
                        timeout=credentials['expires_in'] - 60
                    )
                    time.sleep(3)

    def send(self, path: str):
        if path.startswith('/'):
            path = path[1:]

        with httpx.Client() as client:
            try:
                response = client.get(
                    f"{self.request_url}{path}",
                    params=self.query,
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                response.raise_for_status()
            except httpx.HTTPError as e:
                # if response.status_code == 401:
                #     self.get_access_token(force_refresh=True)
                #     return False
                raise Exception(f"Spotify API request failed: {e}")
            else:
                return response.json()


class ListPlaylists(Spotify):
    """Class to list Spotify playlists for a given user."""

    query = {'limit': 20, 'offset': 0}

    def send(self, **kwargs: str):
        return super().send('/me/playlists')


class GetPlaylist(Spotify):
    """Class to get details of a specific Spotify playlist."""

    query = {
        'fields': 'id,name,tracks.items(added_at, track(id,name,explicit,type,href,artists(name,spotify)))'
    }

    def send(self, playlist_id: str):
        data = cache.get('spotify_playlist_' + playlist_id)
        if data is None:
            data = super().send(f'/playlists/{playlist_id}')
            cache.set('spotify_playlist_' + playlist_id, data,
                      timeout=(60 * 60))  # Cache for 1 hour
        return data
