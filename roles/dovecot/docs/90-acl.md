# 90-acl.conf


```yaml
dovecot_acl:
  plugins:
    - acl: vfile:/etc/dovecot/global-acls:cache_secs=300
    - acl_shared_dict: file:/var/lib/dovecot/shared-mailboxes
```

