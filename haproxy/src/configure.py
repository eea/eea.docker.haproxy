import os
import socket
import sys

FRONTEND_NAME = os.environ.get('FRONTEND_NAME', 'http-frontend')
FRONTEND_PORT = os.environ.get('FRONTEND_PORT', '5000')
BACKEND_NAME = os.environ.get('BACKEND_NAME', 'http-backend')
BALANCE = os.environ.get('BALANCE', 'roundrobin')
SERVICE_NAMES = os.environ.get('SERVICE_NAMES', '').split(';')
COOKIES_ENABLED = (os.environ.get('COOKIES_ENABLED', 'false').lower() == "true")
STATS_PORT = os.environ.get('STATS_PORT', '1936')
STATS_AUTH = os.environ.get('STATS_AUTH', 'admin:admin')
BACKENDS = os.environ.get('BACKENDS', '').split(' ')
BACKENDS_PORT = os.environ.get('BACKENDS_PORT', '80')

listen_conf = """
  listen stats
    bind *:%(port)s
    stats enable
    stats uri /
    stats hide-version
    stats auth %(auth)s
"""

frontend_conf = """
  frontend %(name)s
    bind *:%(port)s
    mode http
    default_backend %(backend)s
"""

backend_conf = """
  backend %(backend)s
    mode http
    balance %(balance)s
    option forwardfor
    http-request set-header X-Forwarded-Port %%[dst_port]
    http-request add-header X-Forwarded-Proto https if { ssl_fc }
    option httpchk HEAD / HTTP/1.1\\r\\nHost:localhost
    cookie SRV_ID prefix
"""

backend_conf_plus = """
    server http-server%(index)d %(host)s:%(port)s %(cookies)s check
"""

with open("/etc/haproxy/haproxy.cfg", "a") as configuration:

    backend_conf = backend_conf % dict(backend=BACKEND_NAME, balance=BALANCE)

    if COOKIES_ENABLED:
        cookies = "cookie value"
    else:
        cookies = ""

    service_names = SERVICE_NAMES

    if sys.argv[1] == "hosts":
        try:
            hosts = open("/etc/hosts")
        except:
            exit(0)

        index = 1
        localhost = socket.gethostbyname(socket.gethostname())
        existing_hosts = set()

        for host in hosts:
            if "0.0.0.0" in host:
                continue
            if "127.0.0.1" in host:
                continue
            if localhost in host:
                continue
            if "::" in host:
                continue

            part = host.split()
            if len(part) < 2:
                continue

            (host_ip, host_name) = part[0:2]
            if host_ip in existing_hosts or not any(host_name.startswith(name) for name in service_names):
                continue

            existing_hosts.add(host_ip)
            host_port = BACKENDS_PORT
            backend_conf += backend_conf_plus % dict(
                    index=index,
                    host=host_ip,
                    port=host_port,
                    cookies=cookies
            )
            index += 1

    if sys.argv[1] == "env":
        for index, backend_server in enumerate(BACKENDS):
            server_port = backend_server.split(':')
            host = server_port[0]
            port = server_port[1] if len(server_port) > 1 else BACKENDS_PORT
            backend_conf += backend_conf_plus % dict(
                    index=index,
                    host=host,
                    port=port,
                    cookies=cookies)

    configuration.write(listen_conf % dict(port=STATS_PORT, auth=STATS_AUTH))
    configuration.write(frontend_conf % dict(
        name=FRONTEND_NAME, port=FRONTEND_PORT, backend=BACKEND_NAME
    ))
    configuration.write(backend_conf)
