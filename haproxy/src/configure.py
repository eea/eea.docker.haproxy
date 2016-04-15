import os
import socket
import sys
import dns.resolver

################################################################################
# INIT
################################################################################

FRONTEND_NAME = os.environ.get('FRONTEND_NAME', 'http-frontend')
FRONTEND_PORT = os.environ.get('FRONTEND_PORT', '5000')
BACKEND_NAME = os.environ.get('BACKEND_NAME', 'http-backend')
BALANCE = os.environ.get('BALANCE', 'roundrobin')
SERVICE_NAMES = os.environ.get('SERVICE_NAMES', '')
COOKIES_ENABLED = (os.environ.get('COOKIES_ENABLED', 'false').lower() == "true")
PROXY_PROTOCOL_ENABLED = (os.environ.get('PROXY_PROTOCOL_ENABLED', 'false').lower() == "true")
STATS_PORT = os.environ.get('STATS_PORT', '1936')
STATS_AUTH = os.environ.get('STATS_AUTH', 'admin:admin')
BACKENDS = os.environ.get('BACKENDS', '').split(' ')
BACKENDS_PORT = os.environ.get('BACKENDS_PORT', '80')
LOGGING = os.environ.get('LOGGING', '')

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
    bind *:%(port)s %(accept_proxy)s
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

if COOKIES_ENABLED:
    cookies = "cookie value"
else:
    cookies = ""

backend_conf = backend_conf % dict(backend=BACKEND_NAME, balance=BALANCE)


################################################################################
# Backends are resolved using internal or external DNS service
################################################################################
if sys.argv[1] == "dns":
    ips = set()
    for index, backend_server in enumerate(BACKENDS):
        server_port = backend_server.split(':')
        host = server_port[0]
        port = server_port[1] if len(server_port) > 1 else BACKENDS_PORT

        try:
            records = dns.resolver.query(host)
        except Exception as err:
            print(err)
            backend_conf += backend_conf_plus % dict(
                    index=index,
                    host=host,
                    port=port,
                    cookies=cookies)
        else:
            ips.update(str(ip) for ip in records)

    with open('/etc/haproxy/dns.backends', 'w') as bfile:
        bfile.write(' '.join(ips))

    for index, ip in enumerate(ips):
        backend_conf += backend_conf_plus % dict(
            index=index,
            host=host,
            port=port,
            cookies=cookies)

################################################################################
# Backends provided via BACKENDS environment variable
################################################################################

elif sys.argv[1] == "env":
    for index, backend_server in enumerate(BACKENDS):
        server_port = backend_server.split(':')
        host = server_port[0]
        port = server_port[1] if len(server_port) > 1 else BACKENDS_PORT
        backend_conf += backend_conf_plus % dict(
                index=index,
                host=host,
                port=port,
                cookies=cookies)

################################################################################
# Look for backend within /etc/hosts
################################################################################

elif sys.argv[1] == "hosts":
    try:
        hosts = open("/etc/hosts")
    except:
        exit(0)

    index = 1
    localhost = socket.gethostbyname(socket.gethostname())
    existing_hosts = set()

    #BBB
    if ';' in SERVICE_NAMES:
        service_names = SERVICE_NAMES.split(';')
    else:
        service_names = SERVICE_NAMES.split()

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
        if host_ip in existing_hosts:
            continue

        if service_names and not any(name in host_name for name in service_names):
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

if PROXY_PROTOCOL_ENABLED:
    accept_proxy = "accept-proxy"
else:
    accept_proxy = ""

with open("/etc/haproxy/haproxy.cfg", "w") as configuration:
    with open("/tmp/haproxy.cfg", "r") as default:
        conf = default.read()
        if LOGGING:
            conf = conf.replace('127.0.0.1', LOGGING)
        configuration.write(conf)
    configuration.write(listen_conf % dict(port=STATS_PORT, auth=STATS_AUTH))
    configuration.write(frontend_conf % dict(
        name=FRONTEND_NAME,
        port=FRONTEND_PORT,
        backend=BACKEND_NAME,
        accept_proxy=accept_proxy
    ))
    configuration.write(backend_conf)
