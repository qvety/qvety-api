#!/bin/sh
files=$(git status -s | grep -E '\.py$' | cut -c 4-)
echo "\033[1;35mflake8 is processing files"
flake8 $files
echo "\033[1;35misort is processing files"
isort $files
