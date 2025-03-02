
# update the master node and worker node ip's to your actual ip addresses

import subprocess
import os
import paramiko  # For SSH connection to worker nodes

# Function to check if a node is reachable on port 2377 (Docker Swarm port)
def is_node_reachable(ip):
    try:
        response = subprocess.run(
            ["nc", "-zvw1", ip, "2377"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return response.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error checking node {ip}: {e}")
        return False

# Function to automatically join the Swarm (if a new node is found)
def join_swarm(worker_ip, join_token, master_node_ip):
    try:
        print(f"Attempting to add node {worker_ip} to the Swarm...")
        # SSH into the worker node and join the swarm
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(worker_ip, username="your-username", password="your-password")  # Provide SSH details
        command = f"docker swarm join --token {join_token} {master_node_ip}:2377"
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Output any errors or results from the command
        result = stdout.read().decode()
        error = stderr.read().decode()

        if result:
            print(f"Output: {result}")
        if error:
            print(f"Error: {error}")
        
        ssh.close()
        print(f"Node {worker_ip} successfully added to the Swarm.")
        
        # Apply iptables rules after joining the swarm
        apply_iptables_rules(worker_ip, master_node_ip)

    except Exception as e:
        print(f"Error joining the swarm for node {worker_ip}: {e}")

# Function to apply iptables rules to worker node
def apply_iptables_rules(worker_ip, master_node_ip):
    try:
        print(f"Applying iptables rules on {worker_ip}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(worker_ip, username="your-username", password="your-password")  # Provide SSH details
        
        # Define iptables rules
        rules = [
            f"sudo iptables -A INPUT -p tcp --dport 2377 -s {master_node_ip} -j ACCEPT",  # Port 2377 for master node
            f"sudo iptables -A INPUT -p tcp --dport 7946 -s <swarm-node-ip-range> -j ACCEPT",  # Port 7946 for internal communication
            f"sudo iptables -A INPUT -p udp --dport 7946 -s <swarm-node-ip-range> -j ACCEPT",  # Port 7946 UDP for internal communication
            f"sudo iptables -A INPUT -p udp --dport 4789 -s <swarm-node-ip-range> -j ACCEPT",  # Port 4789 UDP for overlay network
            "sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT",  # HTTP port
            "sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT",  # HTTPS port
            "sudo iptables -A INPUT -j DROP",  # Drop all other incoming traffic
        ]
        
        for rule in rules:
            stdin, stdout, stderr = ssh.exec_command(rule)
            result = stdout.read().decode()
            error = stderr.read().decode()
            if result:
                print(f"Output: {result}")
            if error:
                print(f"Error: {error}")
        
        print(f"iptables rules applied successfully on {worker_ip}")
        ssh.close()

    except Exception as e:
        print(f"Error applying iptables rules on node {worker_ip}: {e}")

# Function to retrieve the Swarm join token dynamically
def get_join_token():
    try:
        # Retrieve the join token using the 'docker swarm join-token' command on the Master Node
        result = subprocess.run(
            "sudo docker swarm join-token worker -q", 
            shell=True, capture_output=True, text=True, check=True
        )
        join_token = result.stdout.strip()
        
        if not join_token:
            print("Error: Could not retrieve the join token.")
            exit(1)
        return join_token
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving join token: {e}")
        exit(1)

# Main function
def main():
    # Define the master node's IP and the range of worker nodes
    master_node_ip = "192.168.1.1"  # Replace with actual master node IP
    worker_nodes = ["192.168.1.101", "192.168.1.102"]  # Example worker IPs

    join_token = get_join_token()

    # Loop over worker nodes to check if they are reachable
    for worker_ip in worker_nodes:
        if is_node_reachable(worker_ip):
            print(f"Worker node {worker_ip} is reachable. Adding to Swarm.")
            join_swarm(worker_ip, join_token, master_node_ip)
        else:
            print(f"Worker node {worker_ip} is not reachable. Skipping.")

if __name__ == "__main__":
    main()

