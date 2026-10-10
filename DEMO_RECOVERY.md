# Private demo access and recovery

Stable application release: `e5f7801829aaa1f7cfd326e02e415f8389fa3dde`. Host: existing authorized Linode `172.234.201.174`. Deploy user: `closurecall`; root key-only access is recovery administration. Source: `/opt/closurecall/releases/e5f7801829aaa1f7cfd326e02e415f8389fa3dde`. Environment: `/opt/closurecall/config/.env`, never Git. Data: named volume `closurecall_closurecall-data`, database `/app/data/closurecall.sqlite3`. Do not replace it with a fixture/demo seed. Exact image ID: `sha256:11bddbc767275d8af7d603511596cc432b5862fe07fd880d5404fac8d13f7184`.

## Reopen the tunnel on Windows

Run in a PowerShell terminal you control:

```powershell
Set-Location -LiteralPath C:\Projects\ClosureCall
.\scripts\open_tunnel.ps1
```

The script runs foreground and forwards only `127.0.0.1:8081` to VM loopback port 8000, with strict pinned host identity and the existing key `C:\Users\thien\.ssh\closurecall_akamai`. Enter the key passphrase directly in that terminal if prompted; do not put it in arguments, files or chat. If an existing tunnel already owns 8081, keep it and open http://127.0.0.1:8081. If another process owns the port, use `-LocalPort 8082` and that URL; do not kill the unrelated process. Port 8080 already belongs to another service.

The pinned known-host file is the ignored `data/deployment_known_hosts`. Preserve it alongside operator backups. If missing or changed, stop and verify the VM fingerprint through a trusted channel; do not disable host-key verification. The temporary Git agent/socket may expire; foreground SSH can prompt for the encrypted key. Tunnel loss does not erase records. A reload requires manager sign-in again because credentials are held only in tab memory. Use the password from the ignored environment file; do not project it.

V2 recovery check: the actual `open_tunnel.ps1 -LocalPort 8082` was launched with the unlocked agent; loopback health through it succeeded. Only that proven temporary SSH process was stopped afterward, preserving the working 8081 tunnel. See `evidence/release/tunnel-script-check.json`. Unlock/agent startup itself is operator-specific; never store a passphrase in a helper.

## Inspect or restart the existing container

Connect with the same key/pin to `closurecall@172.234.201.174`; inspect these nonsecret values:

```bash
docker ps --format '{{.Names}} {{.Image}} {{.Status}} {{.Ports}}'
curl --fail http://127.0.0.1:8000/health
```

Confirm `closurecall-verified:e5f7801829aaa1f7cfd326e02e415f8389fa3dde` and loopback binding. The application footer/config label is supporting metadata, not independent proof of the VM/image. Never print a full container inspect or resolved Compose config because environment secrets can appear.

Check the manager desk for active work before restarting. Wait for collecting/evaluating to finish; a forced restart interrupts that evaluation and does not automatically recreate a decision. On the VM:

```bash
cd /opt/closurecall/releases/e5f7801829aaa1f7cfd326e02e415f8389fa3dde
export BUILD_COMMIT=e5f7801829aaa1f7cfd326e02e415f8389fa3dde
docker compose exec -T app python scripts/backup_db.py
docker compose restart app
docker compose ps
curl --fail http://127.0.0.1:8000/health
```

Wait for healthy before demonstrating. BUILD_COMMIT is required for subsequent Compose commands, so the existing verified tag is selected. Backups use SQLite's backup API in the persistent `/app/data/backups` directory and never overwrite an existing destination. Do not copy a live SQLite file without its journal; do not use `down -v`, prune volumes, reset the database or reseed it.

From Windows, verify the original stored demo record through the tunnel:

```powershell
.\.venv\Scripts\python.exe scripts/verify_replay.py cf6d7432-7246-49d0-96ce-cb3da56d7f89 --url http://127.0.0.1:8081
```

This read-only helper compares with its ignored baseline when present. The original hash is `ec8f0456b3a4ff15be12a815e0526ad1892d7e7f6267d49903cf3e483ccb3705`. Replay preserves original drafts, including older records without the later follow-up field. Do not repair historical content using current rules/model output.

## Code rollback if the frozen release stops working

The prior verified 75300d4 image/release remains on the VM. The prompt fix did not migrate the database schema. Review compatibility and take a fresh backup first. Code-only rollback can select that preserved image without replacing the persistent database:

```bash
cd /opt/closurecall/releases/75300d4ef4b86f8175be9f17f1fa291b00f9d7b9
export BUILD_COMMIT=75300d4ef4b86f8175be9f17f1fa291b00f9d7b9
docker compose up -d --no-build
docker compose ps
curl --fail http://127.0.0.1:8000/health
```

This code rollback is documented, not executed in production during V2. It loses the new allowed-reference prompt clarification; existing frozen records stay intact. Return to the stable release by selecting its directory/BUILD_COMMIT and the same `up -d --no-build`. Do not overwrite `.env` or rebuild untested source during a judging incident. Respect the official competition freeze; after cutoff, only recovery allowed by organizers.

Latest production backup: `/app/data/backups/closurecall-20261010T225942Z.sqlite3` (eight decisions), created before the actual 22:59:42 UTC restart. All eight full packages/export/drafts matched afterward. Earlier six-record backup `closurecall-20261010T225050Z.sqlite3` was actually restored into separate container/volume and compared after actual restart, without production credentials or source/model calls; see RESTORE_DRILL.md. The eight-record backup itself has not been restored in the drill.

If the database is damaged, preserve the volume and all backups first. Restore into a separate isolated DB/container, inspect hashes, then obtain approval before replacing original data. The retained drill container `closurecall-release-restore-v2-2252` is stopped; its network is internal. Its declared 8002 host mapping was unreachable; verified HTTP checks ran inside that container. It is not a backup browser endpoint. Never restore an old database over newer decisions to roll back code.

No public HTTP endpoint, DNS/domain, new resources or real notification send is needed for this private rehearsal. Public judge access/publication needs explicit authorization and organizer requirements.
