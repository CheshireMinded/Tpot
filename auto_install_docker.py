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

def install_docker_compose_plugin():
    """Install the Docker Compose plugin using apt"""
    print("Installing Docker Compose Plugin...")
    run_command("sudo apt update")
    run_command("sudo apt install -y docker-compose-plugin")
    print("Docker Compose Plugin installed successfully.")

def install_docker_compose_standalone():
    """Install the standalone Docker Compose binary"""
    print("Installing standalone Docker Compose...")
    run_command("sudo curl -L 'https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)' -o /usr/local/bin/docker-compose")
    run_command("sudo chmod +x /usr/local/bin/docker-compose")
    print("Standalone Docker Compose installed successfully.")

def check_docker_installation():
    """Check if Docker is installed"""
    print("Checking if Docker is installed...")
    try:
        subprocess.run(["docker", "-v"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Docker is installed.")
    except FileNotFoundError:
        print("Docker is not installed. Please install Docker first.")
        sys.exit(1)

def main():
    # Check if Docker is installed
    check_docker_installation()

    # Ask user for the installation preference
    choice = input("Do you want to install the Docker Compose Plugin (1) or Standalone Docker Compose (2)? Enter 1 or 2: ").strip()

    if choice == "1":
        install_docker_compose_plugin()
    elif choice == "2":
        install_docker_compose_standalone()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Verify Docker Compose installation
    try:
        result = subprocess.run(["docker", "compose", "version"], check=True, stdout=subprocess.PIPE)
        print(f"Docker Compose version: {result.stdout.decode()}")
    except subprocess.CalledProcessError:
        print("Docker Compose installation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
