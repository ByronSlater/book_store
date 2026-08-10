#!/bin/bash
set -e
export FLASK_DATABASE_URI="postgresql://postgres:password@book_store_db/book_store"
flask --app server init-db
flask --app server seed-db
flask --app server run -h 0.0.0.0 -p 5001
