#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run pyton -m aircraft_manufacturing_app.manage'

echo 'Collectiong static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

exec poetry run core -p 8000 -b 0.0.0.0