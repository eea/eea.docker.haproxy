#!/bin/bash



# haproxy directly configured within /etc/haproxy/haproxy.cfg
if test -e /etc/haproxy/haproxy.cfg; then
  exit 0
fi

if [ ! -z "$DNS_ENABLED" ]; then
  # Backends are resolved using internal or external DNS service
  touch /etc/haproxy/dns.backends
  python3 /configure.py dns
  echo "*/${DNS_TTL:-1} * * * * /track_dns  | logger " > /var/crontab.txt

else

  if [ ! -z "$BACKENDS" ]; then
    # Backend provided via $BACKENDS env
    python3 /configure.py env
  else
    # Find backend within /etc/hosts
    touch /etc/haproxy/hosts.backends
    python3 /configure.py hosts
  fi

  echo "*/${DNS_TTL:-1} * * * * /track_hosts  | logger " > /var/crontab.txt

fi

#enable cron logging
service rsyslog restart

#add crontab
crontab /var/crontab.txt
chmod 600 /etc/crontab
service cron restart


#Add env variables for haproxy
echo "export PATH=$PATH"':$PATH' >> /etc/environment
if [ ! -z "$BACKENDS" ]; then echo "export BACKENDS=\"$BACKENDS\""  >> /etc/environment; fi
if [ ! -z "$BACKENDS_PORT" ]; then echo "export BACKENDS_PORT=\"$BACKENDS_PORT\""  >> /etc/environment; fi
if [ ! -z "$BACKENDS_MODE" ]; then echo "export BACKENDS_MODE=\"$BACKENDS_MODE\""  >> /etc/environment; fi
if [ ! -z "$BACKEND_NAME" ]; then echo "export BACKEND_NAME=\"$BACKEND_NAME\""  >> /etc/environment; fi
if [ ! -z "$BALANCE" ]; then echo "export BALANCE=\"$BALANCE\""  >> /etc/environment; fi
if [ ! -z "$COOKIES_ENABLED" ]; then echo "export COOKIES_ENABLED=\"$COOKIES_ENABLED\""  >> /etc/environment; fi
if [ ! -z "$DOWN_INTER" ]; then echo "export DOWN_INTER=\"$DOWN_INTER\""  >> /etc/environment; fi
if [ ! -z "$FALL" ]; then echo "export FALL=\"$FALL\""  >> /etc/environment; fi
if [ ! -z "$FAST_INTER" ]; then echo "export FAST_INTER=\"$FAST_INTER\""  >> /etc/environment; fi
if [ ! -z "$FRONTEND_NAME" ]; then echo "export FRONTEND_NAME=\"$FRONTEND_NAME\""  >> /etc/environment; fi
if [ ! -z "$FRONTEND_PORT" ]; then echo "export FRONTEND_PORT=\"$FRONTEND_PORT\""  >> /etc/environment; fi
if [ ! -z "$FRONTEND_MODE" ]; then echo "export FRONTEND_MODE=\"$FRONTEND_MODE\""  >> /etc/environment; fi
if [ ! -z "$HTTPCHK" ]; then echo "export HTTPCHK=\"$HTTPCHK\""  >> /etc/environment; fi
if [ ! -z "$INTER" ]; then echo "export INTER=\"$INTER\""  >> /etc/environment; fi
if [ ! -z "$LOGGING" ]; then echo "export LOGGING=\"$LOGGING\""  >> /etc/environment; fi
if [ ! -z "$LOG_LEVEL" ]; then echo "export LOG_LEVEL=\"$LOG_LEVEL\""  >> /etc/environment; fi
if [ ! -z "$PROXY_PROTOCOL_ENABLED" ]; then echo "export PROXY_PROTOCOL_ENABLED=\"$PROXY_PROTOCOL_ENABLED\""  >> /etc/environment; fi
if [ ! -z "$RISE" ]; then echo "export RISE=\"$RISE\""  >> /etc/environment; fi
if [ ! -z "$SERVICE_NAMES" ]; then echo "export SERVICE_NAMES=\"$SERVICE_NAMES\""  >> /etc/environment; fi
if [ ! -z "$STATS_AUTH" ]; then echo "export STATS_AUTH=\"$STATS_AUTH\""  >> /etc/environment; fi
if [ ! -z "$STATS_PORT" ]; then echo "export STATS_PORT=\"$STATS_PORT\""  >> /etc/environment; fi
if [ ! -z "$TIMEOUT_CLIENT" ]; then echo "export TIMEOUT_CLIENT=\"$TIMEOUT_CLIENT\""  >> /etc/environment; fi
if [ ! -z "$TIMEOUT_CONNECT" ]; then echo "export TIMEOUT_CONNECT=\"$TIMEOUT_CONNECT\""  >> /etc/environment; fi
if [ ! -z "$TIMEOUT_SERVER" ]; then echo "export TIMEOUT_SERVER=\"$TIMEOUT_SERVER\""  >> /etc/environment; fi


exec /haproxy-entrypoint.sh "$@"

