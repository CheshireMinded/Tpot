#!/bin/bash

# Check if the script is being run as root
if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root or with sudo"
  exit 1
fi

# Step 1: Update and upgrade the system
echo "Updating and upgrading the system..."
apt update -y && apt upgrade -y

# Step 2: Install Docker and Docker Compose
echo "Installing Docker..."
apt install -y docker.io

# Enable Docker to start on boot
systemctl enable --now docker

echo "Installing Docker Compose..."
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Step 3: Allow the user to run Docker without sudo
echo "Allowing non-root user to run Docker..."
usermod -aG docker $SUDO_USER

# Step 4: Get the join token from the Master Node
# (This assumes the token is provided as an argument to the script or set via environment variable)

if [ -z "$DOCKER_SWARM_JOIN_TOKEN" ]; then
  echo "Error: Docker Swarm join token is not provided. Please set the DOCKER_SWARM_JOIN_TOKEN environment variable."
  exit 1
fi

echo "Joining the node to Docker Swarm..."
docker swarm join --token $DOCKER_SWARM_JOIN_TOKEN <master-node-ip>:2377

# Step 5: Verify the node has joined the swarm
echo "Verifying the node has joined the swarm..."
docker node ls

echo "Worker node setup complete!"
