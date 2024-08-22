# 15-mailboxes.conf


```yaml
dovecot_defaults_mailboxes:
  namespaces:
    - inbox:
        disabled: false
        hidden: false
        ignore_on_failure: false
        inbox: true
        list: true
        location: ""
        order: 0
        prefix: ""
        separator: ""
        subscriptions: true
        type: private
        Archive:
          special_use: \Archive
        Drafts:
          # false     - Never created automatically.
          # create    - Automatically created, but no automatic subscription.
          # subscribe - Automatically created and subscribed.
          auto: subscribe
          autoexpunge: 0
          autoexpunge_max_mails: 0
          comment: ""
          driver: ""
          special_use: \Drafts
        Junk:
          special_use: \Junk
        Sent:
          special_use: \Sent
        "Sent Messages":
          special_use: \Sent
        Trash:
          special_use: \Trash
        virtual/All:
          comment: "All my messages"
          special_use: \All
        virtual/Flagged:
          comment: "All my flagged messages"
          special_use: \Flagged
```

