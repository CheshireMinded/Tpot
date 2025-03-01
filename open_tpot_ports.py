# This sets up the ports required for Tpot by Telekom to work
import subprocess

# List of ports to open
ports = [
    80, 443,  # T-Pot Management
    11434,  # LLM based honeypots
    64294, 64295, 64297,  # T-Pot Management (sensor data transmission, SSH, NGINX reverse proxy)
    5555,  # ADBHoney
    22,  # Beelzebub (LLM required)
    5000,  # CiscoASA
    8443,  # CiscoASA
    443,  # CitrixHoneypot
    80, 102, 502, 1025, 2404, 10001, 44818, 47808, 50100,  # Conpot
    161, 623,  # Conpot (UDP)
    22, 23,  # Cowrie
    19, 53, 123, 1900,  # Ddospot
    11112,  # Dicompot
    21, 42, 135, 443, 445, 1433, 1723, 1883, 3306, 8081,  # Dionaea
    69,  # Dionaea (UDP)
    9200,  # Elasticpot
    22,  # Endlessh
    80, 443, 8080, 8443,  # Galah (LLM required)
    8080,  # Go-pot
    80, 443,  # H0neytr4p
    21, 22, 23, 25, 80, 110, 143, 443, 993, 995, 1080, 5432, 5900,  # Heralding
    3000,  # Honeyaml
    21, 22, 23, 25, 80, 110, 143, 389, 443, 445, 631, 1080, 1433, 1521, 3306, 3389, 5060, 5432, 5900, 6379, 6667, 8080, 9100, 9200, 11211,  # qHoneypots
    53, 123, 161, 5060,  # qHoneypots (UDP)
    631,  # IPPHoney
    80, 443, 8080, 9200, 25565,  # Log4Pot
    25,  # Mailoney
    2575,  # Medpot
    9100,  # Miniprint
    6379,  # Redishoneypot
    5060,  # SentryPeer (TCP/UDP)
    80,  # Snare (Tanner)
    8090  # Wordpot
]

# Function to open ports with ufw
def open_ports():
    for port in ports:
        try:
            print(f"Opening port {port}...")
            # Run the ufw command to allow the port
            subprocess.run(["sudo", "ufw", "allow", str(port)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to open port {port}: {e}")

# Enable ufw if it's not already enabled
def enable_ufw():
    try:
        print("Enabling ufw...")
        subprocess.run(["sudo", "ufw", "enable"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable ufw: {e}")

# Main function
def main():
    enable_ufw()
    open_ports()
    print("All necessary ports are now open.")

if __name__ == "__main__":
    main()
