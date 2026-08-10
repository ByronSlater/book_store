from flask.cli import load_dotenv
import requests
import os
from urllib.parse import urljoin

load_dotenv('.flaskenv')

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + os.environ['WIKIMEDIA_ACCESS_TOKEN'],
    'User-Agent': 'MyBookStoreProject/0.1 (https://example.org; byron.slater3@googlemail.com) Python-Requests/2.31.0'
}

wiki_id = 'Q134798'
BASE_URL = 'https://wikidata.org/w/rest.php/wikibase/v1/'

resp = requests.get(
    url=BASE_URL+f'entities/items/{wiki_id}/statements',
    headers=headers,
)
