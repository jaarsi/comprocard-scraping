#!/bin/sh -ex
git add .
git commit -m $1
branch=$(git symbolic-ref --short -q HEAD)
git push -u origin $branch
