#!/bin/bash

# ==========================
# Sanitize VM for OpenStack Horizon
# This is how you can (FIRST) create a COMPLETE clone of your vm in vmware and THEN make an instance for OpenStack Horizon
# ==========================

echo "🔧 Starting VM cleanup..."

# 1. Set hostname to a generic name
echo "🔹 Resetting hostname..."
sudo hostnamectl set-hostname localhost

# 2. Remove persistent net rules (MAC-related)
echo "🔹 Removing persistent network rules..."
sudo rm -f /etc/udev/rules.d/70-persistent-net.rules

# 3. Clean network configs (Ubuntu / Debian)
echo "🔹 Setting DHCP in Netplan..."
if ls /etc/netplan/*.yaml 1> /dev/null 2>&1; then
    sudo sed -i 's/static/dhcp/g' /etc/netplan/*.yaml
    sudo sed -i '/addresses:/d' /etc/netplan/*.yaml
    sudo sed -i '/gateway/d' /etc/netplan/*.yaml
    sudo sed -i '/nameservers:/,+2d' /etc/netplan/*.yaml
    sudo netplan generate
fi

# 4. Clean SSH host keys
echo "🔹 Removing SSH host keys..."
sudo rm -f /etc/ssh/ssh_host_*

# 5. Remove logs
echo "🔹 Cleaning logs..."
sudo rm -rf /var/log/*

# 6. Clear bash history for all users
echo "🔹 Clearing shell history..."
unset HISTFILE
history -c
sudo rm -f /root/.bash_history
sudo rm -f ~/.bash_history

# 7. Remove cloud-init instance data if re-imaging
echo "🔹 Resetting cloud-init (if installed)..."
sudo cloud-init clean --logs || echo "cloud-init not installed or failed to reset"

# 8. Suggest installing cloud-init if it's missing
if ! command -v cloud-init &> /dev/null; then
    echo "❗ cloud-init not installed. Installing it now..."
    sudo apt update && sudo apt install -y cloud-init
fi

echo "✅ Cleanup complete. You can now power off the VM."

# ===============================
# NOTE TO SELF:
# Make it executable:
#   chmod +x sanitize-for-openstack.sh
# Run it:
#    ./sanitize-for-openstack.sh
# Shutdown the VM:
#    sudo poweroff
# You still need to do this step
# Convert the clone to QCOW2
# From your Linux box or WSL:
#
#     qemu-img convert -f vmdk -O qcow2 CloneVM.vmdk CleanImage.qcow2
#
# ===============================
