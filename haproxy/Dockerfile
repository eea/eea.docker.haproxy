FROM haproxy:1.7
MAINTAINER "Alin Voinea" <alin.voinea@eaudeweb.ro>

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    python3-pip \
    cron \
    rsyslog \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && groupadd -r haproxy \
 && useradd -r -g haproxy haproxy \
 && mkdir -p /var/log/haproxy \
 && ln -s /usr/local/etc/haproxy /etc/haproxy \
 && chown -R haproxy:haproxy /usr/local/etc/haproxy /var/log/haproxy \
 && sed -i '/#cron./c\cron.*                          \/proc\/1\/fd\/1'  /etc/rsyslog.conf


COPY src/reload                 /usr/bin/
COPY src/haproxy.cfg            /tmp/
COPY src/docker-setup.sh src/configure.py src/track_hosts src/track_dns /

ENTRYPOINT ["/docker-setup.sh"]
CMD []
