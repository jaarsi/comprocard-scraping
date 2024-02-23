#!/bin/sh -ex
isort --profile black $1
black $1
ruff $1
