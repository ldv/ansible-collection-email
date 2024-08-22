# 10-ssl.conf

```yaml
dovecot_ssl:
  enabled: false
  # cert: "/etc/dovecot/private/dovecot.pem"
  # key: "/etc/dovecot/private/dovecot.key"
  # key_password: ""
  # ca: ""
  # require_crl: true
  client_ca_dir: /etc/ssl/certs
  # client_ca_file: ""
  # verify_client_cert: false
  # cert_username_field: commonName
  # # Generate new params with `openssl dhparam -out /etc/dovecot/dh.pem 4096`
  # dh: "/usr/share/dovecot/dh.pem"
  min_protocol: TLSv1.2
  # cipher_list:
  #   - ALL
  #   - "!DH"
  #   - "!kRSA"
  #   - "!SRP"
  #   - "!kDHd"
  #   - "!DSS"
  #   - "!aNULL"
  #   - "!eNULL"
  #   - "!EXPORT"
  #   - "!DES"
  #   - "!3DES"
  #   - "!MD5"
  #   - "!PSK"
  #   - "!RC4"
  #   - "!ADH"
  #   - "!LOW@STRENGTH"
  # curve_list:
  #   - P-521
  #   - P-384
  #   - P-256
  # ssl_prefer_server_ciphers: false
  # # for valid values run "openssl engine"
  # ssl_crypto_device: ""
  # ssl_options: ""
```
