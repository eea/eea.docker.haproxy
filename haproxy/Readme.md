## HAProxy Docker image

 - HAProxy 1.6.3

This image is generic, thus you can obviously re-use it within
your non-related EEA projects.

### Warning

For security reasons, latest builds of this image run HAProxy on default port **5000**
instead of **80**. Please update your deployment accordingly.

### Supported tags and respective Dockerfile links

  - `:latest` [*Dockerfile*](https://github.com/eea/eea.docker.haproxy/blob/master/haproxy/Dockerfile) (default)
  - `:1.6` [*Dockerfile*](https://github.com/eea/eea.docker.haproxy/blob/1.6/haproxy/Dockerfile)
  - `:1.5` [*Dockerfile*](https://github.com/eea/eea.docker.haproxy/blob/1.5/haproxy/Dockerfile)

### Changes

 - [CHANGELOG.md](https://github.com/eea/eea.docker.haproxy/blob/master/CHANGELOG.md)

### Base docker image

 - [hub.docker.com](https://registry.hub.docker.com/u/eeacms/haproxy)


### Source code

  - [github.com](http://github.com/eea/eea.docker.haproxy)


### Installation

1. Install [Docker](https://www.docker.com/) **Please note**: version must not be 1.8.x due to docker issue [#16619](https://github.com/docker/docker/issues/16619)
2. Install [Docker Compose](https://docs.docker.com/compose/install/).

## Usage


### Run with Docker Compose

Here is a basic example of a `docker-compose.yml` file using the `eeacms/haproxy` docker image:

    haproxy:
      image: eeacms/haproxy
      links:
      - webapp
      ports:
      - "80:80"
      - "1936:1936"

    webapp:
      image: eeacms/hello


The application can be scaled to use more server instances, with `docker-compose scale`:

    $ docker-compose scale webapp=4
    $ docker-compose up -d

The results can be checked in a browser, navigating to http://localhost.
By refresing the page multiple times it is noticeable that the IP of the server
that served the page changes, as HAProxy switches between them.
The stats page can be accessed at http://localhost:1936 where you have to log in
using the `STATS_AUTH` authentication details (default `admin:admin`).


### Run with backends specified as environment variable

    $ docker run --env BACKENDS="192.168.1.5:80 192.168.1.6:80" eeacms/haproxy

Using the `BACKENDS` variable is a way to quick-start the container.
The servers are written as `server_ip:server_listening_port`,
separated by spaces (and enclosed in quotes, to avoid issues).
The contents of the variable are evaluated in a python script that writes
the HAProxy configuration file automatically.
By default, the `BACKENDS` variable is not set.

If there are multiple DNS records for one or more of your `BACKENDS` (e.g. when deployed using rancher-compose),
you can use `DNS_ENABLED` environment variable. This way, haproxy will load-balance
all of your backends instead of only the first entry found:

  $ docker run --link=webapp -e BACKENDS="webapp" -e DNS_ENABLED=true eeacms/haproxy

It will also automatically add/remove backends when you scale them.

### Link this container to one or more application containers

    $ docker run --link app_instance_1 --link app_instance_2 eeacms/haproxy:latest

When linking containers with the `--link` flag, entries in `/etc/hosts`
are automatically added by `docker`. This image is configured so in absence
of a `haproxy.cfg` file and when the `BACKENDS` variable is not set it will
automatically parse `/etc/hosts` and create and load the configuration for `haproxy`.
In this scenario, the file `/etc/hosts` will be monitored and every time it is
modified (for example when restarting a linked container) configuration for
`haproxy` will be automatically recreated and reloaded.


### Use a custom configuration file mounted as a volume

    $ docker run -v conf.d/haproxy.cfg:/etc/haproxy/haproxy.cfg eeacms/haproxy:latest

This is the preferred way to start a container because the configuration
file can be modified locally at any time. In order for the modifications to be
applied, the configuration has to be reloaded, which can be done by running:

    $ docker exec <name-of-your-container> reload


### Extend the image with a custom haproxy.cfg file

Additionally, you can supply your own static `haproxy.cfg` file by extending the image

    FROM eeacms/haproxy:latest
    COPY conf.d/haproxy.cfg /etc/haproxy/haproxy.cfg

    USER root
    RUN apt-get install...
    USER haproxy

and then run

    $ docker build -t your-image-name:your-image-tag path/to/Dockerfile

### Run with Docker Compose and multiple web apps

If you have multiple apps running on port 80 HAProxy will by default proxy them all. If you want
to restrict it to just one app then specify the `SERVICE_NAMES` environment variable.

    haproxy:
      image: eeacms/haproxy
      links:
      - webapp
      ports:
      - "80:80"
      - "1936:1936"
      environment:
      - SERVICE_NAMES=webapp

    first_webapp:
      image: eeacms/hello

    second_webapp:
      image: eeacms/hello

    third_app:
      image: eeacms/hello

Note that haproxy will not serve requests from `third_app` because of the `SERVICE_NAMES` variable.
You could also say: `SERVICE_NAMES=first_webapp second_webapp`

### Upgrade

    $ docker pull eeacms/haproxy:latest


## Supported environment variables ##

As HAProxy has close to no purpose by itself, this image should be used in
combination with others (for example with [Docker Compose](https://docs.docker.com/compose/)).
HAProxy can be configured by modifying the following env variables,
either when running the container or in a `docker-compose.yml` file.

  * `STATS_PORT` The port to bind statistics to - default `1936`
  * `STATS_AUTH` The authentication details (written as `user:password` for the statistics page - default `admin:admin`
  * `FRONTEND_NAME` The label of the frontend - default `http-frontend`
  * `FRONTEND_PORT` The port to bind the frontend to - default `5000`
  * `PROXY_PROTOCOL_ENABLED` The option to enable or disable accepting proxy protocol (`true` stands for enabled, `false` or anything else for disabled) - default `false`
  * `COOKIES_ENABLED` The option to enable or disable cookie-based sessions (`true` stands for enabled, `false` or anything else for disabled) - default `false`
  * `BACKEND_NAME` The label of the backend - default `http-backend`
  * `BACKENDS` The list of `server_ip:server_listening_port` to be load-balanced by HAProxy, separated by space - by default it is not set
  * `BACKENDS_PORT` Port to use when auto-discovering backends, or when `BACKENDS` are specified without port - by default `80`
  * `BALANCE` The algorithm used for load-balancing - default `roundrobin`
  * `SERVICE_NAMES` An optional prefix for services to be included when discovering services separated by space. - by default it is not set
  * `LOGGING` Override logging ip address:port - default is udp `127.0.0.1:514` inside container
  * `DNS_ENABLED` DNS lookup provided `BACKENDS`. Use this option when your backends are resolved by an internal/external DNS service (e.g. Rancher)
  * `DNS_TTL` DNS lookup backends every $DNS_TTL minutes. Default 1 minute.

## Logging

By default there are no logs from haproxy because they are sent on UDP port 514 inside container.
You can override this behaviour by providing the `LOGGING` environment variable:

    docker run -e LOGGING=logs.example.com:5005 -e BACKENDS=www1 www2 www3 eeacms/haproxy

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
