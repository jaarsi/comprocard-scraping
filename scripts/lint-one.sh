#!/bin/sh -ex
poetry run isort --profile black $1
poetry run black $1
poetry run ruff $1