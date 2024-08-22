# 20-submission.conf


```yaml
dovecot_submission: {}
  # hostname: ""
  # SMTP Submission logout format string:
  #  %i - total number of bytes read from client
  #  %o - total number of bytes sent to client
  #  %{command_count} - Number of commands received from client
  #  %{reply_count} - Number of replies sent to client
  #  %{session} - Session ID of the login session
  #  %{transaction_id} - ID of the current transaction, if any
  # logout_format: in=%i out=%o
  # max_mail_size: ""
  # max_recipients: ""
  # whitespace-before-path:
  #   Allow one or more spaces or tabs between `MAIL FROM:' and path and between
  #   `RCPT TO:' and path.
  # mailbox-for-path:
  #   Allow using bare Mailbox syntax (i.e., without <...>) instead of full path
  #   syntax.
  # client_workarounds: []
  # relay_host: ""
  # relay_port: ""
  # relay_trusted: false
  # relay_user: ""
  # relay_master_user: ""
  # relay_password: ""
  # no        - No SSL is used
  # smtps     - An SMTPS connection (immediate SSL) is used
  # starttls  - The STARTTLS command is used to establish SSL layer
  # relay_ssl: false
  # relay_ssl_verify: true
  # relay_rawlog_dir: ""
  # protocols:
  #   - submission:  {}
  #       #mail_plugins: $mail_plugin
  #       #mail_max_userip_connections: 10
```

