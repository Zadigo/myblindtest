from blindtest.rapidapi.client import BaseApi


class IMDB(BaseApi):
    """IMDB API client using RapidAPI service to fetch TV show data"""
    
    url = 'https://imdb232.p.rapidapi.com/api/search'
    host = 'imdb232.p.rapidapi.com'

    def __init__(self, title: str, search_type: str = 'TV'):
        self.query = {'q': title, 'limit': 1, 'type': search_type }

    def build_query(self, **query):
        search_type = query.get('type')
        accepted_types = ['MOVIE', 'NAME', 'TV', 'TV_EPISODE', 'INTEREST', 'VIDEO_GAME', 'PODCAST_SERIES']

        if search_type is not None and search_type in accepted_types:
            search_type = 'MOVIE'

        self.query.update(query)

    def clean(self, data):
        data = super().clean(data)

        cleaned_data = data['data']['mainSearch']['edges']
        items = cleaned_data[-1]

        if items:
            item = items['node']['entity']

            release_year = item.get('releaseYear')
            release_date = item.get('releaseDate')
            image_url = item.get('primaryImage')

            if release_date is not None:
                release_date = f'{release_date["day"]}-{release_date["month"]}-{release_date["year"]}'

            return {
                'id': item.get('id'),
                'name': item['titleText']['text'],
                'release_year': {
                    'start': release_year['year'],
                    'end': release_year.get('endYear')
                },
                'release_date': release_date,
                'image': image_url.get('url', None)
            }
