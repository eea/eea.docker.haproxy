FROM haproxy:1.8
LABEL maintainer="EEA: IDM2 A-Team <eea-edw-a-team-alerts@googlegroups.com>"

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    python3-pip \
    cron \
    rsyslog \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s /usr/local/etc/haproxy /etc/haproxy \
 && sed -i '/#cron./c\cron.*                          \/proc\/1\/fd\/1'  /etc/rsyslog.conf \
 && sed -i '/#$ModLoad imudp/c\$ModLoad imudp'  /etc/rsyslog.conf \
 && sed -i '/#$UDPServerRun/c\$UDPServerRun 514'  /etc/rsyslog.conf \
 && sed -i '/$UDPServerRun 514/a $UDPServerAddress 127.0.0.1' /etc/rsyslog.conf \
 && sed -i '/cron.*/a local2.*                          \/proc\/1\/fd\/1' /etc/rsyslog.conf \
 && mv /docker-entrypoint.sh /haproxy-entrypoint.sh

COPY src/haproxy.cfg            /tmp/
COPY docker-entrypoint.sh src/configure.py src/track_hosts src/track_dns /
