import yaml
from datetime import datetime

version = """
 ____  [T-Pot]         _            ____        _ _     _
/ ___|  ___ _ ____   _(_) ___ ___  | __ ) _   _(_) | __| | ___ _ __
\___ \ / _ \ '__\ \ / / |/ __/ _ \ |  _ \| | | | | |/ _` |/ _ \ '__|
 ___) |  __/ |   \ V /| | (_|  __/ | |_) | |_| | | | (_| |  __/ |
|____/ \___|_|    \_/ |_|\___\___| |____/ \__,_|_|_|\__,_|\___|_| v0.21
"""

header = """# T-Pot: CUSTOM EDITION, edited from https://github.com/telekom-security/tpotce/blob/master/compose/customizer.py to include deployments for docker swarm
# Generated on: {current_date}
"""

config_filename = "tpot_services.yml"
service_filename = "docker-compose-custom.yml"

# A list of all available honeypots in T-Pot
all_honeypots = [
    "cowrie", "dionaea", "elasticpot", "honeytrap", "glutton", "miniprint",
    "tanner", "wordpot", "conpot", "adbhoney", "beelzebub", "ciscoasa",
    "citrixhoneypot", "ddospot", "dicompot", "endlessh", "go-pot", "galah",
    "hellpot", "heralding", "honeyaml", "honeypots", "ipphoney", "log4pot",
    "mailoney", "medpot", "redishoneypot", "sentrypeer", "snare", "tanner_redis"
]

# A dictionary to store port mappings for each honeypot
honeypot_ports = {
    "cowrie": ["2222:2222"],
    "dionaea": ["445:445", "21:21"],
    "elasticpot": ["9200:9200"],
    "honeytrap": ["25:25", "110:110"],
    "glutton": ["80:80", "443:443"],
    "miniprint": ["9100:9100"],
    "tanner": ["80:80"],
    "wordpot": ["8090:8090"],
    "conpot": ["80:80", "443:443", "8080:8080"],
    "adbhoney": ["5555:5555"],
    "beelzebub": ["80:80"],
    "ciscoasa": ["443:443"],
    "citrixhoneypot": ["443:443"],
    "ddospot": ["53:53", "123:123"],
    "dicompot": ["11112:11112"],
    "endlessh": ["22:22"],
    "go-pot": ["8080:8080"],
    "galah": ["80:80", "443:443"],
    "hellpot": ["80:80"],
    "heralding": ["25:25", "110:110", "443:443"],
    "honeyaml": ["3000:3000"],
    "honeypots": ["8080:8080"],
    "ipphoney": ["631:631"],
    "log4pot": ["80:80", "443:443"],
    "mailoney": ["25:25"],
    "medpot": ["2575:2575"],
    "redishoneypot": ["6379:6379"],
    "sentrypeer": ["5060:5060"],
    "snare": ["80:80"],
    "tanner_redis": ["6379:6379"]
}

def load_config(filename):
    try:
        with open(filename, 'r') as file:
            config = yaml.safe_load(file)
    except:
        print_color(f"Error: {filename} not found. Exiting.", "red")
        exit()
    return config

def prompt_service_include(service_name):
    """Ask if the user wants to include a service."""
    while True:
        try:
            response = input(f"Include {service_name}? (y/n): ").strip().lower()
            if response in ['y', 'n']:
                return response == 'y'
            else:
                print_color("Please enter 'y' for yes or 'n' for no.", "red")
        except KeyboardInterrupt:
            print()
            print_color("Interrupted by user. Exiting.", "red")
            print()
            exit()

def get_replica_count(service_name):
    """Ask the user for the number of replicas to deploy for a given service."""
    while True:
        try:
            response = input(f"How many replicas of {service_name} do you want to deploy? ")
            replicas = int(response)
            if replicas > 0:
                return replicas
            else:
                print_color("Please enter a positive number for replicas.", "red")
        except ValueError:
            print_color("Invalid input. Please enter a valid number.", "red")

