# 20-imap.conf


```yaml
  # hibernate_timeout: 0
  # max_line_length: 64k
  #
  #  %i - total number of bytes read from client
  #  %o - total number of bytes sent to client
  #  %{fetch_hdr_count} - Number of mails with mail header data sent to client
  #  %{fetch_hdr_bytes} - Number of bytes with mail header data sent to client
  #  %{fetch_body_count} - Number of mails with mail body data sent to client
  #  %{fetch_body_bytes} - Number of bytes with mail body data sent to client
  #  %{deleted} - Number of mails where client added \Deleted flag
  #  %{expunged} - Number of mails that client expunged, which does not
  #                include automatically expunged mails
  #  %{autoexpunged} - Number of mails that were automatically expunged after
  #                    client disconnected
  #  %{trashed} - Number of mails that client copied/moved to the
  #               special_use=\Trash mailbox.
  #  %{appended} - Number of mails saved during the session
  logout_format:
    - "in=%i"
    - "out=%o"
    - "deleted=%{deleted}"
    - "expunged=%{expunged}"
    - "trashed=%{trashed}"
    - "hdr_count=%{fetch_hdr_count}"
    - "hdr_bytes=%{fetch_hdr_bytes}"
    - "body_count=%{fetch_body_count}"
    - "body_bytes=%{fetch_body_bytes}"
  # capability: ""
  # idle_notify_interval: 2 mins
  # id_send: ""
  # id_log: ""
  #
  #   delay-newmail:
  #     Send EXISTS/RECENT new mail notifications only when replying to NOOP
  #     and CHECK commands. Some clients ignore them otherwise, for example OSX
  #     Mail (<v2.1). Outlook Express breaks more badly though, without this it
  #     may show user "Message no longer in server" errors. Note that OE6 still
  #     breaks even with this workaround if synchronization is set to
  #     "Headers Only".
  #   tb-extra-mailbox-sep:
  #     Thunderbird gets somehow confused with LAYOUT=fs (mbox and dbox) and
  #     adds extra '/' suffixes to mailbox names. This option causes Dovecot to
  #     ignore the extra '/' instead of treating it as invalid mailbox name.
  #   tb-lsub-flags:
  #     Show \Noselect flags for LSUB replies with LAYOUT=fs (e.g. mbox).
  #     This makes Thunderbird realize they aren't selectable and show them
  #     greyed out, instead of only later giving "not selectable" popup error.
  client_workarounds:
    - delay-newmail
  #   - tb-extra-mailbox-sep
  #   - tb-lsub-flags
  # urlauth_host: ""
  # literal_minus: false
  #
  #   disconnect-immediately:
  #     The FETCH is aborted immediately and the IMAP client is disconnected.
  #   disconnect-after:
  #     The FETCH runs for all the requested mails returning as much data as
  #     possible. The client is finally disconnected without a tagged reply.
  #   no-after:
  #     Same as disconnect-after, but tagged NO reply is sent instead of
  #     disconnecting the client. If the client attempts to FETCH the same failed
  #     mail more than once, the client is disconnected. This is to avoid clients
  #     from going into infinite loops trying to FETCH a broken mail.
  fetch_failure: disconnect-immediately
  protocols:
    - imap:
        mail_plugins: $mail_plugins
        mail_max_userip_connections: 10
```

