
# 10-auth.conf

```yaml
dovecot_auth:
  disable_plaintext_auth: false
  auth_cache_size: 0
  auth_cache_ttl: "1 hour"
  auth_cache_negative_ttl: "1 hour"
  auth_realms: []
  auth_default_realm: ""
  auth_username_chars: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890"
  auth_username_translation: ""
  auth_username_format: "%Lu"
  auth_master_user_separator: ""
  auth_anonymous_username: anonymous
  auth_worker_max_count: 80
  auth_gssapi_hostname: ""
  auth_krb5_keytab: ""
  auth_use_winbind: false
  auth_winbind_helper_path: ""
  auth_failure_delay: 2 secs
  auth_ssl_require_client_cert: false
  auth_ssl_username_from_cert: false
  auth_mechanisms:
    - plain
    - login
    - cram-md5
  includes:
    - "# auth-deny.conf.ext"
    - "# auth-master.conf.ext"
    - auth-system.conf.ext
    - "# auth-sql.conf.ext"
    - "# auth-ldap.conf.ext"
    - "# auth-passwdfile.conf.ext"
    - "# auth-checkpassword.conf.ext"
    - "# auth-vpopmail.conf.ext"
    - "# auth-static.conf.ext"
```
