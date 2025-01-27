
# Ansible Role:  `bodsch.email.mailcow`

Ansible role to install and configure mailcow on various linux systems.

## usage 

```yaml
mailcow_version: latest

mailcow_source: git

mailcow_git:
  repository: 'https://github.com/bodsch/mailcow-dockerized.git'
  version: feature/full-disable-of-sogo

mailcow_install_path: "/var/lib/mailcow"

mailcow_service:
  state: stopped
  enabled: false

mailcow_config:
  hostname: "{{ inventory_hostname }}"
  password_scheme: BLF-CRYPT
  timezone: Europe/Berlin
  compose:
    project_name: cow
    command: docker compose     # ['docker compose' or 'docker-compose']
  log_lines: 99

mailcow_tls_certificate:
  source_files:
    cert: ""
    ca: ""
    dh: ""
    key: ""

mailcow_database:
  schema_name: mailcow
  username: mailcow
  password: mailcow
  root_password: mailcow_root

mailcow_redis:
  password: redis

mailcow_bindings:
  http:
    address: "127.0.0.1"
    port: 80
  https:
    address: ""
    port: 443
  smtp:
    address: ""
    port: 25
  smtps:
    address: ""
    port: 465
  submission:
    address: ""
    port: 587
  imap:
    address: ""
    port: 143
  imaps:
    address: ""
    port: 993
  "pop":
    address: ""
    port: 110
  pops:
    address: ""
    port: 995
  sieve:
    address: ""
    port: 4190
  doveadm:
    address: 127.0.0.1
    port: 19991
  database:
    address: 127.0.0.1
    port: 13306
  redis:
    address: 127.0.0.1
    port: 7654

mailcow_san:
  additional_sans: []
  autodiscover: false

mailcow_additional_server_names: []

mailcow_lets_encrypt:
  enabled: false

mailcow_api:
  allow_from: []
  read_only: []
  key: ""

mailcow_sni:
  enabled: true

mailcow_ip_check:
  enabled: true

mailcow_http_verification:
  enabled: false

mailcow_unbound_healthcheck:
  enabled: true

mailcow_clamd:
  enabled: true

mailcow_sogo:
  enabled: false
  expire_session: 480

mailcow_fts:
  enabled: true
  heap_memory: 128  # MiB
  procs: 1

mailcow_network:
  ipv4: "172.22.1"
  ipv6: "fd4d:6169:6c63:6f77::/64"

mailcow_snat:
  ipv4:
    to_source: ""
  ipv6:
    to_source: ""

mailcow_dovecot:
  master_user: ""
  master_pass: ""

mailcow_acme:
  contact: ""

mailcow_spamhaus:
  dqs_key: ""

mailcow_watchdog:
  enabled: true
  notify:
    emails: []
    webhook: ""
    webhook_body: ""
    ban: true
    start: false
  subject: ""
  external_checks: false
  verbose: false

mailcow_maildir:
  home: "Maildir"
  gc_time: 60
```

## Requirements & Dependencies

Installed docker.  
For example the collection [bodsch.docker](https://github.com/bodsch/ansible-collection-docker)

---

## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

## Author

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
