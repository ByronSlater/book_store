#!/bin/bash
set -e
flask --app server init-db
flask --app server seed-db
flask --app server run -h 0.0.0.0 -p 5001
