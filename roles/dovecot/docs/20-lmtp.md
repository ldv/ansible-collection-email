# 20-lmtp.conf


```yaml
dovecot_defaults_lmtp:
  # proxy: false
  # save_to_detail_mailbox: false
  # rcpt_check_quota: false

  # The default is "final", which is the same as the one given to
  # RCPT TO command.
  # "original" uses the address given in RCPT TO's ORCPT
  # parameter,
  # "none" uses nothing. Note that "none" is currently always used
  # when a mail has multiple recipients.

  # hdr_delivery_address: final
  protocols:
    - lmtp:
        mail_plugins: $mail_plugins
```

