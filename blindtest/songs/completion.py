import datetime
import locale
import pathlib
import re
import ssl
import unicodedata

import certifi
import kagglehub
import nltk
import pandas
import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
from googlesearch import search
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from songs.models import Artist

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    ssl._create_default_https_context = ssl._create_unverified_context
    nltk.download('punkt')
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')


class Wikipedia:
    """Class that extracts information from
    an artist's Wikipedia page"""

    def __init__(self):
        en_contractions_path = pathlib.Path(
            kagglehub.dataset_download(
                'ishivinal/contractions'
            )
        )

        fr_contractions_path = pathlib.Path(
            kagglehub.dataset_download(
                'johnpendenque/french-abbreviations'
            )
        )

        self.fr_contractions_path = fr_contractions_path.joinpath(
            'abreviations.csv'
        )

        # Extra meta data that can be extracted from the page
        self.metadata = {
            'birthname': None,
            'genres': None,
            'date_of_birth': None
        }
        self.errors = []

    def get_general_information(self, soup: Tag):
        locale.setlocale(locale.LC_ALL, 'fr_FR')

        infobox = soup.find('div', attrs={'class': 'infobox_v3'})
        infos = infobox.find_all('tr')

        values: list[str] = [
            item.text.replace('\n', ' ').strip()
            for item in infos
        ]

        for value in values:
            if value.startswith('Nom de naissance'):
                content = value.replace('Nom de naissance', '')
                self.metadata['birthname'] = content.strip()

            if value.startswith('Genre musical'):
                content = value.replace('Genre musical', '')
                self.metadata['genres'] = content.split(',')

            if value.startswith('Naissance'):
                content = value.replace('Naissance', '')
                text = content.strip()
                result = re.match(r'^(\d+(?:er)?\s?\w+\s?\d{4})', text)
                if result:
                    string_date = result.group(1).replace('1er', '1')
                    self.metadata['date_of_birth'] = datetime.datetime.strptime(
                        string_date,
                        '%d %B %Y'
                    )

        # Reset the locale to the user
        # preferred one
        locale.setlocale(locale.LC_ALL, '')
        return values

    def get_date_or_birth(self, text: str | None):
        """Tries to return the date of birth from
        within the text"""
        if text is not None:
            result = re.search(r'naissance\s(\d+\s\w+\s\d+)', text)

            if result:
                date_of_birth = result.group(1)
                months = {
                    'janvier': 1,
                    'fevrier': 2,
                    'mars': 3,
                    'avril': 4,
                    'mai': 5,
                    'juin': 6,
                    'juillet': 7,
                    'aout': 8,
                    'septembre': 9,
                    'octobre': 10,
                    'novembre': 11,
                    'decembre': 12
                }

                day, month, year = date_of_birth.split(' ')
                month = months[month]

                date = f'{day} {month} {year}'
                return datetime.datetime.strptime(date, '%d %M %Y').date()
        return None

    def extract_text_from_page(self, artist: Artist):
        if not artist.wikipedia_page:
            # results = search(
            #     f'{artist.birthname or artist.name} Wikipedia',
            #     num_results=5
            # )

            # base_domain = 'wikipedia.org/wiki/'
            # candidates = list(filter(lambda x: base_domain in x, results))

            # if not candidates:
            #     return None

            # try:
            #     french_wikipedia = list(
            #         filter(
            #             lambda x: 'fr.wikipedia' in x,
            #             candidates
            #         )
            #     )[-1]

            #     english_wikipedia = list(
            #         filter(
            #             lambda x: 'en.wikipedia' in x,
            #             candidates
            #         )
            #     )[-1]
            # except:
            #     return None
            # else:
            #     artist.wikipedia_page = french_wikipedia
            #     artist.save()
            return None

        try:
            response = requests.get(artist.wikipedia_page, headers=HEADERS)
        except:
            return None
        else:
            if response.ok:
                soup = BeautifulSoup(response.content, 'html.parser')
                self.get_general_information(soup)

                body = soup.find('main', attrs={'id': 'content'})
                body_content = body.find('div', attrs={'id': 'bodyContent'})

                raw_text: str = body_content.text.lower()
                df = pandas.read_csv(self.fr_contractions_path, sep=';')

                for item in df.itertuples():
                    value = df.loc[item.Index, 'abbreviation']
                    fullform = df.loc[item.Index, 'meaning']
                    raw_text = re.sub(
                        r'\b' + value + r'\b',
                        fullform,
                        raw_text
                    )

                # Remove special formatting and markup
                # Remove references like (en), (d), etc.
                clean_text = re.sub(r'\([^)]*\)', '', raw_text)

                # Remove square brackets and their contents
                clean_text = re.sub(r'\[[^]]*\]', '', clean_text)

                # Handle unicode characters and accents
                clean_text = unicodedata.normalize('NFKD', clean_text)\
                    .encode('ASCII', 'ignore')\
                    .decode('utf-8')

                # Remove numbers and punctuation
                clean_text = re.sub(r'[^\w\s]', ' ', clean_text)

                # Remove extra whitespace, newlines, tabs
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()

                tokens = word_tokenize(clean_text, language='french')

                french_stop_words = set(stopwords.words('french'))
                english_stop_words = set(stopwords.words('english'))

                stop_words = french_stop_words.union(english_stop_words)
                tokens = [token for token in tokens if token not in stop_words]

                return ' '.join(tokens)
            return None


def nrj(artist: Artist):
    name = artist.name.lower().replace(' ', '-')
    url = f'https://www.nrj.fr/artistes/{name}/biographie'

    metadata = {
        'place_of_birth': None,
        'date_of_birth': None
    }

    try:
        response = requests.get(url, headers=HEADERS)
    except:
        return metadata
    else:

        if response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')
            header = soup.find('div', attrs={'class': 'headerArtist-content'})

            if header is not None:
                sections = []
                for item in header.find_all('p'):
                    sections.append(item.text.strip())

                sections = [re.sub('\n', ' ', section) for section in sections]

                clean_sections = []
                for text in sections:
                    tokens = text.split(' ')
                    clean_sections.append(
                        ' '.join(
                            filter(lambda x: x != '', tokens)
                        )
                    )

                place_of_birth = list(
                    filter(
                        lambda x: 'Pays de naissance' in x,
                        clean_sections
                    )
                )

                date_of_birth = list(
                    filter(
                        lambda x: 'Né(e) le' in x,
                        clean_sections
                    )
                )

                place_of_birth: str = place_of_birth[-1].split(':')[-1]

                if date_of_birth:
                    date_text = date_of_birth[-1].replace('Né(e) le :', '')
                    date_text = re.sub(r'\(.*\)', '', date_text)
                    date_of_birth = datetime.datetime.strptime(
                        date_text.strip(),
                        '%d/%m/%Y'
                    )
                    metadata['date_of_birth'] = date_of_birth.date()

                metadata['place_of_birth'] = place_of_birth.strip()
        return metadata
