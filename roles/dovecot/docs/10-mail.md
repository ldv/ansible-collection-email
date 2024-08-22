# 10-mail.conf

```yaml
dovecot_defaults_mail:
  # mail_location: "mbox:~/mail:INBOX=/var/mail/%u"
  namespaces:
    - name: inbox
      # type: private
      # separator: ""
      # prefix: ""
      # location: ""
      inbox: true
      # hidden: false
      # list: true
      # subscriptions: true
      # ignore_on_failure: false
      # mailboxes:
      #   - name: Drafts
      #     auto: no
      #     autoexpunge: 0
      #     autoexpunge_max_mails: 0
      #     comment: ""
      #     driver: ""
      #     special_use: "\Drafts"

  #   - name: ""
  #     #type: shared
  #     #separator: /
  #     #prefix: shared/%%u/
  #     #location: maildir:%%h/Maildir:INDEX=~/Maildir/shared/%%u
  #     #subscriptions: false
  #     #list: children
  #     #order: 0
  # mail_shared_explicit_inbox: false
  # mail_uid: ""
  # mail_gid: ""
  # mail_privileged_group: mail
  # mail_access_groups: ""
  # mail_full_filesystem_access: false
  # mail_attribute_dict: ""
  # mail_server_comment: ""
  # mail_server_admin: ""
  # mmap_disable: false
  # dotlock_use_excl: true
  # mail_fsync: optimized
  # lock_method: fcntl
  # mail_temp_dir: /tmp

  # <doc/wiki/UserIds.txt>
  # first_valid_uid: 1101
  # last_valid_uid: 1101
  # first_valid_gid: 1101
  # last_valid_gid: 1101
  # mail_max_keyword_length: 50
    # <doc/wiki/Chrooting.txt>
  valid_chroot_dirs: []
  # mail_chroot: ""
  # auth_socket_path: /var/run/dovecot/auth-userdb
  # mail_plugin_dir: /usr/lib/dovecot/modules
  # mail_plugins: []
  # mailbox_list_index: true
  # mailbox_list_index_very_dirty_syncs: true
  # mailbox_list_index_include_inbox: false
  # mail_cache_min_mail_count: 0
  # mailbox_idle_check_interval: 30 secs
  # mail_save_crlf: false
  # mail_prefetch_count: 0
  # mail_temp_scan_interval: 1w
  # mail_sort_max_read_count: 0
    # protocol !indexer-worker {
    #   #mail_vsize_bg_after_count: 0
    # }
  mail_protocols:
    - name: "!indexer-worker"
      # mail_vsize_bg_after_count: 0
  # maildir_stat_dirs: false
  # maildir_copy_with_hardlinks: true
  # maildir_very_dirty_syncs: false
  # maildir_broken_filename_sizes: false
  # maildir_empty_new: false
  # mbox_read_locks:
  #   - fcntl
  # mbox_write_locks:
  #   - fcntl
  #   - dotlock
  # mbox_lock_timeout: 5 mins
  # mbox_dotlock_change_timeout: 2 mins
  # mbox_dirty_syncs: true
  # mbox_very_dirty_syncs: false
  # mbox_lazy_writes: true
  # mbox_min_index_size: 0
  # mbox_md5: apop3d
  # mdbox_rotate_size: 10M
  # mdbox_rotate_interval: 0
  # mdbox_preallocate_space: false
  # mail_attachment_dir: ""
  # mail_attachment_min_size: 128k
  mail_attachment_fs: "sis posix"
  # mail_attachment_hash: "%{sha256:80}"
  # mail_attachment_detection_options: ""
```
