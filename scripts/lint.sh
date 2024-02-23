#!/bin/sh -ex
isort --profile black src scripts
black src scripts
ruff src scripts
