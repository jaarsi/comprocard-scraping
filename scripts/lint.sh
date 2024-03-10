#!/bin/sh -ex
isort --profile black src scripts
black src scripts --line-length 100
ruff src scripts
