#!/bin/bash

set -e

if ! test -e /etc/haproxy/haproxy.cfg; then
	cp /tmp/haproxy_default.cfg /etc/haproxy/haproxy.cfg
	if [ ! -z "$BACKENDS" ]; then
		python /configure.py env
	else
		python /configure.py hosts
		track_hosts &
	fi
fi

rsyslogd

haproxy -f /etc/haproxy/haproxy.cfg && exec tail -f /var/log/haproxy_1.log
