# auth-master.ext.conf


```yaml
dovecot_authentications:
  - master:
      passdb:
        driver: passwd-file
        master: true
        args: /etc/dovecot/master-users
        pass: true
```

