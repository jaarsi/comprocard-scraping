#!/bin/sh -ex
poetry lock
poetry install --no-root
poetry run pre-commit install
