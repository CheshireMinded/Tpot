import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and print output"""
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode()}")

def install_docker():
    """Install Docker"""
    print("Installing Docker...")

    # Update the apt package index
    run_command("sudo apt update")
    
    # Install the required dependencies for Docker's official repository
    run_command("sudo apt install -y apt-transport-https ca-certificates curl software-properties-common")
    
    # Add Docker's official GPG key
    run_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg")
    
    # Set up the stable Docker repository
    run_command('echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
    
    # Update the apt package index again to include Docker packages
    run_command("sudo apt update")
    
    # Install Docker
    run_command("sudo apt install -y docker-ce docker-ce-cli containerd.io")
    
    # Start Docker and enable it to run on boot
    run_command("sudo systemctl start docker")
    run_command("sudo systemctl enable docker")

    # Verify Docker installation
    print("Verifying Docker installation...")
    result = subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE)
    print(f"Docker installed: {result.stdout.decode()}")

def install_docker_compose_plugin():
    """Install Docker Compose Plugin using apt"""
    print("Installing Docker Compose Plugin...")
    run_command("sudo apt install -y docker-compose-plugin")
    print("Docker Compose Plugin installed successfully.")

def install_docker_compose_standalone():
    """Install standalone Docker Compose binary"""
    print("Installing standalone Docker Compose...")
    run_command("sudo curl -L 'https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)' -o /usr/local/bin/docker-compose")
    run_command("sudo chmod +x /usr/local/bin/docker-compose")
    print("Standalone Docker Compose installed successfully.")

def main():
    # Install Docker
    install_docker()

    # Ask user for the installation preference for Docker Compose
    choice = input("Do you want to install the Docker Compose Plugin (1) or Standalone Docker Compose (2)? Enter 1 or 2: ").strip()

    if choice == "1":
        install_docker_compose_plugin()
    elif choice == "2":
        install_docker_compose_standalone()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Verify Docker Compose installation
    print("Verifying Docker Compose installation...")
    try:
        result = subprocess.run(["docker", "compose", "version"], check=True, stdout=subprocess.PIPE)
        print(f"Docker Compose version: {result.stdout.decode()}")
    except subprocess.CalledProcessError:
        print("Docker Compose installation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()

