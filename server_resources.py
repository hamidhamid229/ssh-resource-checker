import getpass
from pathlib import Path

import paramiko


def get_server_resources() -> None:
    host = input("Server IP: ").strip()
    try:
        port = int(input("SSH port [22]: ").strip() or "22")
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("SSH port must be a number between 1 and 65535.")
        return

    username = input("Username: ").strip()
    while True:
        auth_method = input("Authentication method (1 = password, 2 = SSH key): ").strip()
        if auth_method in {"1", "2"}:
            break
        print("Please enter 1 or 2.")

    if auth_method == "1":
        auth_options = {
            "password": getpass.getpass("Password: "),
            "allow_agent": False,
            "look_for_keys": False,
        }
    else:
        key_path = input("Private key path (leave empty to use SSH agent/default keys): ").strip()
        auth_options = {
            "allow_agent": not key_path,
            "look_for_keys": not key_path,
        }
        if key_path:
            auth_options["key_filename"] = str(Path(key_path).expanduser())
            encrypted = input("Is this private key encrypted? [y/N]: ").strip().lower()
            if encrypted in {"y", "yes"}:
                auth_options["passphrase"] = getpass.getpass("Private key passphrase: ")

    commands = {
        "Operating system": "uname -a",
        "Uptime": "uptime",
        "CPU": "LC_ALL=C top -bn1 | grep 'Cpu(s)'",
        "RAM usage": "free -h",
        "Disk usage": "df -h",
        "Top processes": "ps aux --sort=-%cpu | head -n 6",
    }

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.RejectPolicy())

    try:
        print(f"\nConnecting to {host}...")
        ssh.connect(
            hostname=host,
            port=port,
            username=username,
            timeout=10,
            banner_timeout=10,
            auth_timeout=10,
            **auth_options,
        )
        print("Connection established.\n")

        for title, command in commands.items():
            _, stdout, stderr = ssh.exec_command(command, timeout=30)
            output = stdout.read().decode("utf-8", errors="replace").strip()
            error = stderr.read().decode("utf-8", errors="replace").strip()

            print(f"\n{'=' * 20} {title} {'=' * 20}")
            if output:
                print(output)
            if error:
                print(f"Error: {error}")
            if not output and not error:
                print("No output received.")

    except paramiko.PasswordRequiredException:
        print("The private key is encrypted. Provide its passphrase or unlock it in your SSH agent.")
    except paramiko.AuthenticationException:
        print("Authentication failed. Check the username, password, or SSH key.")
    except paramiko.SSHException as error:
        print(f"SSH error: {error}")
        print("The host key must be registered in known_hosts after verifying its fingerprint.")
    except TimeoutError:
        print("The connection or command timed out.")
    except OSError as error:
        print(f"Connection error: {error}")
    finally:
        ssh.close()
        print("\nConnection closed.")


if __name__ == "__main__":
    while True:
        try:
            server_count = int(input("Number of servers: ").strip())
            if server_count < 1:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")

    for index in range(server_count):
        print(f"\n{'=' * 20} Server {index + 1}/{server_count} {'=' * 20}")
        get_server_resources()
