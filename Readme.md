## HAProxy Docker image

 - HAProxy 1.5.14

This image is generic, thus you can obviously re-use it within
your non-related EEA projects.

### Supported tags and respective Dockerfile links

  -  `:latest` (default)
  -  `:1.5`


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
      image: razvan3895/nodeserver


The application can be scaled to use more server instances, with `docker-compose scale`:

    $ docker-compose scale webapp=4 haproxy=1

The results can be checked in a browser, navigating to http://localhost.
By refresing the page multiple times it is noticeable that the IP of the server
that served the page changes, as HAProxy switches between them.
The stats page can be accessed at http://localhost:1936 where you have to log in
using the `STATS_AUTH` authentication details (default `admin:admin`).


### Run with backends specified as environment variable

    $ docker run --env BACKENDS="192.168.1.5:80 192.168.1.6:80" eeacms/haproxy:latest

Using the `BACKENDS` variable is a way to quickstart the container.
The servers are written as `server_ip:server_listening_port`,
separated by spaces (and enclosed in quotes, to avoid issues).
The contents of the variable are evaluated in a python script that writes
the HAProxy configuration file automatically.
By default, the `BACKENDS` variable is not set.


### Link this container to one or more application containers

    $ docker run --link app_instance_1 --link app_instance_2 eeacms/haproxy:latest

When linking containers with the `--link` flag, entries in `/etc/hosts`
are automatically added by `docker`. This image is configured so in absence
of a `haproxy.cfg` file and when the `BACKENDS` variable is not set it will
automatically parse `/etc/hosts` and create and load the configuration for `haproxy`.
In this scenario, the file `/etc/hosts` will be monitored and everytime it is
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

and then run

    $ docker build -t your-image-name:your-image-tag path/to/Dockerfile


### Upgrade

    $ docker pull eeacms/haproxy:latest


## Supported environment variables ##

### haproxy.env ###

As HAProxy has close to no purpose by itself, this image should be used in
combination with others (for example with [Docker Compose](https://docs.docker.com/compose/)).
HAProxy can be configured by modifying the following env variables,
either when running the container or in a `docker-compose.yml` file,
preferably by supplying an `.env` file in the appropriate tag.

  * `STATS_PORT` The port to bind statistics to - default `1936`
  * `STATS_AUTH` The authentication details (written as `user:password` for the statistics page - default `admin:admin`
  * `FRONTEND_NAME` The label of the frontend - default `http-frontend`
  * `FRONTEND_PORT` The port to bind the frontend to - default `80`
  * `COOKIES_ENABLED` The option to enable or disable cookie-based sessions (`true` stands for enabled, `false` or anything else for disabled) - default `false`
  * `BACKEND_NAME` The label of the backend - default `http-backend`
  * `BACKENDS` The list of `server_ip:server_listening_port` to be load-balanced by HAProxy, separated by space - by default it is not set
  * `BALANCE` The algorithm used for load-balancing - default `roundrobin`
  * `SERVICE_NAMES` An optional prefix for services to be included when discovering services. - by default it is not set


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
