#  PRIOR - join token is set as an environment variable.
# export DOCKER_SWARM_JOIN_TOKEN=<your_swarm_join_token_here>

import subprocess
import os

# Get the join token for worker nodes from the environment variable
def get_join_token():
    try:
        # Retrieve the join token from an environment variable for security
        join_token = os.getenv('DOCKER_SWARM_JOIN_TOKEN')
        if not join_token:
            raise ValueError("Join token is not set in environment variables.")
        print("Docker Swarm join token retrieved from environment variables.")
        return join_token
    except Exception as e:
        print(f"Error retrieving join token: {e}")
        exit(1)

# Discover worker nodes in the local network
def discover_worker_nodes():
    worker_nodes = []
    # Run a simple nmap scan to discover devices with port 2377 open (Docker Swarm port)
    try:
        print("Scanning for worker nodes in the network...")
        result = subprocess.run("nmap -p 2377 --open 192.168.1.0/24", shell=True, capture_output=True, text=True)
        
        # Parse the nmap output to find IPs with open port 2377
        for line in result.stdout.splitlines():
            if "Nmap scan report for" in line:
                ip = line.split()[-1]
                worker_nodes.append(ip)
        print(f"Found worker nodes: {worker_nodes}")
    except subprocess.CalledProcessError as e:
        print(f"Error during network scan: {e}")
    return worker_nodes

# Check if the worker node is reachable on port 2377 (Docker Swarm port)
def is_node_reachable(ip):
    try:
        print(f"Checking if worker node {ip} is reachable...")
        response = subprocess.run(["nc", "-zvw1", ip, "2377"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode == 0:
            print(f"Node {ip} is reachable.")
            return True
        else:
            print(f"Node {ip} is not reachable.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error checking node {ip}: {e}")
        return False

# Add worker nodes to Docker Swarm if reachable
def add_worker_node_to_swarm(worker_ip, join_token):
    try:
        if is_node_reachable(worker_ip):
            print(f"Adding worker node {worker_ip} to Docker Swarm...")
            join_command = f"sudo docker swarm join --token {join_token} {worker_ip}:2377"
            subprocess.run(join_command, shell=True, check=True)
            print(f"Worker node {worker_ip} successfully added.")
        else:
            print(f"Worker node {worker_ip} is still not available. Skipping...")
    except subprocess.CalledProcessError as e:
        print(f"Error adding worker node {worker_ip} to Swarm: {e}")
        exit(1)

# Main function
def main():
    # Discover worker nodes in the local network
    worker_nodes = discover_worker_nodes()
    
    # If no worker nodes are found, exit the script
    if not worker_nodes:
        print("No worker nodes found in the network.")
        exit(1)
    
    # Get the join token for Docker Swarm
    join_token = get_join_token()
    
    # Try to add the worker nodes to the Swarm
    for worker_ip in worker_nodes:
        add_worker_node_to_swarm(worker_ip, join_token)

if __name__ == "__main__":
    main()
