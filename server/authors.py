import os
import sys
from datetime import datetime
from urllib.parse import urljoin

import requests
from flask import (
    Blueprint,
    Response,
    render_template,
    request,
)

from server.database import get_db

bp = Blueprint('authors', __name__)


def setup_author(author):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ['WIKIMEDIA_ACCESS_TOKEN'],
        'User-Agent': 'MyBookStoreProject/0.1 (https://example.org; byron.slater3@googlemail.com) Python-Requests/2.31.0'
    }

    wiki_id = author['wikidata_id']

    BASE_URL = 'https://wikidata.org/w/rest.php/wikibase/v1/'
    resp = requests.get(
        url=urljoin(BASE_URL, f'entities/items/{wiki_id}/statements'),
        headers=headers,
    )

    ts = resp.json()['P569'][0]['value']['content']['time']
    dob = datetime.fromisoformat(ts[1:])

    if 'P648' in resp.json():
        ol_id = resp.json()['P648'][0]['value']['content']
    else:
        ol_id = None

    filename = resp.json()['P18'][0]['value']['content']

    IMAGE_URL = 'https://commons.wikimedia.org/w/rest.php/v1/'

    resp2 = requests.get(
        url=urljoin(IMAGE_URL, f'file/{filename}'),
        headers={
            'Accept': 'image/jpeg',
            **headers
        }
    )

    image_url = resp2.json()['original']['url']

    resp3 = requests.get(
        url=image_url,
        headers={
            'Accept': 'image/jpeg',
            **headers
        }
    )

    db = get_db()
    db.execute("""
        UPDATE authors
        SET picture = %s,
            dob = %s,
            openlibrary_id = %s
        WHERE id = %s;
        """,
        (
            resp3.content,
            dob,
            ol_id,
            author['id']
        )
    )
    db.commit()

    author['picture'] = resp3.content


@bp.route('/authors/new', methods=['GET', 'POST'])
def new_author():
    if request.method == 'GET':
        return render_template('authors/new.html')
    elif request.method == 'POST':
        db = get_db()
        db.execute("""
            INSERT INTO "authors" ("wikidata_id", "name")
            VALUES (%s, %s);
        """.strip(), (request.form['wikidata_id'], request.form['name']))
        db.commit()
        return {

        }


@bp.route('/authors/new/search', methods=['POST'])
def new_author_search():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ['WIKIMEDIA_ACCESS_TOKEN'],
        'User-Agent': 'MyBookStoreProject/0.1 (https://example.org; byron.slater3@googlemail.com) Python-Requests/2.31.0',
        'Accept': 'application/sparql-results+json'
    }

    BASE_URL = "https://query.wikidata.org/sparql"

    query = """
    SELECT DISTINCT ?item ?entityId ?itemLabel ?itemDescription (SAMPLE(?image) AS ?image) WHERE {{
        SERVICE wikibase:mwapi {{
            bd:serviceParam wikibase:endpoint "www.wikidata.org" ;
                            wikibase:api "EntitySearch" ;
                            mwapi:search "{}" ;
                            mwapi:language "en" .
            ?item wikibase:apiOutputItem mwapi:item .
        }}
        ?item wdt:P31 wd:Q5 ;
                wdt:P106/wdt:P279* wd:Q36180 .
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}

        # Extract clean Q-ID (e.g. Q34887)
        BIND(STRAFTER(STR(?item), "http://www.wikidata.org/entity/") AS ?entityId)

        OPTIONAL {{ ?item wdt:P18 ?image . }}
    }}

    GROUP BY ?item ?entityId ?itemLabel ?itemDescription
    """.format(request.form['stext'])

    response = requests.get(
        url=BASE_URL,
        params={'query': query, 'format': 'json'},
        headers=headers
    )

    data = response.json()['results']['bindings']

    db = get_db()
    already_saved = [row['wikidata_id'] for row in db.execute('SELECT wikidata_id FROM authors;').fetchall()]

    data = [elem for elem in data if elem['entityId']['value'] not in already_saved]


    return data


@bp.route('/authors/img/<int:id>')
def author_image(id: int):
    author = get_db().execute('SELECT * FROM authors WHERE id=%s;', (id,)).fetchone()

    if author['picture'] is not None:
        picture = author['picture']
    else:
        setup_author(author)
        picture = author['picture']

    return Response(picture, mimetype='image/jpeg', headers={
        'content-type': 'image/jpeg'
    })


def get_bio(author):
    if author['openlibrary_id'] is None:
        setup_author(author)

    if author['openlibrary_id'] is None:
        author['bio'] = f'{author["name"]} is/was an author.'
        return

    BASE_URL = 'https://openlibrary.org/authors/'

    resp = requests.get(url=urljoin(BASE_URL, f'{author['openlibrary_id']}.json'),
                        headers={
                            'User-Agent': 'MyBookStoreProject/0.1 (https://example.org; byron.slater3@googlemail.com) Python-Requests/2.31.0'}
    )

    if 'bio' in resp.json():
        bio = resp.json()['bio']
        if type(bio) is dict:
            bio = bio['value']
    else:
        bio = f'Couldn\'t get bio for {author["name"]}'

    author['bio'] = bio


@bp.route('/authors/<int:id>')
def author(id: int):
    db = get_db()
    author = db.execute('SELECT * FROM authors WHERE id = %s;', (id,)).fetchone()

    if author['bio'] is None:
        get_bio(author)

    import bleach
    bio_lines = [bleach.linkify(line) for line in author['bio'].split('\n')]
    books = db.execute('SELECT * FROM books WHERE author_id = %s', (id,)).fetchall()
    return render_template('authors/author.html', author=author, bio=bio_lines, books=books)


@bp.route('/authors', methods=['GET', 'POST'])
def authors():
    if request.method == 'GET':
        authors = get_db().execute('SELECT * FROM authors ORDER BY name;').fetchall()

        return render_template('authors/authors.html', authors=authors)
    elif request.method == 'POST':
        print(request.get_data())
