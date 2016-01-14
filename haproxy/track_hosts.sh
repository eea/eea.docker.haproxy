#!/bin/bash

while inotifywait -e close_write /etc/hosts 1>/dev/null 2>/dev/null; do
	sed -i "/.*server http-server.*/d" /etc/haproxy/haproxy.cfg
	python /configure.py update
	reload
done