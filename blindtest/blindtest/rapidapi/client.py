import os
from typing import Union

from requests import Request, Session


class BaseApi:
    url: str = None
    host: str = None
    errors = []

    def __init__(self):
        self.query = {}
        self.response_data = {}

    def __repr__(self):
        return f'<{self.__class__.__name__}({self.url})>'

    def __getitem__(self, key) -> str:
        return self.response_data[key]

    def clean(self, data) -> dict[str, Union[str, int, dict, list]]:
        return data

    def build_headers(self, **headers):
        base_headers = {'content-type': 'application/json'} | headers
        base_headers.update({'x-rapidapi-key': os.getenv('RAPID_API_KEY')})
        base_headers['x-rapidapi-host'] = self.host
        return base_headers

    def build_query(self, **query):
        self.query | query

    def build_request(self, headers={}, request_params={}):
        session = Session()
        headers = self.build_headers(**headers)

        if self.url is None:
            raise ValueError('Cannot use endpoint with empty url')

        self.build_query()
        request = Request(
            method='get',
            url=self.url,
            headers=headers,
            params=self.query,
            **request_params
        )

        prepared_request = session.prepare_request(request)
        return session, prepared_request

    def send(self, headers={}, request_params={}):
        session, request = self.build_request(
            headers=headers,
            request_params=request_params
        )

        try:
            response = session.send(request)
        except Exception as e:
            self.errors.append(e.args)
        else:
            if response.ok:
                self.response_data = self.clean(response.json())
            else:
                self.errors.append(response.json())


class Spotify(BaseApi):
    """Spotify API client using RapidAPI service to fetch data
    about artists, albums, tracks, playlists, podcasts, episodes,
    genres and users."""

    url = 'https://spotify23.p.rapidapi.com/search/'
    host = 'spotify23.p.rapidapi.com'

    def __init__(self, search, search_type='artists'):
        super().__init__()
        self.search_type = search_type
        self.build_query(q=search, type=search_type)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, key):
        return self.items[key]

    def __len__(self):
        return len(self.items)

    @property
    def items(self) -> list[dict[str, Union[str, dict, int]]]:
        return self.response_data[self.search_type]['items']

    def build_query(self, **query):
        if 'type' in query:
            value = query.get('type')
            accepted_types = [
                'albums',
                'artists',
                'episodes',
                'genres',
                'playlists',
                'podcasts',
                'tracks',
                'users'
            ]
            if value not in accepted_types:
                raise ValueError('Search type is not valid')

        self.query.update({
            'offset': '0',
            'limit': '2',
            'numberOfTopResults': '5',
            **query
        })
