#!/bin/bash
set -e

if [ "$1" == "-change" ]; then
    black_args="--skip-string-normalization"
    isort_args="--profile black"
else
    black_args="--check --diff --skip-string-normalization"
    isort_args="--check-only --diff --profile black"
fi

flake8_args="--exclude=migrations,__init__.py,apps.py,media,static --config pyproject.toml"

echo "Black checking"
black $black_args .

echo "isort checking"
isort $isort_args . --skip migrations --skip media --skip logs --skip venv --skip .venv

echo "flake8 checking"
flake8 $flake8_args src
