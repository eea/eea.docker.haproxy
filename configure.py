import os


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

    for index, backend_server in enumerate(os.environ['BACKEND_SERVERS'].split(' ')):
        host = backend_server.split(':')[0]
        port = backend_server.split(':')[1]
        backend_conf += """\
        server http-server%d %s:%s %s check\n""" % (index, host, port, cookies)
    print >> f
    print >> f, listen_conf
    print >> f, frontend_conf
    print >> f, backend_conf
