import subprocess
import os

# Define the username and group for the T-Pot installation
NEW_USER = "tpotuser"
NEW_GROUP = "tpotgroup"

# Step 1: Create a new user and group for T-Pot
def create_user_and_group():
    try:
        print("Creating new user and group for T-Pot...")
        
        # Create a new group for T-Pot
        subprocess.run(["sudo", "groupadd", NEW_GROUP], check=True)
        
        # Create a new user with the group and set password
        subprocess.run(["sudo", "useradd", "-m", "-g", NEW_GROUP, NEW_USER], check=True)
        
        # Set a password for the user
        subprocess.run(f"echo '{NEW_USER}:tpotpassword' | sudo chpasswd", shell=True, check=True)

        # Set the proper permissions for the user's home directory
        subprocess.run(f"sudo chmod 750 /home/{NEW_USER}", shell=True, check=True)
        
        # Add the user to sudo group to give it necessary permissions
        subprocess.run(f"sudo usermod -aG sudo {NEW_USER}", shell=True, check=True)
        
        print(f"User '{NEW_USER}' created successfully with the proper permissions.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user and group: {e}")
        exit(1)

# Step 2: Install Docker and Docker Compose
def install_docker_and_compose():
    try:
        print("Installing Docker and Docker Compose...")
        
        # Update and install required packages
        subprocess.run("sudo apt update && sudo apt upgrade -y", shell=True, check=True)
        subprocess.run("sudo apt install -y apt-transport-https ca-certificates curl software-properties-common", shell=True, check=True)
        
        # Add Docker's official GPG key
        subprocess.run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -", shell=True, check=True)
        
        # Set up Docker's stable repository
        subprocess.run("sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"", shell=True, check=True)
        
        # Install Docker
        subprocess.run("sudo apt update", shell=True, check=True)
        subprocess.run("sudo apt install -y docker-ce", shell=True, check=True)
        
        # Install Docker Compose
        subprocess.run("sudo curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose", shell=True, check=True)
        subprocess.run("sudo chmod +x /usr/local/bin/docker-compose", shell=True, check=True)
        
        # Enable Docker to start on boot
        subprocess.run("sudo systemctl enable --now docker", shell=True, check=True)

        print("Docker and Docker Compose installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Docker and Docker Compose: {e}")
        exit(1)

# Step 3: Clone the T-Pot repository
def clone_tpot_repository():
    try:
        print("Cloning T-Pot repository...")
        
        # Switch to the user's home directory
        subprocess.run(f"sudo su - {NEW_USER} -c 'cd ~ && git clone https://github.com/telekom-security/tpotce.git'", shell=True, check=True)
        
        print("T-Pot repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning T-Pot repository: {e}")
        exit(1)

# Step 4: Run the T-Pot installation script
def run_tpot_installation():
    try:
        print("Running T-Pot installation script...")
        
        # Run the install script as the new user
        subprocess.run(f"sudo su - {NEW_USER} -c 'cd ~/tpotce && ./install.sh'", shell=True, check=True)
        
        print("T-Pot installation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running T-Pot installation: {e}")
        exit(1)

# Main function to execute all setup steps
def main():
    print("Starting T-Pot installation process...")

    # Step 1: Create a new user and group for T-Pot
    create_user_and_group()

    # Step 2: Install Docker and Docker Compose
    install_docker_and_compose()

    # Step 3: Clone the T-Pot repository
    clone_tpot_repository()

    # Step 4: Run the T-Pot installation script
    run_tpot_installation()

    print("T-Pot setup completed successfully!")

if __name__ == "__main__":
    main()
