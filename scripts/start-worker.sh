#!/bin/sh -ex
PYTHONPATH=src rq worker --max-jobs 24
