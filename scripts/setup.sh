#!/bin/sh -ex
poetry lock
poetry install --no-root --with dev
poetry run pre-commit install
