FROM haproxy:1.7
MAINTAINER "Alin Voinea" <alin.voinea@eaudeweb.ro>


#install gosu
ENV GOSU_VERSION 1.10
RUN set -ex; \
        \
        fetchDeps=' \
                ca-certificates \
                wget \
        '; \
        apt-get update; \
        apt-get install -y --no-install-recommends $fetchDeps; \
        rm -rf /var/lib/apt/lists/*; \
        \
        dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
        wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
        wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
        \
# verify the signature
        export GNUPGHOME="$(mktemp -d)"; \
        gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
        gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
        rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc; \
        \
        chmod +x /usr/local/bin/gosu; \
# verify that the binary works
        gosu nobody true; \
        \
        apt-get purge -y --auto-remove $fetchDeps

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
 && sed -i '/#cron./c\cron.*                          \/proc\/1\/fd\/1'  /etc/rsyslog.conf \
 && sed -i '/#$ModLoad imudp/c\$ModLoad imudp'  /etc/rsyslog.conf \
 && sed -i '/#$UDPServerRun/c\$UDPServerRun 514'  /etc/rsyslog.conf \
 && sed -i '/$UDPServerRun 514/a $UDPServerAddress 127.0.0.1' /etc/rsyslog.conf \
 && sed -i '/cron.*/a local2.*                          \/proc\/1\/fd\/1' /etc/rsyslog.conf \
 && mv /docker-entrypoint.sh /haproxy-entrypoint.sh



COPY src/reload                 /usr/bin/
COPY src/haproxy.cfg            /tmp/
COPY docker-entrypoint.sh src/configure.py src/track_hosts src/track_dns /



