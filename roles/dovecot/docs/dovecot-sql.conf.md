# dovecot-ldap.conf.ext

```yaml
dovecot_sql:
  driver: ""
  connect: ""
  default_pass_scheme: ""
  password_query: ""
  user_query: ""
  iterate_query: ""
```


## sqlite

```yaml
dovecot_sql:
  driver: sqlite
  connect: /etc/dovecot/authdb.sqlite
  default_pass_scheme: MD5
  password_query: |
    SELECT username, domain, password
    FROM users WHERE username: '%n' AND domain: '%d'
  user_query: |
    SELECT home, uid, gid
    FROM users WHERE username: '%n' AND domain: '%d'
  iterate_query: SELECT username AS user FROM users
```

## mysql

```yaml
dovecot_sql:
  driver: mysql
  connects:
    host: localhost
    dbname: mails
    user: testuser
    password: pass
  default_pass_scheme: CRAM-MD5
  password_query: SELECT password FROM mailbox WHERE username = '%u'
  user_query: |
    SELECT
      '/srv/mail/%d/%n' as home,
      CONCAT('maildir:/srv/mail/', maildir) AS mail,
      1101 AS uid,
      1101 AS gid
      FROM mailbox
      WHERE username = '%u'
```
