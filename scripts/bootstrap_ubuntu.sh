#!/usr/bin/env bash
# Reviewed bootstrap for the user's existing Ubuntu VM. No paid provisioning.
# Run only after inspecting actual server state and validating the supplied public key.
set -euo pipefail
if [[ $(id -u) != 0 ]]; then echo 'Run as an authorized root/sudo operator.'; exit 2; fi
. /etc/os-release
if [[ "$ID" != ubuntu || "$VERSION_ID" != 24.04 ]]; then echo 'Expected Ubuntu 24.04; review before proceeding.'; exit 2; fi
public_key_file=${1:?Path to the approved public key file required}
if [[ ! -f "$public_key_file" ]] || ! ssh-keygen -lf "$public_key_file" >/dev/null; then
  echo 'A valid approved public key is required.'; exit 2
fi

if ! command -v docker >/dev/null 2>&1; then
  for package in docker.io docker-compose docker-compose-v2 podman-docker containerd runc; do
    if dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q 'install ok installed'; then
      echo "Existing conflicting package $package; stop for compatibility review rather than removing it."; exit 2
    fi
  done
  apt-get update
  apt-get install -y ca-certificates curl sudo
  install -m 0755 -d /etc/apt/keyrings
  if [[ ! -e /etc/apt/keyrings/docker.asc ]]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
  fi
  if [[ ! -e /etc/apt/sources.list.d/docker.sources ]]; then
    cat >/etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
  fi
  apt-get update
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi
docker --version
docker compose version
systemctl is-active docker
docker run --rm hello-world

if ! id closurecall >/dev/null 2>&1; then
  useradd --create-home --shell /bin/bash closurecall
fi
install -d -m 700 -o closurecall -g closurecall /home/closurecall/.ssh
authorized=/home/closurecall/.ssh/authorized_keys
touch "$authorized"
if ! grep -Fqx "$(cat "$public_key_file")" "$authorized"; then cat "$public_key_file" >>"$authorized"; fi
chown closurecall:closurecall "$authorized"
chmod 600 "$authorized"
# Docker access is equivalent to root; only the authorized deployment principal gets it.
usermod -aG docker closurecall
install -d -m 750 -o closurecall -g closurecall /opt/closurecall
echo 'Bootstrap complete. Verify a second key-authenticated closurecall SSH session before any SSH/firewall restriction.'
echo 'No root login, password authentication or firewall setting was changed by this script.'
