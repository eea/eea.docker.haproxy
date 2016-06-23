#!/bin/bash

# haproxy directly configured within /etc/haproxy/haproxy.cfg
if test -e /etc/haproxy/haproxy.cfg; then
  exit 0
fi

if [ ! -z "$DNS_ENABLED" ]; then
  # Backends are resolved using internal or external DNS service
  python3 /configure.py dns
  touch /etc/haproxy/dns.backends
  exit $?
fi

if [ ! -z "$BACKENDS" ]; then
  # Backend provided via $BACKENDS env
  python3 /configure.py env
else
  # Find backend within /etc/hosts
  python3 /configure.py hosts
  touch /etc/haproxy/hosts.backends
fi
