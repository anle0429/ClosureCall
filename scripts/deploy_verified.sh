#!/usr/bin/env bash
# Source directory should be a freshly exported, secret-scanned verified commit.
set -euo pipefail
release=${1:?Absolute source-release directory required}
env_file=${2:?Absolute privately configured environment file required}
commit=${3:?Verified commit ID required}
case "$release" in /opt/closurecall/releases/*) ;; *) echo 'Release must be under /opt/closurecall/releases'; exit 2;; esac
if [[ ! -d "$release" || ! -f "$env_file" ]]; then echo 'Source/env missing'; exit 2; fi
if [[ "$commit" != "$(basename "$release")" ]]; then echo 'Commit/release mismatch'; exit 2; fi
cd "$release"
export BUILD_COMMIT="$commit"
if [[ -e .env && ! .env -ef "$env_file" ]]; then echo 'Existing release env differs; refusing overwrite'; exit 2; fi
if [[ ! -e .env ]]; then ln -s "$env_file" .env; fi
chmod 600 "$env_file"
docker compose config --quiet
docker build -t "closurecall-verified:$commit" .
# Verify tests inside this exact Linux image before changing the running service.
docker run --rm --user 0 --entrypoint sh -v "$release/tests:/app/tests:ro" \
  "closurecall-verified:$commit" -c 'pip install pytest==9.1.1 >/dev/null && python -m pytest /app/tests -q'
if docker compose ps --status running -q app | grep -q .; then
  docker compose exec -T app python scripts/backup_db.py
fi
docker compose up -d --no-build
docker compose ps
curl --fail --max-time 10 http://127.0.0.1:8000/health
echo 'Next: remote live source smoke + authenticated workflow, restart replay, listener/firewall verification.'
