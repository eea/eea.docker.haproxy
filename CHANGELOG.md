# Changelog

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
