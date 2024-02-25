#! /bin/bash
# stop execution instantly on non-zero status. This is to know location of error
set -e

# Commands from Docker Desktop for Linux pre-config doc at:
# https://docs.docker.com/desktop/install/linux-install/#kvm-virtualization-support
# Check that the AMD kvm is working
modprobe kvm_amd

# Add current user to KVM group
sudo usermod -aG kvm $USER

echo "Please logout and log back in for user '$USER' to be added to KVM group"