import datetime
import pathlib
import re
import unicodedata

import kagglehub
import nltk
import pandas
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from songs.models import Artist


class Wikipedia:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('punkt_tab')
        nltk.download('omw-1.4')

        en_contractions_path = pathlib.path(
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

        self.errors = []

    def get_date_or_birth(self, text: str | None):
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
            results = list(search(f'{artist.name} Wikipedia', num_results=2))

            base_domain = 'wikipedia.org/wiki/'
            candidates = list(filter(lambda x: base_domain in x, results))

            if not candidates:
                return None

            french_wikipedia = list(
                filter(
                    lambda x: 'fr.wikipedia' in x,
                    candidates
                )
            )[-1]

            english_wikipedia = list(
                filter(
                    lambda x: 'en.wikipedia' in x,
                    candidates
                )
            )[-1]

            artist.wikipedia_page = french_wikipedia
            artist.save()

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }

        try:
            response = requests.get(artist.wikipedia_page, headers=headers)
        except:
            return None
        else:
            if response.ok:
                soup = BeautifulSoup(response.content, 'html.parser')
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
