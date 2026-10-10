# Runtime and deployment runbook

Local Python 3.13.9 is used in a private .venv; Linux image targets 3.12. Actual versions/results are recorded in PROJECT_STATE.md. Windows freeze is not a tested Linux lock. Docker daemon was unavailable during initial inspection; do not claim a successful image build until tested.

## Credentials

Use ignored `.env`, never Git. Required: `MANAGER_USERNAME`, `MANAGER_PASSWORD`; inference: `INFERENCE_API_KEY`, approved `INFERENCE_BASE_URL`, `INFERENCE_MODEL`; optional source contact: `NWS_USER_AGENT`. The only approved inference endpoint in this build is the workshop HTTPS endpoint. A provider change requires approval and an explicit allowlist update. Credentials are loaded at server start; restart after local edits, preserve database.

Budget variables in `.env.example` are enforced. `APP_TIMEZONE` validates the default Kansas City preset timezone; other sites use NWS-verified timezone. `DEPLOYMENT_LABEL` and `BUILD_COMMIT` are operator-supplied display metadata, not deployment proof.

### Existing VM authorization (2026-10-10)

User provided existing Ubuntu 24.04 VM `172.234.201.174`, root SSH and key path `C:\Users\thien\.ssh\closurecall_akamai`. Setup/deployment is authorized, public exposure remains withheld. No new resource purchase is needed. First SSH connection recorded its host key in ignored `data/deployment_known_hosts` using trust on first use (`accept-new`); subsequent connections use strict checking. Server accepts the public key, but private key requires a passphrase and Windows ssh-agent was stopped/disabled. User must unlock it locally; never send passphrase in chat.

Prepared `bootstrap_ubuntu.sh` follows official Docker apt repository installation, refuses conflicting packages instead of removing them, installs a non-root key-authenticated deployment user, and leaves access restrictions for a second-session check. `deploy_verified.sh` builds a commit-tagged image, runs tests inside that Linux image before replacing a service, uses the exact tested image with `--no-build`, and preserves the named SQLite volume. These scripts are prepared, not proof that remote execution passed. Inspect the live server before using them.

## Akamai gate (pending access/approval)

Before creating any VM, verify credits, show the actual region, plan, disk, price and resource label in Cloud Manager and obtain approval. Suggested Ubuntu 24.04 x86_64, around 2 vCPU/4 GB, no GPU. No paid resource was provisioned by this repository.

Use SSH key, a deploy user, and appropriate firewall. SSH binary locally: `C:\Windows\System32\OpenSSH\ssh.exe`. Confirm a second SSH connection before changing access. Inspect existing Docker before installing; use the official Ubuntu apt repository instructions, never blindly pipe a script or remove an existing installation.

Transfer reviewed source only, never .env/.venv/DB through Git. Enter secrets privately on the VM. Keep backend bound to loopback, with a named persistent data volume:

```bash
chmod 600 .env
sudo docker compose config --quiet
sudo docker compose up -d --build
curl --fail http://127.0.0.1:8000/health
```

On Windows, tunnel `ssh -N -L 8080:127.0.0.1:8000 DEPLOY_USER@SERVER_IP`. Remote UI is http://127.0.0.1:8080; local UI is port 8000. Neither is a public judging URL. Public exposure/DNS/HTTPS needs approval; never public plain-HTTP Basic Auth.

## Persistence verification

Run live evaluation, human decision, outbox and replay on the VM. Record IDs, timestamps and hash. Backup with SQLite backup API before migration/deploy. Restart container and replay the same decision; compare exact bundle hash and notification drafts. Do not run `down -v`, prune volumes or reset DB. Record measured remote latency and tools; capture redacted resource evidence. Pin a Linux-compatible dependency lock and image digest only after successful Linux testing.

## Recovery

Pending jobs become interrupted on restart. Re-evaluate explicitly. No decision/notification side effects are retried automatically. Idempotency keys protect duplicate user requests. An override of stale/incomplete evidence requires a human reason; consider re-evaluation first. Backups never overwrite an existing destination. Code rollback requires schema compatibility review and preserving data.
