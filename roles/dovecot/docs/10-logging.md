# 10-logging.conf

```yaml
dovecot_logging:
  auth_debug: false
  auth_debug_passwords: false
  auth_verbose: false
  # false, plain, sha1
  auth_verbose_passwords: false
  debug_log_path: /var/log/dovecot/debug.log

  # Format to use for logging mail deliveries:
  #  %$ - Delivery status message (e.g. "saved to INBOX")
  #  %m / %{msgid} - Message-ID
  #  %s / %{subject} - Subject
  #  %f / %{from} - From address
  #  %p / %{size} - Physical size
  #  %w / %{vsize} - Virtual size
  #  %e / %{from_envelope} - MAIL FROM envelope
  #  %{to_envelope} - RCPT TO envelope
  #  %{delivery_time} - How many milliseconds it took to deliver the mail
  #  %{session_time} - How long LMTP session took, not including delivery_time
  #  %{storage_id} - Backend-specific ID for mail, e.g. Maildir filename
  deliver_log_format: "msgid=%m [from=%f subject=%s]: %$"
  info_log_path: /var/log/dovecot/dovecot.log
  log_core_filter: ""
  log_debug: []
  log_path: ""
  log_timestamp: "%Y-%m-%d %H:%M:%S | "
  login_log_format: "%$: %s"
  login_log_format_elements:
    - "user=[%u]"
    - "method=%m"
    - "rip=%r"
    - "lip=%l"
    - "mpid=%e"
    - "%c"
  mail_debug: false
  mail_log_prefix: "%Us(%u): "
  syslog_facility: "" # mail
  verbose_ssl: false
  plugins:
    mail_log_events:
      # Events to log. Also available: flag_change append
      # delete undelete expunge copy mailbox_delete mailbox_rename
      - delete
      - undelete
      - expunge
      - copy
      - mailbox_delete
      - mailbox_rename
      - flag_change
      - append
    mail_log_fields:
      # Available fields: uid, box, msgid, from, subject, size, vsize, flags
      # size and vsize are available only for expunge and copy events.
      - uid
      - box
      - msgid
      - size
      - from
      - subject
      - vsize
      - flags
```
