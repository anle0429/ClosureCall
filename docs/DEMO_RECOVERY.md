# Private access and recovery

Running source: **a5681bcd98400fd75d02670f378a04365459dd7e**. Image: `sha256:9ab42b0dcdfaee241b3d9156ac5433ecd0da772f29707ec6cb397664f0256b90`. Fresh read-only observations on October 12 confirmed healthy/non-root/read-only/loopback and the original 2026-10-11T11:45:50Z start. Candidate **3bc1ddd is not deployed**. [Manifest](../RELEASE_MANIFEST.json), [verification](VERIFICATION.md).

## Open the existing operator tunnel

Run in a PowerShell terminal you control:

```powershell
Set-Location -LiteralPath C:\Projects\ClosureCall
.\scripts\open_tunnel.ps1
```

Open `http://127.0.0.1:8081/`. The helper uses the existing encrypted key, strict pinned host verification and loopback forwarding. Enter a passphrase only at the terminal prompt. Never store it in commands, files or chat. The operator can use `ssh-add` with the existing key when ssh-agent is available; starting that service may require administrator rights.

An occupied port makes the helper refuse a duplicate tunnel. Keep a valid existing tunnel; do not kill unrelated processes. Use `-LocalPort 8082` where appropriate. Preserve the ignored known-host pin; a missing/changed pin requires trusted fingerprint verification. The tunnel was stopped at R0 and has not been reopened in this pass; historical helper verification is retained, not a fresh test. Browser reload requires sign-in again.

8084 is a separate local QA server with a copied database and blocked providers. It is not Linode or a public URL. Preserve original QA/env/DB when restarting the isolated portfolio preview.

## Production inspection and approved rollback

Current release directory: `/opt/closurecall/releases/a5681bcd98400fd75d02670f378a04365459dd7e`. Environment and persistent data remain separate. Inspect selected health/image/start/port fields, never full environment/config output. Before an approved restart, wait for active evaluations and take a fresh SQLite backup. A new deploy/restart needs specific approval.

Earlier `4dffaac` and `e5f7801` source/images are retained code fallbacks. An approved code-only rollback can select a preserved image using its exact BUILD_COMMIT and `docker compose up -d --no-build` in its release directory after backup/compatibility review. This pass did not execute production rollback. Never use `down -v`, reseed, reset, replace `.env`, or restore old data over later decisions.

## Isolated backup restore

Existing backup `/app/data/backups/closurecall-20261011T114549Z.sqlite3`, SHA-256 `608ef3c847cc227e10e421f8f170e5061c0ed879d767992ed1f45fba0850a003`, was copied into a separate volume and opened with exact candidate image `5fdf4901...`. No external network, published port or inference key. All nine replay/export/outbox/memo records matched before/after an actual QA restart, with in-memory current rule/roster changes and zero recomputation traps. QA containers stopped afterward. Production was untouched. [Drill evidence](../evidence/portfolio/restore-final-verified.txt).

The first attempt to copy a verifier into a read-only container was refused. The corrected attempt mounted files read-only at startup; protections remained enabled. [Initial log](../evidence/portfolio/restore-final.txt).

Original-data replacement remains destructive and requires approval, preservation of the original volume and independent validation. A successful drill is not permission to replace current data. [Historical operator evidence](archive/hackathon/README.md).
