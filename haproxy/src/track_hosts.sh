#!/bin/bash

while inotifywait -e close_write /etc/hosts; do
  sleep 1
  reload
done
