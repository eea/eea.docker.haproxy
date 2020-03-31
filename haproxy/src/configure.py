import os
import socket
import sys
from string import Template
import subprocess

################################################################################
# INIT
################################################################################

FRONTEND_NAME = os.environ.get('FRONTEND_NAME', 'http-frontend')
FRONTEND_PORT = os.environ.get('FRONTEND_PORT', '5000')
FRONTEND_MODE = os.environ.get('FRONTEND_MODE', os.environ.get('BACKENDS_MODE','http'))
BACKEND_NAME = os.environ.get('BACKEND_NAME', 'http-backend')
BALANCE = os.environ.get('BALANCE', 'roundrobin')
SERVICE_NAMES = os.environ.get('SERVICE_NAMES', '')
COOKIES_ENABLED = (os.environ.get('COOKIES_ENABLED', 'false').lower() == "true")
COOKIES_PARAMS = os.environ.get('COOKIES_PARAMS','')
PROXY_PROTOCOL_ENABLED = (os.environ.get('PROXY_PROTOCOL_ENABLED', 'false').lower() == "true")
STATS_PORT = os.environ.get('STATS_PORT', '1936')
STATS_AUTH = os.environ.get('STATS_AUTH', 'admin:admin')
BACKENDS = os.environ.get('BACKENDS', '').split(' ')
BACKENDS_PORT = os.environ.get('BACKENDS_PORT', '80')
BACKENDS_MODE = os.environ.get('BACKENDS_MODE', FRONTEND_MODE)
LOGGING = os.environ.get('LOGGING', '127.0.0.1')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'notice')
TIMEOUT_CONNECT = os.environ.get('TIMEOUT_CONNECT', '5000')
TIMEOUT_CLIENT = os.environ.get('TIMEOUT_CLIENT', '50000')
TIMEOUT_SERVER = os.environ.get('TIMEOUT_SERVER', '50000')
HTTPCHK = os.environ.get('HTTPCHK', 'HEAD /')
HTTPCHK_HOST = os.environ.get('HTTPCHK_HOST', 'localhost')
INTER = os.environ.get('INTER', '2s')
FAST_INTER = os.environ.get('FAST_INTER', INTER)
DOWN_INTER = os.environ.get('DOWN_INTER', INTER)
RISE = os.environ.get('RISE', '2')
FALL = os.environ.get('FALL', '3')


listen_conf = Template("""
  listen stats
    bind *:$port
    stats enable
    stats uri /
    stats hide-version
    stats auth $auth
""")

frontend_conf = Template("""
  frontend $name
    bind *:$port $accept_proxy
    mode $mode
    default_backend $backend
""")

if COOKIES_ENABLED:
    #if we choose to enable session stickiness
    #then insert a cookie named SRV_ID to the request:
    #all responses from HAProxy to the client will contain a Set-Cookie:
    #header with a specific value for each backend server as its cookie value.
    backend_conf = Template("""
  backend $backend
    mode $mode
    balance $balance
    default-server inter $inter fastinter $fastinter downinter $downinter fall $fall rise $rise
    cookie SRV_ID insert $cookies_params
""")
    cookies = "cookie \\\"@@value@@\\\""
else:
    #the old template and behaviour for backward compatibility
    #in this case the cookie will not be set - see below the value for
    #cookies variable (is set to empty)
    backend_conf = Template("""
  backend $backend
    mode $mode
    balance $balance
    default-server inter $inter fastinter $fastinter downinter $downinter fall $fall rise $rise
    cookie SRV_ID prefix $cookies_params
""")
    cookies = ""

backend_type_http = Template("""
    option forwardfor
    http-request set-header X-Forwarded-Port %[dst_port]
    http-request add-header X-Forwarded-Proto https if { ssl_fc }
    option httpchk $httpchk HTTP/1.1\\r\\nHost:$httpchk_host
""")

backend_conf_plus = Template("""
    server $name-$index $host:$port $cookies check
""")

health_conf = """
listen default
  bind *:4242
"""

backend_conf = backend_conf.substitute(
    backend=BACKEND_NAME,
    mode=BACKENDS_MODE,
    balance=BALANCE,
    inter=INTER,
    fastinter=FAST_INTER,
    downinter=DOWN_INTER,
    fall=FALL,
    rise=RISE,
    cookies_params=COOKIES_PARAMS
)

if BACKENDS_MODE == 'http':
    backend_conf += backend_type_http.substitute(
        httpchk=HTTPCHK,
        httpchk_host=HTTPCHK_HOST
    )

################################################################################
# Backends are resolved using internal or external DNS service
################################################################################
if sys.argv[1] == "dns":
    ips = {}
    for index, backend_server in enumerate(BACKENDS):
        server_port = backend_server.split(':')
        host = server_port[0]
        port = server_port[1] if len(server_port) > 1 else BACKENDS_PORT

        try:
            records = subprocess.check_output(["getent", "hosts", host])
        except Exception as err:
            print(err)
        else:
            for record in records.splitlines():
                ip = record.split()[0].decode()
                ips[ip] = host

    with open('/etc/haproxy/dns.backends', 'w') as bfile:
        bfile.write(' '.join(sorted(ips)))

    for ip, host in ips.items():
        backend_conf += backend_conf_plus.substitute(
            name=host.replace(".", "-"),
            index=ip.replace(".", "-"),
            host=ip,
            port=port,
            cookies=cookies.replace('@@value@@', ip))

################################################################################
# Backends provided via BACKENDS environment variable
################################################################################

elif sys.argv[1] == "env":
    for index, backend_server in enumerate(BACKENDS):
        server_port = backend_server.split(':')
        host = server_port[0]
        port = server_port[1] if len(server_port) > 1 else BACKENDS_PORT
        backend_conf += backend_conf_plus.substitute(
                name=host.replace(".", "-"),
                index=index,
                host=host,
                port=port,
                cookies=cookies.replace('@@value@@', host))

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
        backend_conf += backend_conf_plus.substitute(
                name='http-server',
                index=index,
                host=host_ip,
                port=host_port,
                cookies=cookies.replace('@@value@@', host_ip)
        )
        index += 1

    with open('/etc/haproxy/hosts.backends', 'w') as bfile:
        bfile.write(' '.join(sorted(existing_hosts)))

if PROXY_PROTOCOL_ENABLED:
    accept_proxy = "accept-proxy"
else:
    accept_proxy = ""

with open("/etc/haproxy/haproxy.cfg", "w") as configuration:
    with open("/tmp/haproxy.cfg", "r") as default:
        conf = Template(default.read())
        conf = conf.substitute(
            LOGGING=LOGGING,
            LOG_LEVEL=LOG_LEVEL,
            TIMEOUT_CLIENT=TIMEOUT_CLIENT,
            TIMEOUT_CONNECT=TIMEOUT_CONNECT,
            TIMEOUT_SERVER=TIMEOUT_SERVER
        )

        configuration.write(conf)

    configuration.write(
        listen_conf.substitute(
            port=STATS_PORT, auth=STATS_AUTH
        )
    )

    configuration.write(
        frontend_conf.substitute(
            name=FRONTEND_NAME,
            port=FRONTEND_PORT,
            mode=FRONTEND_MODE,
            backend=BACKEND_NAME,
            accept_proxy=accept_proxy
        )
    )

    configuration.write(backend_conf)
    configuration.write(health_conf)
