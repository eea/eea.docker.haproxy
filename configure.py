import os
import socket


with open("/etc/haproxy/haproxy.cfg", "a") as f:
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

    hosts_from_file = False
    index = 1

    try:
        hosts = open("/etc/hosts")
    except:
        hosts = None

    if hosts:
        localhost = socket.gethostbyname(socket.gethostname())
        existing_hosts = []

        for host in hosts:
            if "0.0.0.0" in host or "127.0.0.1" in host or localhost in host or "::" in host:
                continue
            hosts_from_file = True
            host_ip = host.split()[0]
            host_name = host.split()[1]
            if host_ip in existing_hosts:
                continue
            existing_hosts.append(host_ip)
            backend_conf += """        server http-server%d %s:80 %s check\n""" % (index, host_name, cookies)
            index += 1

    if hosts_from_file is False:
        for index, backend_server in enumerate(os.environ['BACKEND_SERVERS'].split(' ')):
            host = backend_server.split(':')[0]
            port = backend_server.split(':')[1]
            backend_conf += """\
            server http-server%d %s:%s %s check\n""" % (index, host, port, cookies)

    print >> f
    print >> f, listen_conf
    print >> f, frontend_conf
    print >> f, backend_conf
