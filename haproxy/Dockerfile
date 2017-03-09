FROM haproxy:1.7
MAINTAINER "Alin Voinea" <alin.voinea@eaudeweb.ro>

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      python3-pip \
      dnsutils \
      inotify-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install chaperone dnspython3

RUN groupadd -r haproxy && useradd -r -g haproxy haproxy

RUN mkdir -p /var/log/haproxy
RUN ln -s /usr/local/etc/haproxy /etc/haproxy
RUN chown -R haproxy:haproxy /usr/local/etc/haproxy /var/log/haproxy

COPY src/chaperone.conf         /etc/chaperone.d/chaperone.conf
COPY src/haproxy.cfg            /tmp/haproxy.cfg
COPY src/docker-setup.sh        /docker-setup.sh
COPY src/configure.py           /configure.py
COPY src/reload.sh              /usr/bin/reload
COPY src/track_hosts.sh         /track_hosts
COPY src/track_dns.sh           /track_dns

ENTRYPOINT ["/usr/local/bin/chaperone"]
CMD ["--user", "haproxy"]
