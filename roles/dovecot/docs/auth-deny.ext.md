# auth-deny.ext.conf


```yaml
dovecot_authentications:
  - deny:
      passdb:
        driver: passwd-file
        deny: true
        args: /etc/dovecot/deny-users
```

