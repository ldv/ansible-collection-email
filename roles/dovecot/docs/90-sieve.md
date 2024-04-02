# 90-sieve.conf


```yaml
dovecot_sieve:
  plugins:
    - default:
        sieve: file:%h/sieve;active=%h/dovecot.sieve
        sieve_dir: /srv/mail/sieve/%d/%u
        sieve_global_dir: /srv/mail/sieve/global
        # sieve_default: /var/lib/dovecot/sieve/default.sieve
        # sieve_default_name: ""
        # sieve_global: ""
        # sieve_discard: ""
        # sieve_before: /var/lib/dovecot/sieve.d/
        # sieve_before2: ldap:/etc/sieve-ldap.conf;name=ldap-domain
        # sieve_before3: (etc...)
        # sieve_after: ""
        # sieve_after2: ""
        # sieve_after2: (etc...)
        sieve_extensions: "+notify +imapflags"
        # sieve_global_extensions: ""
        # sieve_plugins: ""
        # recipient_delimiter: +
        # sieve_max_script_size: 1M
        # sieve_max_actions: 32
        # sieve_max_redirects: 4
        # sieve_quota_max_scripts: 0
        # sieve_quota_max_storage: 0
        # sieve_user_email: ""
        # sieve_user_log: ""
        # sieve_redirect_envelope_from: sender
        # sieve_trace_dir: ""
        # #   "actions"        - Only print executed action commands, like keep,
        # #                      fileinto, reject and redirect.
        # #   "commands"       - Print any executed command, excluding test commands.
        # #   "tests"          - Print all executed commands and performed tests.
        # #   "matching"       - Print all executed commands, performed tests and the
        # #                      values matched in those tests.
        #sieve_trace_level: ""
        # sieve_trace_debug: false
        # sieve_trace_addresses: false
```

