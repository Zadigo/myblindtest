# https://www.discogs.com/developers#page:database,header:database-search

# import requests

# # Enter your API Key
# API_KEY = ''

# url = "https://api.deepseek.com/chat/completions"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {API_KEY}"
# }

# data = {
#     # Use 'deepseek-reasoner' for R1 model or 'deepseek-chat' for V3 model
#     "model": "deepseek-chat",
#     "messages": [
#         {"role": "system", "content": "You are a professional assistant"},
#         {"role": "user", "content": "Who are you?"}
#     ],
#     "stream": False  # Disable streaming
# }

# response = requests.post(url, headers=headers, json=data)

# if response.status_code == 200:
#     result = response.json()
#     print(result['choices'][0]['message']['content'])
# else:
#     print("Request failed, error code:", response.json())


# import discogs_client

# d = discogs_client.Client(
#     'Blindtest',
#     user_token='VZIJxGDDvlKpOmKKjYWyTZbkaDyoLosMAbHlRdFV'
# )

# value = d.search(
#     'Complicated',
#     artist='Avril Lavigne',
#     release_title='Complicated',
#     type='release',
#     page=1,
#     per_page=1
# )
# print(list(value))

import re
import dataclasses
import unicodedata
from urllib.parse import unquote, urlencode, urljoin
import locale
import requests
from bs4 import BeautifulSoup
from bs4._typing import _QueryResults
from googlesearch import search
import datetime


class DataclassMixin:
    def as_dict(self):
        data = {}
        fields = dataclasses.fields(self)
        for field in fields:
            data[field.name] = getattr(self, field.name)
        return data


@dataclasses.dataclass
class Artist(DataclassMixin):
    name: str = None
    wikipedia_page: str = None

    def __post_init__(self):
        pass


@dataclasses.dataclass
class Release(DataclassMixin):
    name: str
    release_year: int
    wikipedia_page: str = None

    def __post_init__(self):
        clean_year = unicodedata.normalize("NFKD", self.release_year)
        self.release_year = int(clean_year.strip())

        if self.wikipedia_page is not None:
            self.wikipedia_page = unquote(self.wikipedia_page)


class Wikipedia:
    base_domain = 'https://fr.wikipedia.org/wiki'

    def __init__(self, artist_name: str):
        self.artist_name = artist_name
        self.artist = Artist()

    @staticmethod
    def release_iterator(base_domain: str, items: _QueryResults, release_type='Album'):
        for item in items:
            release_year, title = item.text.split(':', maxsplit=1)
            other_pages = item.find_all('a')

            new_release = Release(title, release_year)
            new_release.object_type = release_type

            if len(other_pages) > 1:
                wikipedia_page = other_pages[-1]
                path = wikipedia_page.attrs['href']

                album_wikipedia = urljoin(base_domain, path)
                new_release.wikipedia_page = album_wikipedia

            yield new_release

    def get_wikipedia_page(self):
        """Search for the Wikipedia page on Google"""
        results = search('Avril Lavigne Wikipedia', num_results=2)

        candidates = []
        for item in results:
            if not 'fr.wikipedia.org/wiki/' in item:
                continue
            candidates.append(item)
        self.artist.wikipedia_page = candidates[-0]
        return candidates

    def get_awards(self, html_content: BeautifulSoup):
        # with open('D:/mywebsites/myblindtest/test.html', mode='r', encoding='utf-8') as f:
        #     s = BeautifulSoup(f.read(), 'html.parser')

        title = html_content.find(
            'h3',
            attrs={'id': 'Récompenses'}
        )
        table = title.parent.find_next_sibling('table')
        items = table.find_all('li')
        for item in items:
            print(item.text)

    def request_page(self):
        """Searches for Wikipedia page on Google and
        then returns the correspoding HTML content of
        the page"""
        try:
            results = search(f'{self.artist_name} Wikipedia', num_results=2)
        except:
            return False
        else:
            if not results:
                return False

            candidates = []
            for item in results:
                if not self.base_domain in item:
                    continue
                candidates.append(item)

            url = candidates[-0]

        try:
            response = requests.get(url, headers={'user-agent': 'Google'})
        except:
            return False
        else:
            return response

    def parse_artist_page(self):
        response = self.request_page()
        if response and response.status_code == 200:
            # with open('D:/mywebsites/myblindtest/test.html', mode='r', encoding='utf-8') as f:
            # s = BeautifulSoup(f.read(), 'html.parser')

            s = BeautifulSoup(response.content, 'html.parser')
            title = s.find('h3', attrs={'id': 'Albums_studio'})
            album_list = title.parent.find_next('ul')
            album_items = album_list.find_all('li')
            albums = list(
                self.release_iterator(
                    self.base_domain,
                    album_items
                )
            )

            template = {
                'albums': [item.as_dict() for item in albums],
                'singles': []
            }

            title = s.find('h3', attrs={'id': 'Singles'})
            if title is not None:
                singles_list = title.parent.find_next('ul')
                singles_items = singles_list.find_all('li')
                singles = list(
                    self.release_iterator(
                        self.base_domain,
                        singles_items
                    )
                )
                template['singles'] = [item.as_dict() for item in singles]

            raw_text = s.find('body').get_text()
            text = ' '.join(filter(lambda x: x != '', raw_text.split('\n')))

            result = re.search(
                r'née? le (?P<birth>\d+ \w+ \d{4})\[?\d?\]?',
                text
            )

            if result:
                locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
                date_of_birth = result.groupdict()['birth']
                d = datetime.datetime.strptime(date_of_birth, '%d %B %Y')
                # city = result.groupdict()['city']
                # country = result.groupdict()['country']

                template['date_of_birth'] = d
                # template['city'] = city
                # template['country'] = country

            return template


w = Wikipedia('Mariah Carey')
print(w.parse_artist_page())
# print(w.parse_artist_page())
