#!/bin/bash

if [ -f /etc/haproxy/hosts.backends ]; then
  cp /tmp/haproxy.cfg /etc/haproxy/haproxy.cfg
  python3 /configure.py hosts
fi

haproxy -f /etc/haproxy/haproxy.cfg -p /etc/haproxy/haproxy.pid -st $(</etc/haproxy/haproxy.pid)
