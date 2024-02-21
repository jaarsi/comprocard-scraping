#!/bin/sh -ex
poetry run isort --profile black src
poetry run black src
poetry run ruff src
