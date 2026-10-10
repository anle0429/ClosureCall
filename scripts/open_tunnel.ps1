# Foreground operator command: enter the SSH key passphrase in your terminal if prompted.
# Existing Git ssh-agent users may set SSH_AUTH_SOCK before invoking this script.
param([int]$LocalPort=8081)
$projectRoot=Split-Path $PSScriptRoot -Parent
$knownHosts=Join-Path $projectRoot 'data/deployment_known_hosts'
if (!(Test-Path -LiteralPath $knownHosts)) { throw 'Pinned known-host file missing; verify host identity before connecting.' }
if (Get-NetTCPConnection -LocalPort $LocalPort -State Listen -ErrorAction SilentlyContinue) { throw 'Local tunnel port is already occupied; preserve the existing process.' }
& 'C:\Program Files\Git\usr\bin\ssh.exe' -N -i "$env:USERPROFILE/.ssh/closurecall_akamai" -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o "UserKnownHostsFile=$knownHosts" -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -L "127.0.0.1:${LocalPort}:127.0.0.1:8000" closurecall@172.234.201.174
exit $LASTEXITCODE
