#!/bin/bash
if [ $# -eq 0 ]
  then
    echo "Port not suppled"
    exit 1
fi
PORT=$1
echo "stopping gunicorn on port $PORT"
PIDS=`ps ax | grep gunicorn | grep $PORT | awk '{split($0,a," "); print a[1]}'`
if [ -z "$PIDS" ]; then
  echo "no gunicorn deamon on port ${PORT}"
else
  echo "killed gunicorn ($PIDS) deamon on port $1"
  xargs kill <<< "$PIDS"
fi