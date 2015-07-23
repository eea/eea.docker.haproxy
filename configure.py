import os
import socket
import sys


if sys.argv[1] == "update":
    configuration = open("/etc/haproxy/haproxy.cfg", "a")
    index = 1
    backend_conf = ""

    try:
        hosts = open("/etc/hosts")
    except:
        exit(0)

    localhost = socket.gethostbyname(socket.gethostname())
    existing_hosts = []
    if os.environ['COOKIES_ENABLED'].lower() == "true":
        cookies = "cookie value"
    else:
        cookies = ""

    for host in hosts:
        if "0.0.0.0" in host or "127.0.0.1" in host or localhost in host or "::" in host:
            continue
        host_ip = host.split()[0]
        if host_ip in existing_hosts:
            continue
        existing_hosts.append(host_ip)
        backend_conf += """        server http-server%d %s:80 %s check\n""" % (index, host_ip, cookies)
        index += 1

    print >> configuration, backend_conf

    exit(0)



with open("/etc/haproxy/haproxy.cfg", "a") as configuration:
    listen_conf = """listen stats
        bind *:%s
        stats enable
        stats uri /
        stats hide-version
        stats auth %s""" % (os.environ['STATS_PORT'],
                            os.environ['STATS_AUTH'])

    frontend_conf = """frontend %s
        bind *:%s
        mode http
        default_backend %s""" % (os.environ['FRONTEND_NAME'],
                                 os.environ['FRONTEND_PORT'],
                                 os.environ['BACKEND_NAME'])

    backend_conf = """backend %s
        mode http
        balance %s
        option forwardfor
        http-request set-header X-Forwarded-Port %%[dst_port]
        http-request add-header X-Forwarded-Proto https if { ssl_fc }
        option httpchk HEAD / HTTP/1.1\\r\\nHost:localhost
        cookie SRV_ID prefix\n""" % (os.environ['BACKEND_NAME'],
                                       os.environ['BALANCE'])
    if os.environ['COOKIES_ENABLED'].lower() == "true":
        cookies = "cookie value"
    else:
        cookies = ""

    if sys.argv[1] == "hosts":
        try:
            hosts = open("/etc/hosts")
        except:
            exit(0)

        index = 1
        localhost = socket.gethostbyname(socket.gethostname())
        existing_hosts = []

        for host in hosts:
            if "0.0.0.0" in host or "127.0.0.1" in host or localhost in host or "::" in host:
                continue
            host_ip = host.split()[0]
            if host_ip in existing_hosts:
                continue
            existing_hosts.append(host_ip)
            backend_conf += """        server http-server%d %s:80 %s check\n""" % (index, host_ip, cookies)
            index += 1

    if sys.argv[1] == "env":
        for index, backend_server in enumerate(os.environ['BACKENDS'].split(' ')):
            host = backend_server.split(':')[0]
            port = backend_server.split(':')[1]
            backend_conf += """\
            server http-server%d %s:%s %s check\n""" % (index, host, port, cookies)

    print >> configuration
    print >> configuration, listen_conf
    print >> configuration, frontend_conf
    print >> configuration, backend_conf
