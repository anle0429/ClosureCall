# Separate-container backup restore

Executed 2026-10-10 22:52–22:54 UTC on the existing authorized host. Result: VERIFIED for the scope below, not a production recovery execution.

- Backup: `/app/data/backups/closurecall-20261010T225050Z.sqlite3`, copied read-only from production into `/opt/closurecall/restore-drills/v2-20261010T2252/restored-source.sqlite3`. SHA-256 `3131e3b36c7407054bce0d7cbfe698dd6563dfdf86faff9fd4889700f1a348f6`.
- Exact candidate: `e5f7801829aaa1f7cfd326e02e415f8389fa3dde`, image `sha256:11bddbc767275d8af7d603511596cc432b5862fe07fd880d5404fac8d13f7184`.
- Container, volume and internal network: `closurecall-release-restore-v2-2252`, all distinct from production `closurecall-app-1` / `closurecall_closurecall-data`. No production data mount. Network inspection confirmed `Internal=true`; no provider credentials. A random test-only manager credential is in private `test.env`, never logged/committed.
- Appuser, read-only root, dropped capabilities, no-new-privileges; declared host mapping `127.0.0.1:8002`. The internal network did **not** make that host-published port reachable in this Docker setup. Actual Uvicorn HTTP was tested from inside the isolated container at `127.0.0.1:8000`; this is not a verified host-browser restore endpoint.
- Actual HTTP health, six historical replay/export/outbox bundles, authenticated business reads, schema and SQLite integrity checked. `PRAGMA integrity_check=ok`.
- Changed current rules/version and roster bindings in the separate verification process, never frozen records. Call traps for NWS/AQ/model/assessment/routing remained zero. Two ASGI lifespan cycles matched all six full bundles. Then **actual container restart**, another actual Uvicorn HTTP comparison and another two lifespan cycles matched all six.
- Initial harness tried `docker cp` into the read-only root and failed. Corrected harness streams verification code and baseline through `docker exec -i`, writing baseline only to `/tmp` tmpfs. No security setting was relaxed. No application bug was indicated.
- Production six original bundles remained exact after the drill; two new synthetic decisions were later added deliberately by browser rehearsal, then all eight survived production restart unchanged.
- Drill container stopped after checks; separate volume/network/private drill files retained for inspection. No prune, production replacement or original backup deletion.

Evidence: `evidence/release/restore-verified.txt`, `restore-restarted.txt`, before/after JSON checks and `final-restart-runtime.txt`. The drill restores the six-record pre-deploy backup; it does not claim to have restored the later eight-record backup.

Executed verification transport (VM):

```bash
docker exec -i closurecall-release-restore-v2-2252 python -c 'import sys;from pathlib import Path;Path("/tmp/baselines.json").write_text(sys.stdin.read())' < /opt/closurecall/release-restore-baselines.json
docker exec -i closurecall-release-restore-v2-2252 python - < /opt/closurecall/release-restore-verify.py
```

These commands require the retained drill container to be started first. They are not instructions to replace production data. Original backups and both verified production images remain available.
