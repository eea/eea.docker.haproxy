# Changelog


## 2019-11-28 (1.8-1.5)

- Add COOKIES_PARAMS variable to give the possibility to add expiration time to cookies

## 2019-11-22 (1.8-1.4)

- Upgrade HAproxy to 1.8.22
- Fix BACKENDS_MODE typo, set the default values of FRONTEND_MODE and BACKENDS_MODE to depend on each other
- Only enable /track_hosts cron when BACKENDS and DNS_ENABLED env vars are not present. 
- Only add http check option when backend is of type http.

## 2018-11-21 (1.8-1.3)

- Upgrade to haproxy 1.8.14
- Move the restart of rsyslog and cron to run at every docker start


## 2018-08-02 (1.8-1.2)

- Upgrade to haproxy 1.8.13

## 2018-04-11 (1.8-1.1)

- Fix entrypoint to work when haproxy.cfg externally is provided.

## 2017-12-05 (1.8-1.0)

- Upgrade to haproxy 1.8

- Possibility to change frontend/backend `mode` to `TCP` via environment variables `FRONTEND_MODE` and `BACKENDS_MODE` [refs #10]

## 2017-11-30 (1.7-4.1)

- bugfix add LOG_LEVEL to /etc/environment as well


## 2017-11-22 (1.7-4.0)

- Remove chaperone in favour of cron

- Release 4.0

## 2017-03-22

- Fix /track_dns cron when no backend is up

- Refactor /track_hosts: use chaperone cron instead of inotify

- Remove unnecessary image layers

## 2017-03-09

- Add possibility to customize backend health check via environment variables

## 2017-02-22

- Fix HAProxy version inside 1.6 tag

- Release HAProxy 1.7

## 2017-02-17

- surround cookie with quotas [chiridra refs #82353]

## 2017-01-30

- Fixed session stickiness [chiridra refs #81199]

## 2017-01-03

- Fix DNS lookup to work with latest Rancher version (1.2.0+)

## 2016-04-18

- Support for named backends resolved by an internal/external DNS service (e.g. when deployed using rancher-compose)

## 2016-01-15

- Start HAProxy on port *5000* instead of *80*

- Start all processes with *haproxy* user instead of *root*

- Added chaperone process manager

- Improved haproxy auto-reloading backends

- Fixed issue #2: How to specify to eeacms/haproxy a different web app port?
  Added possibility to define backends port via $BACKENDS_PORT env

## 2015-07-20

- Initial public release
