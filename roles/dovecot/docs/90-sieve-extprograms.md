# 90-sieve-extprograms.conf


```yaml
dovecot_sieve_extprograms:
  plugins:
    - default:
        sieve_pipe_socket_dir: sieve-pipe
        sieve_filter_socket_dir: sieve-filter
        sieve_execute_socket_dir: sieve-execute
        sieve_pipe_bin_dir: /usr/lib/dovecot/sieve-pipe
        sieve_filter_bin_dir: /usr/lib/dovecot/sieve-filter
        sieve_execute_bin_dir: /usr/lib/dovecot/sieve-execute

  services:
    - do-something:
        user: dovenull
        executable: "script /usr/lib/dovecot/sieve-pipe/do-something.sh"
        listeners:
          - sieve-pipe/do-something:
              type: unix
              user: vmail
              mode: "0600"
```

