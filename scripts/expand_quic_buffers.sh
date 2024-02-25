#! /bin/bash
# stop execution instantly on non-zero status. This is to know location of error
set -e

# Cloudflared tunnel requires some adjustments to default memory settings
# https://github.com/quic-go/quic-go/wiki/UDP-Buffer-Sizes

if [[ $EUID -ne 0 ]]; then
  YELLOW='\033[0;93m'
  NO_COLOR='\033[0m'
  echo -e "${YELLOW}[WARNING]${NO_COLOR} script must be run as root"
  exit 1
fi

sysctl -w net.core.rmem_max=2500000
sysctl -w net.core.wmem_max=2500000