def check_port_conflicts(selected_services):
    """Check for port conflicts among selected services."""
    all_ports = {}
    conflict_ports = []

    for service_name, config in selected_services.items():
        ports = config.get('ports', [])
        for port in ports:
            parts = port.split(':')
            host_port = parts[1] if len(parts) == 3 else (parts[0] if parts[1].isdigit() else parts[1])

            if host_port in all_ports:
                conflict_ports.append((service_name, host_port))
                if all_ports[host_port] not in [service for service, _ in conflict_ports]:
                    conflict_ports.append((all_ports[host_port], host_port))
            else:
                all_ports[host_port] = service_name

    if conflict_ports:
        print_color("[WARNING] - Port conflict(s) detected:", "red")
        for service, port in conflict_ports:
            print_color(f"{service}: {port}", "red")
        return True
    return False

def enforce_dependencies(selected_services, services):
    """Enforce dependencies based on service selection."""
    tanner_services = {'snare', 'tanner', 'tanner_redis', 'tanner_phpox', 'tanner_api'}
    if tanner_services.intersection(selected_services):
        print_color("[OK] - For Snare / Tanner to work all required services have been added to your configuration.", "green")
        for service in tanner_services:
            selected_services[service] = services[service]

    if 'kibana' in selected_services:
        selected_services['elasticsearch'] = services['elasticsearch']
        print_color("[OK] - Kibana requires Elasticsearch which has been added to your configuration.", "green")

    if 'spiderfoot' in selected_services:
        selected_services['nginx'] = services['nginx']
        print_color("[OK] - Spiderfoot requires Nginx which has been added to your configuration.","green")

    map_services = {'map_web', 'map_redis', 'map_data'}
    if map_services.intersection(selected_services):
        print_color("[OK] - For AttackMap to work all required services have been added to your configuration.", "green")
        for service in map_services.union({'elasticsearch', 'nginx'}):
            selected_services[service] = services[service]

    if 'honeytrap' in selected_services and 'glutton' in selected_services:
        del selected_services['glutton']
        print_color("[OK] - Honeytrap and Glutton cannot be active at the same time. Glutton has been removed from your configuration.","green")

def remove_unused_networks(selected_services, services, networks):
    """Remove unused networks from the configuration."""
    used_networks = set()
    for service_name in selected_services:
        service_config = services[service_name]
        if 'networks' in service_config:
            for network in service_config['networks']:
                used_networks.add(network)

    for network in list(networks):
        if network not in used_networks:
            del networks[network]

def print_color(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "end": "\033[0m",
    }
    print(f"{colors[color]}{text}{colors['end']}")

def main():
    config = load_config(config_filename)

    services = config['services']
    networks = config.get('networks', {})
    selected_services = {'tpotinit': services['tpotinit'], 'logstash': services['logstash']}  # Always include tpotinit and logstash

    for service_name in all_honeypots:
        if service_name not in selected_services:  # Skip already included services
            if prompt_service_include(service_name):
                selected_services[service_name] = services.get(service_name, {})
                replicas = get_replica_count(service_name)
                selected_services[service_name]['deploy'] = {'replicas': replicas}
                selected_services[service_name]['ports'] = honeypot_ports.get(service_name, [])

    enforce_dependencies(selected_services, services)
    remove_unused_networks(selected_services, services, networks)

    output_config = {
        'networks': networks,
        'services': selected_services,
    }

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(service_filename, 'w') as file:
        file.write(header.format(current_date=current_date))
        yaml.dump(output_config, file, default_flow_style=False, sort_keys=False, indent=2)

    if check_port_conflicts(selected_services):
        print_color(f"[WARNING] - Adjust the conflicting ports in the {service_filename} or re-run the script and select services that do not occupy the same port(s).", "red")
    else:
        print_color(f"[OK] - Custom {service_filename} has been generated without port conflicts.", "green")
    print_color(f"Copy {service_filename} to ~/tpotce and test with: docker compose -f {service_filename} up", "blue")
    print_color(f"If everything works, exit with CTRL-C and replace docker-compose.yml with the new config.", "blue")

if __name__ == "__main__":
    print_color(version, "magenta")
    main()

