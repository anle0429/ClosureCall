# Security boundary

ClosureCall is a prototype for synthetic administrative offices and employees. It does not establish building safety, government operating authority or notification delivery.

- All business APIs require server-side manager authentication. The actor comes from that principal.
- The model sees frozen inputs through five scoped read-only tools. It cannot change policy, approve a decision or send a message.
- Source requests are bounded and validated; source/model errors become safe codes rather than raw provider responses.
- Approval/outbox writes are transactional and idempotent. Replay reads frozen records and verifies hashes.
- The private deployment binds to loopback and runs as a non-root user with a read-only root filesystem. Secrets and persistent data remain outside source control.

Basic authentication is suitable here only within the private local/tunnel arrangement or an explicitly approved HTTPS setup. Enterprise SSO, independent zone verification, operational resilience certification and a privileged-host tamper-proof audit system are not implemented.

No public vulnerability-reporting address or disclosure program has been designated. If you are a collaborator, report a concern privately through a contact channel already agreed with the maintainer. Do not include credentials, private employee information or raw provider diagnostics in a public issue. Public access and contact details must be chosen before publication.
