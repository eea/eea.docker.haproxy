#!/bin/bash

if [ -f /etc/haproxy/hosts.backends ]; then
  python3 /configure.py hosts
fi

haproxy -f /etc/haproxy/haproxy.cfg -p /etc/haproxy/haproxy.pid -st $(</etc/haproxy/haproxy.pid)
