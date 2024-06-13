#!/bin/bash

#fix variable _name to not have /
if [ -n "$FRONTEND_NAME" ]; then
    export FRONTEND_NAME="${FRONTEND_NAME//\//}"
fi
if [ -n "$BACKEND_NAME" ]; then
    export BACKEND_NAME="${BACKEND_NAME//\//}"
fi

# haproxy not directly configured within /usr/local/etc/haproxy/haproxy.cfg
if ! test -e /usr/local/etc/haproxy/haproxy.cfg; then
    if [ -n "$DNS_ENABLED" ]; then
      # Backends are resolved using internal or external DNS service
      touch /etc/haproxy/dns.backends
      python3 /configure.py dns
      echo "*/${DNS_TTL:-1} * * * * /track_dns  | logger " > /var/crontab.txt
    
    else
    
      if [ -n "$BACKENDS" ]; then
        # Backend provided via $BACKENDS env
        python3 /configure.py env
      else
        # Find backend within /etc/hosts
        touch /etc/haproxy/hosts.backends
        python3 /configure.py hosts
        echo "*/${DNS_TTL:-1} * * * * /track_hosts  | logger " > /var/crontab.txt
      fi
    
    fi
    
    #add crontab
    crontab /var/crontab.txt
    chmod 600 /etc/crontab
    
    #Add env variables for haproxy
    echo "export PATH=$PATH"':$PATH' >> /etc/environment
    if [ -n "$BACKENDS" ]; then echo "export BACKENDS=\"$BACKENDS\""  >> /etc/environment; fi
    if [ -n "$BACKENDS_PORT" ]; then echo "export BACKENDS_PORT=\"$BACKENDS_PORT\""  >> /etc/environment; fi
    if [ -n "$BACKENDS_MODE" ]; then echo "export BACKENDS_MODE=\"$BACKENDS_MODE\""  >> /etc/environment; fi
    if [ -n "$BACKEND_NAME" ]; then echo "export BACKEND_NAME=\"$BACKEND_NAME\""  >> /etc/environment; fi
    if [ -n "$BALANCE" ]; then echo "export BALANCE=\"$BALANCE\""  >> /etc/environment; fi
    if [ -n "$COOKIES_ENABLED" ]; then echo "export COOKIES_ENABLED=\"$COOKIES_ENABLED\""  >> /etc/environment; fi
    if [ -n "$COOKIES_NAME" ]; then echo "export COOKIES_NAME=\"$COOKIES_NAME\""  >> /etc/environment; fi
    if [ -n "$COOKIES_PARAMS" ]; then echo "export COOKIES_PARAMS=\"$COOKIES_PARAMS\""  >> /etc/environment; fi
    if [ -n "$DOWN_INTER" ]; then echo "export DOWN_INTER=\"$DOWN_INTER\""  >> /etc/environment; fi
    if [ -n "$FALL" ]; then echo "export FALL=\"$FALL\""  >> /etc/environment; fi
    if [ -n "$FAST_INTER" ]; then echo "export FAST_INTER=\"$FAST_INTER\""  >> /etc/environment; fi
    if [ -n "$FRONTEND_NAME" ]; then echo "export FRONTEND_NAME=\"$FRONTEND_NAME\""  >> /etc/environment; fi
    if [ -n "$FRONTEND_PORT" ]; then echo "export FRONTEND_PORT=\"$FRONTEND_PORT\""  >> /etc/environment; fi
    if [ -n "$FRONTEND_MODE" ]; then echo "export FRONTEND_MODE=\"$FRONTEND_MODE\""  >> /etc/environment; fi
    if [ -n "$HTTPCHK" ]; then echo "export HTTPCHK=\"$HTTPCHK\""  >> /etc/environment; fi
    if [ -n "$HTTPCHK_HOST" ]; then echo "export HTTPCHK_HOST=\"$HTTPCHK_HOST\""  >> /etc/environment; fi
    if [ -n "$INTER" ]; then echo "export INTER=\"$INTER\""  >> /etc/environment; fi
    if [ -n "$LOGGING" ]; then echo "export LOGGING=\"$LOGGING\""  >> /etc/environment; fi
    if [ -n "$LOG_LEVEL" ]; then echo "export LOG_LEVEL=\"$LOG_LEVEL\""  >> /etc/environment; fi
    if [ -n "$PROXY_PROTOCOL_ENABLED" ]; then echo "export PROXY_PROTOCOL_ENABLED=\"$PROXY_PROTOCOL_ENABLED\""  >> /etc/environment; fi
    if [ -n "$RISE" ]; then echo "export RISE=\"$RISE\""  >> /etc/environment; fi
    if [ -n "$MAXCONN" ]; then echo "export MAXCONN=\"$MAXCONN\""  >> /etc/environment; fi
    if [ -n "$SERVICE_NAMES" ]; then echo "export SERVICE_NAMES=\"$SERVICE_NAMES\""  >> /etc/environment; fi
    if [ -n "$STATS_AUTH" ]; then echo "export STATS_AUTH=\"$STATS_AUTH\""  >> /etc/environment; fi
    if [ -n "$STATS_PORT" ]; then echo "export STATS_PORT=\"$STATS_PORT\""  >> /etc/environment; fi
    if [ -n "$STATS_REFRESH" ]; then echo "export STATS_REFRESH=\"$STATS_REFRESH\""  >> /etc/environment; fi
    if [ -n "$TIMEOUT_CLIENT" ]; then echo "export TIMEOUT_CLIENT=\"$TIMEOUT_CLIENT\""  >> /etc/environment; fi
    if [ -n "$TIMEOUT_CONNECT" ]; then echo "export TIMEOUT_CONNECT=\"$TIMEOUT_CONNECT\""  >> /etc/environment; fi
    if [ -n "$TIMEOUT_SERVER" ]; then echo "export TIMEOUT_SERVER=\"$TIMEOUT_SERVER\""  >> /etc/environment; fi
fi


#start logging
service rsyslog restart

#start crontab
service cron restart

exec /usr/local/bin/haproxy-entrypoint.sh "$@"

