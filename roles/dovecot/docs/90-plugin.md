# 90-plugin.conf


```yaml
dovecot_plugin:
  plugins:
    - autosubscribe: INBOX.Sent
    - autosubscribe2: INBOX.Trash
    - autosubscribe3: INBOX.Drafts
    - autosubscribe4: INBOX.Junk
    - autosubscribe5: INBOX.Archive
    - mail_log_events: "delete undelete expunge copy mailbox_delete mailbox_rename"
    - mail_log_fields: "uid box msgid size from subject"
```

