import subprocess

# Define the username and group for the T-Pot installation
NEW_USER = "tpotuser"
NEW_GROUP = "tpotgroup"

# Step 1: Update and upgrade the system
def update_upgrade_system():
    try:
        print("Updating and upgrading the system...")
        subprocess.run("sudo apt update && sudo apt upgrade -y", shell=True, check=True)
        print("System updated and upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating and upgrading the system: {e}")
        exit(1)

# Step 2: Install essential packages (curl, git, wget)
def install_essential_packages():
    try:
        print("Installing essential packages (curl, git, wget)...")
        subprocess.run("sudo apt install -y curl git wget", shell=True, check=True)
        print("Essential packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        exit(1)

# Step 3: Install Docker and Docker Compose
def install_docker_and_compose():
    try:
        print("Installing Docker and Docker Compose...")
        
        # Install Docker
        subprocess.run("sudo apt install -y docker.io", shell=True, check=True)
        
        # Install Docker Compose
        subprocess.run("sudo curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose", shell=True, check=True)
        subprocess.run("sudo chmod +x /usr/local/bin/docker-compose", shell=True, check=True)
        
        # Enable Docker service
        subprocess.run("sudo systemctl enable --now docker", shell=True, check=True)
        
        print("Docker and Docker Compose installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Docker and Docker Compose: {e}")
        exit(1)

# Step 4: Create a new user and group for T-Pot
def create_user_and_group():
    try:
        print(f"Creating new user and group for T-Pot...")
        
        # Create a new group
        subprocess.run(["sudo", "groupadd", NEW_GROUP], check=True)
        
        # Create a new user and add to the group
        subprocess.run(["sudo", "useradd", "-m", "-g", NEW_GROUP, NEW_USER], check=True)
        
        # Set password for the user
        subprocess.run(f"echo '{NEW_USER}:tpotpassword' | sudo chpasswd", shell=True, check=True)
        
        # Add the user to sudo group to grant admin privileges
        subprocess.run(f"sudo usermod -aG sudo {NEW_USER}", shell=True, check=True)
        
        # Set proper permissions for the user's home directory
        subprocess.run(f"sudo chmod 750 /home/{NEW_USER}", shell=True, check=True)
        
        print(f"User '{NEW_USER}' created successfully with necessary permissions.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user and group: {e}")
        exit(1)

# Step 5: Clone the T-Pot repository
def clone_tpot_repository():
    try:
        print("Cloning T-Pot repository from GitHub...")
        
        # Switch to the user's home directory and clone the T-Pot repo
        subprocess.run(f"sudo su - {NEW_USER} -c 'cd ~ && git clone https://github.com/telekom-security/tpotce.git'", shell=True, check=True)
        
        print("T-Pot repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning T-Pot repository: {e}")
        exit(1)

# Step 6: Run the T-Pot installation script
def run_tpot_installation():
    try:
        print("Running T-Pot installation script...")
        
        # Run the installation script as the new user
        subprocess.run(f"sudo su - {NEW_USER} -c 'cd ~/tpotce && ./install.sh'", shell=True, check=True)
        
        print("T-Pot installation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running T-Pot installation: {e}")
        exit(1)

# Main function to execute all setup steps
def main():
    print("Starting T-Pot installation process...")

    # Step 1: Update and upgrade the system
    update_upgrade_system()

    # Step 2: Install essential packages (curl, git, wget)
    install_essential_packages()

    # Step 3: Install Docker and Docker Compose
    install_docker_and_compose()

    # Step 4: Create a new user and group for T-Pot
    create_user_and_group()

    # Step 5: Clone the T-Pot repository
    clone_tpot_repository()

    # Step 6: Run the T-Pot installation script
    run_tpot_installation()

    print("T-Pot setup completed successfully!")

if __name__ == "__main__":
    main()

