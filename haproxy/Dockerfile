FROM haproxy:1.7
MAINTAINER "Shadow Walker" <ops@buluma.me.ke>

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    ca-certificates \
    python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && pip3 install chaperone \
 && groupadd -r haproxy \
 && useradd -r -g haproxy haproxy \
 && mkdir -p /var/log/haproxy \
 && ln -s /usr/local/etc/haproxy /etc/haproxy \
 && chown -R haproxy:haproxy /usr/local/etc/haproxy /var/log/haproxy

COPY src/chaperone.conf         /etc/chaperone.d/chaperone.conf
COPY src/reload                 /usr/bin/
COPY src/haproxy.cfg            /tmp/
COPY src/docker-setup.sh src/configure.py src/track_hosts src/track_dns /

ENTRYPOINT ["/usr/local/bin/chaperone"]
CMD ["--user", "haproxy"]
