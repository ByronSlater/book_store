from server.authors import setup_author
from server.database import get_db
from server import create_app, database

app = create_app()
app.app_context().push()


db = database.get_db()

authors = db.execute('SELECT * FROM authors;')

for author in authors:
    try:
        setup_author(author['id'], author['name'])
    except Exception:
        pass
