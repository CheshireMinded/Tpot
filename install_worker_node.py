import subprocess
import os
import sys

# Step 1: Check if the script is being run as root
def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root or with sudo")
        sys.exit(1)

# Step 2: Update and upgrade the system
def update_upgrade_system():
    print("Updating and upgrading the system...")
    try:
        subprocess.run("apt update -y && apt upgrade -y", shell=True, check=True)
        print("System updated and upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating and upgrading the system: {e}")
        sys.exit(1)

# Step 3: Install Docker and Docker Compose
def install_docker_and_compose():
    print("Installing Docker...")
    try:
        subprocess.run("apt install -y docker.io", shell=True, check=True)
        subprocess.run("systemctl enable --now docker", shell=True, check=True)
        print("Docker installed successfully.")

        print("Installing Docker Compose...")
        subprocess.run(
            "curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
            shell=True, check=True)
        subprocess.run("chmod +x /usr/local/bin/docker-compose", shell=True, check=True)
        print("Docker Compose installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Docker and Docker Compose: {e}")
        sys.exit(1)

# Step 4: Allow the user to run Docker without sudo
def allow_docker_without_sudo():
    try:
        user = os.getenv("SUDO_USER")  # Get the non-root user running the script
        if user:
            print(f"Allowing {user} to run Docker without sudo...")
            subprocess.run(f"usermod -aG docker {user}", shell=True, check=True)
            print(f"User {user} has been added to the Docker group.")
        else:
            print("No SUDO_USER found. Cannot add user to Docker group.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error allowing user to run Docker without sudo: {e}")
        sys.exit(1)

# Step 5: Get the join token from the Master Node
def get_join_token():
    join_token = os.getenv('DOCKER_SWARM_JOIN_TOKEN')
    if not join_token:
        print("Error: Docker Swarm join token is not provided. Please set the DOCKER_SWARM_JOIN_TOKEN environment variable.")
        sys.exit(1)
    return join_token

# Step 6: Join the Docker Swarm
def join_swarm(join_token):
    master_node_ip = "<master-node-ip>"  # Replace with the actual Master Node IP
    print("Joining the node to Docker Swarm...")
    try:
        subprocess.run(f"docker swarm join --token {join_token} {master_node_ip}:2377", shell=True, check=True)
        print("Node successfully joined the Docker Swarm.")
    except subprocess.CalledProcessError as e:
        print(f"Error joining the node to Docker Swarm: {e}")
        sys.exit(1)

# Step 7: Verify the node has joined the swarm
def verify_swarm_join():
    print("Verifying the node has joined the swarm...")
    try:
        subprocess.run("docker node ls", shell=True, check=True)
        print("Node is successfully listed in the swarm.")
    except subprocess.CalledProcessError as e:
        print(f"Error verifying the node in the swarm: {e}")
        sys.exit(1)

# Main function
def main():
    check_root()  # Check if the script is run as root
    update_upgrade_system()  # Update and upgrade the system
    install_docker_and_compose()  # Install Docker and Docker Compose
    allow_docker_without_sudo()  # Allow the user to run Docker without sudo

    join_token = get_join_token()  # Retrieve the Docker Swarm join token
    join_swarm(join_token)  # Join the Docker Swarm
    verify_swarm_join()  # Verify the node has joined the Swarm

    print("Worker node setup complete!")

if __name__ == "__main__":
    main()

