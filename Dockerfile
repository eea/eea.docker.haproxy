FROM haproxy:latest

MAINTAINER "Razvan Chitu" <razvan.chitu@eaudeweb.ro>

RUN apt-get update && \
	apt-get install -y ca-certificates && \
	apt-get install -y rsyslog && \
	apt-get install -y python && \
	apt-get clean && \
	mv /usr/local/etc/haproxy /etc/haproxy

COPY etc/haproxy/haproxy_default.cfg		/tmp/haproxy_default.cfg
COPY etc/rsyslog.d/49-haproxy.conf 			/etc/rsyslog.d/49-haproxy.conf
COPY start.sh 								/usr/bin/start
COPY reload.sh 								/usr/bin/reload
COPY configure.py 							/configure.py

ENV STATS_PORT=1936 \
	STATS_AUTH=admin:admin \
    FRONTEND_NAME=http-frontend \
    FRONTEND_PORT=80 \
    COOKIES_ENABLED=false \
    BACKEND_NAME=http-backend \
    BACKEND_SERVERS=0.0.0.0:80 \
    BALANCE=roundrobin

CMD ["start"]