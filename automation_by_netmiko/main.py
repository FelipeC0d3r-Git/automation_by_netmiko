# main.py
import json
from netmiko import ConnectHandler
from getpass import getpass
from commands import commands_groups
import os

# Carregar o arquivo hosts_by_client.json
script_dir = os.path.dirname(os.path.abspath(__file__))
hosts_file = os.path.join(script_dir, "hosts_by_client.json")

with open(hosts_file, encoding="utf-8") as f:
    hosts_by_client = json.load(f)

# Variáveis globais para armazenar nome de usuário e senha
global_username = None
global_password = None

def get_user_credentials():
    global global_username, global_password
    if global_username is None or global_password is None:
        # Solicitar nome de usuário e senha
        global_username = input("Digite o seu nome de usuário: ")
        global_password = getpass("Digite a sua senha: ")
    return global_username, global_password

def select_client():
    while True:
        print("Selecione o grupo de cliente:")
        clients = list(hosts_by_client.keys())
        for i, client in enumerate(clients):
            print(f"{i + 1}. {client}")
        print("0. Voltar")

        choice = int(input("Digite o número do grupo de cliente: ")) - 1
        if choice == -1:
            return None
        elif 0 <= choice < len(clients):
            return clients[choice]

def select_host(client):
    while True:
        print("Selecione o host:")
        hosts = hosts_by_client[client]
        for i, host in enumerate(hosts):
            print(f"{i + 1}. {host['name']}")
        print("0. Voltar")

        choice = int(input("Digite o número do host: ")) - 1
        if choice == -1:
            return None
        elif 0 <= choice < len(hosts):
            return hosts[choice]

def select_command_group():
    while True:
        print("Selecione o grupo de comandos:")
        groups = list(commands_groups.keys())
        for i, group in enumerate(groups):
            print(f"{i + 1}. {group}")
        print("0. Voltar")

        choice = int(input("Digite o número do grupo de comandos: ")) - 1
        if choice == -1:
            return None
        elif 0 <= choice < len(groups):
            return groups[choice]

def select_command(group, vpn_instance=None):
    while True:
        print("Selecione o comando:")
        commands = commands_groups[group]
        if vpn_instance is not None:
            commands = [cmd for cmd in commands if "{vpn_instance}" in cmd]
        else:
            commands = [cmd for cmd in commands if "{vpn_instance}" not in cmd]
        for i, command in enumerate(commands):
            parts = command.split("#")
            cmd = parts[0].strip()
            comment = parts[1].strip() if len(parts) > 1 else ""
            print(f"{i + 1}. {cmd} ({comment})")
        print("0. Voltar")

        choice = int(input("Digite o número do comando: ")) - 1
        if choice == -1:
            return None
        elif 0 <= choice < len(commands):
            return commands[choice]

def check_vpn_instances(device, host_name):
    try:
        net_connect = ConnectHandler(**device)
        print(f"Conectado ao dispositivo {host_name}")

        output = net_connect.send_command("display current-configuration | include ip vpn-instance")
        print(f"Comando: display current-configuration | include ip vpn-instance\n{output}\n")

        net_connect.disconnect()
        print(f"Desconectado do dispositivo {host_name}\n")

        vpn_instances = [line.split()[-1] for line in output.splitlines() if "ip vpn-instance" in line]
        return vpn_instances

    except Exception as e:
        print(f"Erro ao conectar ou executar comandos no dispositivo {host_name}: {e}")
        return []

def connect_and_execute(device, command, host_name):
    try:
        cmd = command.split("#")[0].strip()
        
        net_connect = ConnectHandler(**device)
        print(f"Conectado ao dispositivo {host_name}")
        
        prompt = net_connect.find_prompt().strip()
        
        if "routing-table" in cmd.lower():
            output = net_connect.send_command(cmd, expect_string=prompt, read_timeout=120)
        else:
            output = net_connect.send_command(cmd)
        print(f"Comando: {cmd}")
        
        if "routing-table" in cmd.lower():
            lines = output.splitlines()
            lines = [line for line in lines if "---- More ----" not in line]
            pointer = 0
            total_lines = len(lines)
            while pointer < total_lines:
                chunk = lines[pointer:pointer+100]
                print("\n".join(chunk))
                pointer += 100
                if pointer < total_lines:
                    resposta = input("Deseja visualizar as próximas 100 linhas? (s/n): ").strip().lower()
                    if resposta != 's':
                        break
        else:
            print(output)
        
        if cmd == "display current-configuration":
            backup_choice = input("Deseja fazer um backup da configuração? (s/n): ").strip().lower()
            if backup_choice == 's':
                backup_filename = f"{host_name}_backup.txt"
                with open(backup_filename, 'w', encoding='utf-8') as backup_file:
                    backup_file.write(output)
                print(f"Backup salvo em {backup_filename}")
        
        net_connect.disconnect()
        print(f"Desconectado do dispositivo {host_name}\n")
    
    except Exception as e:
        print(f"Erro ao conectar ou executar comandos no dispositivo {host_name}: {e}")

def main():
    nome_usuario, senha = get_user_credentials()

    while True:
        selected_client = select_client()
        if selected_client is None:
            continue
        selected_host = select_host(selected_client)
        if selected_host is None:
            continue

        device = {
            'device_type': 'huawei',
            'ip': selected_host['host'],
            'username': f'{nome_usuario}#netmiko@redes#{selected_host["id"]}',
            'password': senha,
            'port': 2222,
        }

        while True:
            command_group = select_command_group()
            if command_group is None:
                break

            vpn_instance = None
            if command_group == "Visualização de Sessão BGP":
                vpn_instances = check_vpn_instances(device, selected_host['name'])
                if vpn_instances:
                    print("Selecione a vpn-instance:")
                    for i, vpn in enumerate(vpn_instances):
                        print(f"{i + 1}. {vpn}")
                    print(f"{len(vpn_instances) + 1}. Não usar vpn-instance")
                    print("0. Voltar")

                    choice = int(input("Digite o número da vpn-instance: ")) - 1
                    if choice == -1:
                        continue
                    elif choice < len(vpn_instances):
                        vpn_instance = vpn_instances[choice]

            command = select_command(command_group, vpn_instance)
            if command is None:
                continue

            if vpn_instance:
                command = command.format(vpn_instance=vpn_instance)

            connect_and_execute(device, command, selected_host['name'])

            another_command = input("Deseja executar outro comando? (s/n): ").strip().lower()
            if another_command != 's':
                break

        another_host = input("Deseja executar em outro host? (s/n): ").strip().lower()
        if another_host != 's':
            break

if __name__ == "__main__":
    main()
