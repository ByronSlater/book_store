import click
import psycopg
from flask import current_app, g
from psycopg.rows import dict_row


def get_db():
    if 'db' not in g:
        g.db = psycopg.connect(
            current_app.config['DATABASE_URI'],
            row_factory=dict_row
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.execute(f.read())
        db.commit()

def seed_db():
    db = get_db()

    with current_app.open_resource("seeds.sql") as f:
        db.execute(f.read())
        db.commit()

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialised db')


@click.command('seed-db')
def seed_db_command():
    seed_db()
    click.echo('seeded database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
