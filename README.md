# Server Resources Checker

With the number of servers I check throughout the day, I needed a small Python script to check their resources — without opening a Prometheus dashboard or setting up a monitoring service.

Nothing fancy. Just SSH into a server, grab its CPU, RAM, disk usage, uptime, and busiest processes, and print everything in the terminal.

Got more than one server? Enter the count up front, and a simple `for` loop walks you through them one by one.

## What it does

- Checks multiple Linux servers in one run.
- Connects using a password or an SSH key.
- Skips the server password prompt when you choose SSH key authentication.
- Supports encrypted private keys with a separate passphrase prompt.
- Can use your SSH agent or default keys if you leave the key path empty.
- Shows system information, uptime, CPU usage, RAM usage, and disk space.
- Lists the top five processes by CPU usage.
- Keeps everything right in your terminal.

## Getting started

You'll need Python 3 on your machine and SSH access to the Linux servers you want to check. Run these commands from the project folder:

```bash
# Install the project's dependencies
python3 -m pip install -r requirements.txt

# Start the script
python3 server_resources.py
```

Or install the dependency directly:

```bash
# Install the SSH library used by the script
python3 -m pip install paramiko
```

## How it works

First, the script asks how many servers you want to check. For each server, it asks for:

1. Server IP
2. SSH port — press Enter to use `22`
3. Username
4. Authentication method — `1` for password, `2` for SSH key
5. Your password or private key path, depending on your choice

It connects, prints the resources, closes the connection, and moves on to the next server.

### Using a password

Here's an example of the prompts you'll see:

```text
Number of servers: 2

==================== Server 1/2 ====================
Server IP: 192.168.1.10
SSH port [22]:
Username: root
Authentication method (1 = password, 2 = SSH key): 1
Password:
```

Your password stays hidden while you type.

### Using an SSH key

```text
Authentication method (1 = password, 2 = SSH key): 2
Private key path (leave empty to use SSH agent/default keys): ~/.ssh/id_rsa
Is this private key encrypted? [y/N]: n
```

No server password needed in this mode. If your private key is encrypted, answer `y` and enter its passphrase — that's the key's passphrase, not the server password.

Leave the key path empty to use your SSH agent or default keys. If those keys are encrypted, unlock them in your SSH agent first.

## Before your first connection

The script doesn't automatically trust unknown host keys. Connect with regular SSH first and verify the server's fingerprint with your hosting provider or server admin before accepting it.

```bash
# Replace USERNAME and SERVER_IP with your details
# Change 22 if your server uses a different SSH port
ssh -p 22 USERNAME@SERVER_IP
```

Once you've verified and accepted the key, SSH saves it in `known_hosts`, and the script can use it on future connections.

The remote server needs the usual Linux tools: `uname`, `uptime`, `top`, `grep`, `free`, `df`, `ps`, and `head`. Your SSH user must be allowed to run them.

## What's running on the server?

These are the commands the script runs. You can copy them and try them yourself:

```bash
# Show system and kernel information
uname -a

# Show uptime and load averages
uptime

# Show used and available RAM in a readable format
free -h

# Show used and available disk space for mounted filesystems
df -h

# Grab the CPU summary from top using English output
LC_ALL=C top -bn1 | grep 'Cpu(s)'

# Show the five busiest processes by CPU usage, plus the header
ps aux --sort=-%cpu | head -n 6
```

## A quick heads-up

This is a quick, manual check — not a replacement for Prometheus, Grafana, or a full monitoring setup. There's no background collection, history, or alerting. It's just for those moments when you want to check a few servers and get on with your day.

## Project files

```text
server_resources.py   # The main script
requirements.txt      # Python dependencies
README.md             # You're reading it
```
