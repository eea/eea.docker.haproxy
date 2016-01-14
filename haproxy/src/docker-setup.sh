#!/bin/bash

# haproxy directly configured within /etc/haproxy/haproxy.cfg
if test -e /etc/haproxy/haproxy.cfg; then
  exit 0
fi

cp /tmp/haproxy.cfg /etc/haproxy/haproxy.cfg

if [ ! -z "$BACKENDS" ]; then
  # Backend provided via $BACKENDS env
  python3 /configure.py env
else
  # Find backend within /etc/hosts
  python3 /configure.py hosts
  touch /etc/haproxy/hosts.backends
fi
