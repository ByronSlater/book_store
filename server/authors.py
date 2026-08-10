import os
from datetime import datetime
from urllib.parse import urljoin
import sys

import requests
from flask import (
    Blueprint,
    Response,
    render_template,
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

    print('WHAT IS GOING ON HERE', file=sys.stderr)
    print(resp.json(), file=sys.stderr)
    print(os.environ['WIKIMEDIA_ACCESS_TOKEN'], file=sys.stderr)
    print(resp.request.url, sys.stderr)
    print(resp.request.headers, file=sys.stderr)

    print(resp.json()['P569'][0]['value']['content']['time'])
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

@bp.route('/authors')
def authors():
    authors = get_db().execute('SELECT * FROM authors ORDER BY name;').fetchall()

    return render_template('authors/authors.html', authors=authors)
