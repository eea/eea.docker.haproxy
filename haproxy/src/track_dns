#!/bin/bash

IPS_1=`cat /etc/haproxy/dns.backends`
python3 /configure.py dns
IPS_2=`cat /etc/haproxy/dns.backends`

if [ "$IPS_1" != "$IPS_2" ]; then
  echo "DNS backends changed: $IPS_2"
  reload
fi
