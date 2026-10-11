# Private demo access and recovery

## Latest work-hours release — verified 2026-10-11 UTC

Current application source **a5681bcd98400fd75d02670f378a04365459dd7e**, image `sha256:9ab42b0dcdfaee241b3d9156ac5433ecd0da772f29707ec6cb397664f0256b90`, directory `/opt/closurecall/releases/a5681bcd98400fd75d02670f378a04365459dd7e`. Main private address remains **http://127.0.0.1:8081/**; tunnel/manager credentials unchanged. The main form is open with **Refresh time (+15 min)**. Click it when the work hours have aged, then explicitly Check conditions for a new evaluation; it does not fetch sources or change historical records itself.

Latest pre-cutover backup `/app/data/backups/closurecall-20261011T114549Z.sqlite3`; all nine original decision packages and six table fingerprints unchanged afterward. Current container verified healthy with loopback-only binding. For current inspection/restart use the latest directory and `export BUILD_COMMIT=a5681bcd98400fd75d02670f378a04365459dd7e`, following the no-active-run/fresh-backup safeguards below. The retained 4dffaac release is the immediate code-only fallback (same env/volume); select its directory/BUILD_COMMIT and `docker compose up -d --no-build` without restoring old data. This rollback was not executed. Existing older e5f7801 remains retained too. See [refresh release](WORK_HOURS_REFRESH.md).

The earlier section below remains useful for opening the unchanged pinned tunnel and describes the prior precision release.

## Current private release — verified 2026-10-11 UTC

Use **http://127.0.0.1:8081/** on the presentation laptop. The verified release is `4dffaac63f06b57bd97e2af17140ff850be147e5`, image `sha256:d580f299413bb9598750ab259502f1f96351d9078ae77fdc924acf6da3317a41`; source directory `/opt/closurecall/releases/4dffaac63f06b57bd97e2af17140ff850be147e5`. Existing env `/opt/closurecall/config/.env` and volume `closurecall_closurecall-data` remain intact. Application is private loopback only; no public endpoint/domain is needed. 8084 is a separate QA preview, not the main demo.

The main tab is already signed in and shows an original saved decision as **REPLAY**. Click **2 Review conditions** for the original evidence/recommendation/manager reason; **4 Check employee drafts** for the roster. For a fresh LIVE run, return to work hours, choose the actual facility and upcoming period in its timezone, and check the explicitly synthetic special-shift box for Sunday. Do not evaluate using the old replay dates. Do not call the saved Flood Watch current weather. Latest isolated remote KC check returned zero alerts; never move the site silently to manufacture a result.

The updated `scripts/open_tunnel.ps1` prefers Windows OpenSSH and was actually used to open 8081. Keep the running tunnel. If it has closed, unlock the existing key in a terminal you control, then run the helper:

```powershell
& 'C:\Windows\System32\OpenSSH\ssh-add.exe' 'C:\Users\thien\.ssh\closurecall_akamai'
Set-Location -LiteralPath C:\Projects\ClosureCall
.\scripts\open_tunnel.ps1
```

Enter the passphrase only at the terminal prompt. The existing Windows ssh-agent is running at this checkpoint; if the service is stopped, starting it may require an administrator terminal. Never store the passphrase or disable host verification. An occupied 8081 makes the helper refuse to start another forward. Browser reload requires manager sign-in again; use credentials from the existing ignored env privately and keep them off the projected screen.

At the actual 11:26:02 UTC cutover, the fresh backup was `/app/data/backups/closurecall-20261011T112601Z.sqlite3`. All 9 original historical packages and all six table fingerprints matched after restart (2 facilities / 13 runs / 9 decisions / 9 outbox). This backup was not restored into the original DB. `evidence/precision-release` contains the current checks.

For inspection/restart, use the existing pinned key and `closurecall` deploy user. In the **current** release directory:

```bash
cd /opt/closurecall/releases/4dffaac63f06b57bd97e2af17140ff850be147e5
export BUILD_COMMIT=4dffaac63f06b57bd97e2af17140ff850be147e5
docker compose ps
curl --fail http://127.0.0.1:8000/health
# Only after checking no evaluation is active and taking a fresh backup:
docker compose exec -T app python scripts/backup_db.py
docker compose restart app
```

Prior stable **e5f7801** source/image remains available. If a code-only rollback is needed, take a fresh current-data backup first, then select it without rebuilding or replacing the volume:

```bash
cd /opt/closurecall/releases/e5f7801829aaa1f7cfd326e02e415f8389fa3dde
export BUILD_COMMIT=e5f7801829aaa1f7cfd326e02e415f8389fa3dde
docker compose up -d --no-build
docker compose ps
curl --fail http://127.0.0.1:8000/health
```

That rollback is documented, not executed in this release. It removes the newer design/feedback behavior but retains current historical data. Never use `down -v`, reseed, overwrite `.env` or restore an older DB over later decisions. Database recovery requires preserving the original volume, verifying a restore in isolation, then approval before any original-data replacement.

## Earlier V2 recovery checkpoint — historical reference

The following e5f7801/75300d4 commands and eight-record backup describe the earlier checkpoint. Use the current section above for this release.

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
