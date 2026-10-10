# Runtime and deployment runbook

Local Python 3.13.9 is used in a private .venv; Linux image targets 3.12. Actual versions/results are recorded in PROJECT_STATE.md. Linux requirements-linux.lock was captured from the actual Python 3.12 image after 59 tests passed. Docker base image is pinned by its tested digest. Docker daemon is unavailable locally; Linux builds run on the authorized Linode.

## Credentials

Use ignored `.env`, never Git. Required: `MANAGER_USERNAME`, `MANAGER_PASSWORD`; inference: `INFERENCE_API_KEY`, approved `INFERENCE_BASE_URL`, `INFERENCE_MODEL`; optional source contact: `NWS_USER_AGENT`. The only approved inference endpoint in this build is the workshop HTTPS endpoint. A provider change requires approval and an explicit allowlist update. Credentials are loaded at server start; restart after local edits, preserve database.

Budget variables in `.env.example` are enforced. `APP_TIMEZONE` validates the default Kansas City preset timezone; other sites use NWS-verified timezone. `DEPLOYMENT_LABEL` and `BUILD_COMMIT` are operator-supplied display metadata, not deployment proof.

### Existing VM authorization (2026-10-10)

User provided existing Ubuntu 24.04 VM `172.234.201.174`, root SSH and key path `C:\Users\thien\.ssh\closurecall_akamai`. Setup/deployment is authorized, public exposure remains withheld. No new resource purchase is needed. First SSH connection recorded its host key in ignored `data/deployment_known_hosts` using trust on first use (`accept-new`); subsequent connections use strict checking. Key authentication is verified with a two-hour Git OpenSSH agent identity. The Windows agent refused importing the key; use the Git ssh/ssh-add pair consistently with its SSH_AUTH_SOCK. Never write the passphrase into scripts or command arguments.

Prepared `bootstrap_ubuntu.sh` follows official Docker apt repository installation, refuses conflicting packages instead of removing them, installs a non-root key-authenticated deployment user, and leaves access restrictions for a second-session check. `deploy_verified.sh` builds a commit-tagged image, runs tests inside that Linux image before replacing a service, uses the exact tested image with `--no-build`, and preserves the named SQLite volume. Bootstrap actually passed on Ubuntu 24.04.4. Docker 29.9.0 / Compose 5.6.0 and hello-world verified. Second closurecall session passed before hardening; SSH is key-only, UFW active with only SSH allowed. Configuration backup is under /root/closurecall-config-backups. Root key-only recovery remains available.

## Private Akamai deployment

Before creating any VM, verify credits, show the actual region, plan, disk, price and resource label in Cloud Manager and obtain approval. Suggested Ubuntu 24.04 x86_64, around 2 vCPU/4 GB, no GPU. No paid resource was provisioned by this repository.

Use SSH key, a deploy user, and appropriate firewall. SSH binary locally: `C:\Windows\System32\OpenSSH\ssh.exe`. Confirm a second SSH connection before changing access. Inspect existing Docker before installing; use the official Ubuntu apt repository instructions, never blindly pipe a script or remove an existing installation.

Transfer reviewed source only, never .env/.venv/DB through Git. Existing private environment is /opt/closurecall/config/.env (600), parent directory 700; never overwrite it during a source release. Keep backend bound to loopback, with a named persistent data volume:

```bash
chmod 600 .env
sudo docker compose config --quiet
sudo docker compose up -d --build
curl --fail http://127.0.0.1:8000/health
```

On Windows, tunnel `ssh -N -L 127.0.0.1:8081:127.0.0.1:8000 DEPLOY_USER@SERVER_IP`. Remote UI is http://127.0.0.1:8081; local UI is port 8000. Neither is a public judging URL. Public exposure/DNS/HTTPS needs approval; never public plain-HTTP Basic Auth.

## Persistence verification

Run live evaluation, human decision, outbox and replay on the VM. Record IDs, timestamps and hash. Backup with SQLite backup API before migration/deploy. Restart container and replay the same decision; compare exact bundle hash and notification drafts. Do not run `down -v`, prune volumes or reset DB. Record measured remote latency and tools; capture redacted resource evidence. Linux dependency lock and base digest are now captured from the tested image. Compose runs non-root, read-only root filesystem, dropped capabilities, no-new-privileges, bounded processes/memory/logs and one worker. /app/data is the persistent writable volume; /tmp is ephemeral.

## Recovery

Pending jobs become interrupted on restart. Re-evaluate explicitly. No decision/notification side effects are retried automatically. Idempotency keys protect duplicate user requests. An override of stale/incomplete evidence requires a human reason; consider re-evaluation first. Backups never overwrite an existing destination. Code rollback requires schema compatibility review and preserving data.

## Verified release procedure

Export a secret-scanned local Git commit into a new /opt/closurecall/releases/<full-commit> directory. Run `bash scripts/deploy_verified.sh <release> /opt/closurecall/config/.env <full-commit>` from that release. Tests must pass inside the exact built image before Compose starts it with --no-build. Keep BUILD_COMMIT set to that full commit for every later Compose command; otherwise its default tag is local. Backups created by scripts/backup_db.py are under the database parent data/backups, persisted in the Docker volume. Never run down -v or prune volumes.

Ubuntu security package upgrades completed on 2026-10-10; reboot scheduled before first app deployment to apply the updated kernel. Verify fresh key-authenticated SSH, Docker, UFW and sshd settings after reboot. Do not assume scheduling a reboot proves it finished.

Local port 8080 is occupied by an existing AgentService.exe; it was preserved. Use scripts/open_tunnel.ps1 (foreground, default 8081) or the equivalent Git OpenSSH command. Tunnel access is private; no public judging URL.
