#!/bin/bash



# haproxy directly configured within /etc/haproxy/haproxy.cfg
if test -e /etc/haproxy/haproxy.cfg; then
  exit 0
fi

if [ ! -z "$DNS_ENABLED" ]; then
  # Backends are resolved using internal or external DNS service
  touch /etc/haproxy/dns.backends
  python3 /configure.py dns
  echo "*/${DNS_TTL:-1} * * * * /track_dns  >/proc/1/fd/1 2>/proc/1/fd/2" > /var/crontab.txt

else

  if [ ! -z "$BACKENDS" ]; then
    # Backend provided via $BACKENDS env
    python3 /configure.py env
  else
    # Find backend within /etc/hosts
    touch /etc/haproxy/hosts.backends
    python3 /configure.py hosts
  fi

  echo "*/${DNS_TTL:-1} * * * * /track_hosts  >/proc/1/fd/1 2>/proc/1/fd/2" > /var/crontab.txt

fi

#enable cron logging
service rsyslog restart

#add crontab 
crontab /var/crontab.txt 
chmod 600 /etc/crontab
service cron restart



echo "export PATH=$PATH"':$PATH' >> /etc/environment

#Add env variables for haproxy
echo "export BACKENDS=$BACKENDS"  >> /etc/environment
echo "export BACKENDS_PORT=$BACKENDS_PORT"  >> /etc/environment
echo "export BACKEND_NAME=$BACKEND_NAME"  >> /etc/environment
echo "export BALANCE=$BALANCE"  >> /etc/environment
echo "export COOKIES_ENABLED=$COOKIES_ENABLED"  >> /etc/environment
echo "export DOWN_INTER=$DOWN_INTER"  >> /etc/environment
echo "export FALL=$FALL"  >> /etc/environment
echo "export FAST_INTER=$FAST_INTER"  >> /etc/environment
echo "export FRONTEND_NAME=$FRONTEND_NAME"  >> /etc/environment
echo "export FRONTEND_PORT=$FRONTEND_PORT"  >> /etc/environment
echo "export HTTPCHK=\"$HTTPCHK\""  >> /etc/environment
echo "export INTER=$INTER"  >> /etc/environment
echo "export LOGGING=$LOGGING"  >> /etc/environment
echo "export PROXY_PROTOCOL_ENABLED=$PROXY_PROTOCOL_ENABLED"  >> /etc/environment
echo "export RISE=$RISE"  >> /etc/environment
echo "export SERVICE_NAMES=$SERVICE_NAMES"  >> /etc/environment
echo "export STATS_AUTH=$STATS_AUTH"  >> /etc/environment
echo "export STATS_PORT=$STATS_PORT"  >> /etc/environment
echo "export TIMEOUT_CLIENT=$TIMEOUT_CLIENT"  >> /etc/environment
echo "export TIMEOUT_CONNECT=$TIMEOUT_CONNECT"  >> /etc/environment
echo "export TIMEOUT_SERVER=$TIMEOUT_SERVER"  >> /etc/environment

gosu haproxy $(which haproxy-systemd-wrapper) -p /etc/haproxy/haproxy.pid  -f /etc/haproxy/haproxy.cfg

