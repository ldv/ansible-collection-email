# 10-director.conf 

```yaml
dovecot_director:
  director_servers: ""
  director_mail_servers: ""
  director_user_expire: "15 min"
  director_username_hash: "%Lu"
  director_services:
      # service director {
      #   unix_listener login/director {
      #     #mode: 0666
      #   }
      #   fifo_listener login/proxy-notify {
      #     #mode: 0666
      #   }
      #   unix_listener director-userdb {
      #     #mode: 0600
      #   }
      #   inet_listener {
      #     #port: ""
      #   }
      # }
    - director:
        - listener: unix
          type: login/director
          mode: "0666"
        - listener: fifo
          type: login/proxy-notify
          mode: "0666"
        - listener: unix
          type: director-userdb
          mode: "0600"
        - listener: inet
          port: ""
    # service imap-login {
    #   #executable = imap-login director
    # }
    # service pop3-login {
    #   #executable = pop3-login director
    # }
    # service submission-login {
    #   #executable = submission-login director
    # }
    - logins:
        - imap: {}
            # executable: imap-login director
        - pop3: {}
            # executable: pop3-login director
        - submission: {}
            # executable: submission-login director
    # # Enable director for LMTP proxying:
    # protocol lmtp {
    #   #auth_socket_path: director-userdb
    # }
    - protocols:
        - lmtp: {}
            # auth_socket_path: director-userdb
```
