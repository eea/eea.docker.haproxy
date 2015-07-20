#!/bin/bash

set -e

if ! test -e /etc/haproxy/haproxy.cfg; then
	cp /tmp/haproxy_default.cfg /etc/haproxy/haproxy.cfg
	python /configure.py
fi

rsyslogd

haproxy -f /etc/haproxy/haproxy.cfg && tail -f /var/log/haproxy_1.log
