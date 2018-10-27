#!/bin/sh

INTERVAL_SECONDS=${INTERVAL_SECONDS:-10}

while :
do
  pipenv run python main.py
  sleep $INTERVAL_SECONDS
done
