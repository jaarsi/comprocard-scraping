#!/bin/sh -ex
git add .
git commit -m wip
branch=$(git symbolic-ref --short -q HEAD)
git push -u origin $branch
