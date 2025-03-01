import subprocess

# Get the join token for worker nodes
def get_join_token():
    try:
        print("Getting Docker Swarm join token for worker nodes...")
        result = subprocess.run("sudo docker swarm join-token -q worker", shell=True, check=True, capture_output=True, text=True)
        join_token = result.stdout.strip()
        return join_token
    except subprocess.CalledProcessError as e:
        print(f"Error getting join token: {e}")
        exit(1)

# Check if the worker node is reachable (using netcat for port 2377)
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
    # List of worker nodes (replace with your actual worker IP addresses)
    worker_nodes = ["192.168.1.101", "192.168.1.102"]  # Example IPs for worker nodes
    
    # Get the join token for Docker Swarm
    join_token = get_join_token()
    
    # Try to add the worker nodes to the Swarm
    for worker_ip in worker_nodes:
        add_worker_node_to_swarm(worker_ip, join_token)

if __name__ == "__main__":
    main()
wr
