#!/usr/bin/env bash
# Run only after the second non-root key-authenticated session succeeds.
set -euo pipefail
[[ $(id -u) == 0 ]] || exit 2
id closurecall >/dev/null
test -s /home/closurecall/.ssh/authorized_keys
stamp=$(date -u +%Y%m%dT%H%M%SZ)
install -d -m 700 /root/closurecall-config-backups
cp -a /etc/ssh/sshd_config /root/closurecall-config-backups/sshd_config-$stamp
cp -a /etc/ssh/sshd_config.d /root/closurecall-config-backups/sshd_config.d-$stamp
target=/etc/ssh/sshd_config.d/00-closurecall-security.conf
if [[ -e "$target" ]]; then echo 'Security drop-in already exists; inspect before changing'; exit 2; fi
cat >"$target" <<'EOF'
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin prohibit-password
PubkeyAuthentication yes
X11Forwarding no
EOF
chmod 600 "$target"
sshd -t
systemctl reload ssh
ufw default deny incoming
ufw default allow outgoing
ufw limit 22/tcp comment 'Key-only SSH administration'
ufw --force enable
sshd -T | grep -E 'passwordauthentication|kbdinteractiveauthentication|permitrootlogin|pubkeyauthentication|x11forwarding'
ufw status verbose
echo 'Root key-only recovery retained; app port is not opened.'
