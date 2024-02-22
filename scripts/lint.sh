#!/bin/sh -ex
poetry run isort --profile black src scripts
poetry run black src scripts
poetry run ruff src scripts
