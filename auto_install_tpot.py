import subprocess

# Step 1: Prompt for the username for T-Pot
def get_user_input():
    global NEW_USER
    NEW_USER = input("Enter the username for T-Pot (default: tpotuser): ")
    if not NEW_USER:
        NEW_USER = "tpotuser"  # Default value

# Step 2: Update and upgrade the system
def update_upgrade_system():
    try:
        print("Updating and upgrading the system...")
        subprocess.run("sudo apt update && sudo apt upgrade -y", shell=True, check=True)
        print("System updated and upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating and upgrading the system: {e}")
        exit(1)

# Step 3: Install essential packages (curl, git, wget)
def install_essential_packages():
    try:
        print("Installing essential packages (curl, git, wget)...")
        subprocess.run("sudo apt install -y curl git wget", shell=True, check=True)
        print("Essential packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        exit(1)

# Step 4: Install Docker and Docker Compose
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

# Step 5: Create a new user for T-Pot and add them to the root group
def create_user_and_group():
    try:
        print(f"Creating new user '{NEW_USER}' and adding to the root group...")
        
        # Create a new user
        subprocess.run(["sudo", "useradd", "-m", "-g", "root", NEW_USER], check=True)
        
        # Set password for the user
        subprocess.run(f"echo '{NEW_USER}:tpotpassword' | sudo chpasswd", shell=True, check=True)
        
        # Add the user to the sudo group (root group for full privileges)
        subprocess.run(f"sudo usermod -aG sudo {NEW_USER}", shell=True, check=True)
        
        # Set proper permissions for the user's home directory
        subprocess.run(f"sudo chmod 750 /home/{NEW_USER}", shell=True, check=True)
        
        print(f"User '{NEW_USER}' created successfully and added to the root group.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user and adding to root group: {e}")
        exit(1)

# Step 6: Clone the T-Pot repository
def clone_tpot_repository():
    try:
        print("Cloning T-Pot repository from GitHub...")
        
        # Switch to the user's home directory and clone the T-Pot repo
        subprocess.run(f"sudo su - {NEW_USER} -c 'cd ~ && git clone https://github.com/telekom-security/tpotce.git'", shell=True, check=True)
        
        print("T-Pot repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning T-Pot repository: {e}")
        exit(1)

# Step 7: Run the T-Pot installation script
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
    
    # Step 1: Prompt for the username
    get_user_input()

    # Step 2: Update and upgrade the system
    update_upgrade_system()

    # Step 3: Install essential packages (curl, git, wget)
    install_essential_packages()

    # Step 4: Install Docker and Docker Compose
    install_docker_and_compose()

    # Step 5: Create a new user and add to the root group
    create_user_and_group()

    # Step 6: Clone the T-Pot repository
    clone_tpot_repository()

    # Step 7: Run the T-Pot installation script
    run_tpot_installation()

    print("T-Pot setup completed successfully!")

if __name__ == "__main__":
    main()

