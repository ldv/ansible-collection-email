# auth-passwdfile.ext.conf


```yaml
dovecot_authentications:
  - passwdfile:
      passdb:
        driver: passwd-file
        args: scheme=CRYPT username_format=%u /etc/dovecot/users
      userdb:
        driver: passwd-file
        args: username_format=%u /etc/dovecot/users
        default_fields: quota_rule=*:storage=1G
        # override_fields: home=/home/virtual/%u
```

