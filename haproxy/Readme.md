## HAProxy Docker image

This image is generic, thus you can obviously re-use it within
your non-related EEA projects.

 - Debian: **Jessie**
 - HAProxy: **1.8**
 - Expose: **5000**

### Supported tags and respective Dockerfile links

  - `:latest` [*Dockerfile*](https://github.com/eea/eea.docker.haproxy/blob/master/haproxy/Dockerfile) - Debian: **Jessie**, HAProxy: **1.8**

### Stable and immutable tags

  - `:1.8-1.3` [*Dockerfile*](https://github.com/eea/eea.docker.haproxy/tree/1.8-1.3/haproxy/Dockerfile) - HAProxy: **1.8** Release: **1.3**

See [older versions](https://github.com/eea/eea.docker.haproxy/releases)


### Changes

 - [CHANGELOG.md](https://github.com/eea/eea.docker.haproxy/blob/master/CHANGELOG.md)

### Base docker image

 - [hub.docker.com](https://hub.docker.com/r/eeacms/haproxy)


### Source code

  - [github.com](http://github.com/eea/eea.docker.haproxy)


### Installation

1. Install [Docker](https://www.docker.com/)
2. Install [Docker Compose](https://docs.docker.com/compose/install/).

## Usage


### Run with Docker Compose

Here is a basic example of a `docker-compose.yml` file using the `eeacms/haproxy` docker image:

    version: "2"
    services:
      haproxy:
        image: eeacms/haproxy
        depends_on:
        - webapp
        ports:
        - "80:5000"
        - "1936:1936"
        environment:
          BACKENDS: "webapp"
          DNS_ENABLED: "true"
          LOG_LEVEL: "info"

      webapp:
        image: eeacms/hello


The application can be scaled to use more server instances, with `docker-compose scale`:

    $ docker-compose up -d
    $ docker-compose scale webapp=4

The results can be checked in a browser, navigating to http://localhost.
By refresing the page multiple times it is noticeable that the IP of the server
that served the page changes, as HAProxy switches between them.
The stats page can be accessed at http://localhost:1936 where you have to log in
using the `STATS_AUTH` authentication details (default `admin:admin`).

Note that it may take **up to one minute** until backends are plugged-in due to the
minimum possible `DNS_TTL`.


### Run with backends specified as environment variable

    $ docker run --env BACKENDS="192.168.1.5:80 192.168.1.6:80" eeacms/haproxy

Using the `BACKENDS` variable is a way to quick-start the container.
The servers are written as `server_ip:server_listening_port`,
separated by spaces (and enclosed in quotes, to avoid issues).
The contents of the variable are evaluated in a python script that writes
the HAProxy configuration file automatically.

If there are multiple DNS records for one or more of your `BACKENDS` (e.g. when deployed using rancher-compose),
you can use `DNS_ENABLED` environment variable. This way, haproxy will load-balance
all of your backends instead of only the first entry found:

  $ docker run --link=webapp -e BACKENDS="webapp" -e DNS_ENABLED=true eeacms/haproxy


### Use a custom configuration file mounted as a volume

    $ docker run -v conf.d/haproxy.cfg:/etc/haproxy/haproxy.cfg eeacms/haproxy:latest


If you edit `haproxy.cfg` you can reload it without having to restart the container:

    $ docker exec <name-of-your-container> reload


### Extend the image with a custom haproxy.cfg file

Additionally, you can supply your own static `haproxy.cfg` file by extending the image

    FROM eeacms/haproxy:latest
    COPY conf.d/haproxy.cfg /etc/haproxy/haproxy.cfg

    RUN apt-get install...

and then run

    $ docker build -t your-image-name:your-image-tag path/to/Dockerfile

## Supported environment variables ##

As HAProxy has close to no purpose by itself, this image should be used in
combination with others (for example with [Docker Compose](https://docs.docker.com/compose/)).

HAProxy can be configured by modifying the following env variables,
either when running the container or in a `docker-compose.yml` file.

  * `STATS_PORT` The port to bind statistics to - default `1936`
  * `STATS_AUTH` The authentication details (written as `user:password` for the statistics page - default `admin:admin`
  * `FRONTEND_NAME` The label of the frontend - default `http-frontend`
  * `FRONTEND_PORT` The port to bind the frontend to - default `5000`
  * `FRONTEND_MODE` Frontend mode - default `http`
  * `PROXY_PROTOCOL_ENABLED` The option to enable or disable accepting proxy protocol (`true` stands for enabled, `false` or anything else for disabled) - default `false`
  * `COOKIES_ENABLED` The option to enable or disable cookie-based sessions (`true` stands for enabled, `false` or anything else for disabled) - default `false`
  * `BACKEND_NAME` The label of the backend - default `http-backend`
  * `BACKENDS` The list of `server_ip:server_listening_port` to be load-balanced by HAProxy, separated by space - by default it is not set
  * `BACKENDS_PORT` Port to use when auto-discovering backends, or when `BACKENDS` are specified without port - by default `80`
  * `BACKENDS_MODE` Backends mode - default `http`
  * `BALANCE` The algorithm used for load-balancing - default `roundrobin`
  * `SERVICE_NAMES` An optional prefix for services to be included when discovering services separated by space. - by default it is not set
  * `LOGGING` Override logging ip address:port - default is udp `127.0.0.1:514` inside container
  * `LOG_LEVEL` Set haproxy log level, default is `notice` ( only send important events ). Can be: `emerg`,`alert`,`crit`,`err`,`warning`,`notice`,`info`,`debug`
  * `DNS_ENABLED` DNS lookup provided `BACKENDS`. Use this option when your backends are resolved by an internal/external DNS service (e.g. **Docker 1.11+**, **Rancher**)
  * `DNS_TTL` DNS lookup backends every `DNS_TTL` minutes. Default `1` minute.
  * `TIMEOUT_CONNECT` the maximum time to wait for a connection attempt to a VPS to succeed. Default `5000` ms
  * `TIMEOUT_CLIENT` timeouts apply when the client is expected to acknowledge or send data during the TCP process. Default `50000` ms
  * `TIMEOUT_SERVER` timeouts apply when the server is expected to acknowledge or send data during the TCP process. Default `50000` ms
  * `HTTPCHK` The HTTP method and uri used to check on the servers health - default `HEAD /`
  * `INTER` parameter sets the interval between two consecutive health checks. If not specified, the default value is `2s`
  * `FAST_INTER` parameter sets the interval between two consecutive health checks when the server is any of the transition state (read above): UP - transitionally DOWN or DOWN - transitionally UP. If not set, then `INTER` is used.
  * `DOWN_INTER` parameter sets the interval between two consecutive health checks when the server is in the DOWN state. If not set, then `INTER` is used.
  * `RISE` number of consecutive valid health checks before considering the server as UP. Default value is `2`
  * `FALL` number of consecutive invalid health checks before considering the server as DOWN. Default value is `3`


## Logging

By default the logs from haproxy are present in the docker log, by using the rsyslog inside the container (UDP port 514). No access logs are present by default, but this can be changed by setting the log level.

You can change the logging level by providing the `LOG_LEVEL` environment variable:

    docker run -e LOG_LEVEL=info  ... eeacms/haproxy

You can override the log output by providing the `LOGGING` environment variable:

    docker run -e LOGGING=logs.example.com:5005 ... eeacms/haproxy

Now make sure that `logs.example.com` listen on UDP port `5005`

## Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The Original Code is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.


## Funding

[European Environment Agency (EU)](http://eea.europa.eu)
