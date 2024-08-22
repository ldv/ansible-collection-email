# auth-checkpassword.ext.conf


```yaml
dovecot_authentications:
  - checkpassword:
      passdb:
        driver: checkpassword
        args: /usr/bin/checkpassword
      userdb:
        driver: prefetch

```

