#!/usr/bin/python3 

"""
> 'AYO' is a simple application to store box information when playing ctfs
> Store box data and receive them instantly
"""

import argparse
import json
import os
import socket
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import box
from pathlib import Path
from datetime import datetime
import time

# Global Paths
JSON_FILE = "/root/ayo-boxes.json"
HTB_PATH = Path("/root/htb")
THM_PATH = Path("/root/thm")
HOSTS_FILE = "/etc/hosts"

# Init
console = Console()

# Load boxes JSON
def load_boxes():
    if not os.path.exists(JSON_FILE):
        return {"sessions": {}, "boxes": {}}
    with open(JSON_FILE) as f:
        return json.load(f)

# Save boxes JSON
def save_boxes(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Pretty print boxes
def print_all_boxes():
    data = load_boxes()
    boxes = data.get("boxes", {})
    table = Table(title="[bold green]All Boxes", box=box.SIMPLE)
    table.add_column("Name", style="cyan", no_wrap=True)
    for name in boxes:
        table.add_row(name)
    console.print(table)

# Print hosts file
def print_hosts():
    table = Table(title="[bold yellow]/etc/hosts Analysis", box=box.SIMPLE)
    table.add_column("IP", style="magenta")
    table.add_column("Domain", style="cyan")
    with open(HOSTS_FILE) as f:
        for line in f:
            if not line.strip() or line.startswith("#"): continue
            parts = line.split()
            if len(parts) >= 2:
                table.add_row(parts[0], parts[1])
    console.print(table)

# Print hot boxes
def print_hot():
    data = load_boxes()
    boxes = data.get("boxes", {})
    table = Table(title="[bold red]Hot Boxes", box=box.SIMPLE)
    table.add_column("Name", style="red")
    for name, info in boxes.items():
        if info.get("hot"):
            table.add_row(name)
    console.print(table)

# Ping function
def ping(ip):
    try:
        subprocess.run(["ping", "-c", "1", ip], check=True)
    except subprocess.CalledProcessError:
        console.print(f"[bold red]Failed to ping {ip}")

# Edit variable
def edit_var(box, var, value):
    data = load_boxes()
    boxes = data.get("boxes", {})
    if box in boxes:
        boxes[box][var] = value
        save_boxes(data)
        console.print(f"[green]Updated {box}'s {var} to {value}")
    else:
        console.print("[red]Box not found")

# Get variable
def get_var(box, var):
    data = load_boxes()
    boxes = data.get("boxes", {}) 
    if box in boxes:
        value = boxes[box].get(var)
        if value is not None:
            print(value)
        else:
            console.print(f"[red]{var} not set for {box}")
    else:
        console.print("[red]Box not found")

# Create box
def create_box(name, ip, platform, domain, session=None):
    data = load_boxes()
    boxes = data.setdefault("boxes", {})
    boxes[name] = {
        "rhost": ip,
        "platform": platform,
        "domain": domain,
        "status": "active",
        "notes": "",
        "hot": False,
        "session": session
    }
    save_boxes(data)
    with open(HOSTS_FILE, "a") as f:
        f.write(f"{ip}\t{domain}\n")
    console.print(f"[bold green]Box {name} created with IP {ip} and domain {domain}")

# Add hot status
def add_hot(name):
    data = load_boxes()
    boxes = data.get("boxes", {})
    if name in boxes:
        boxes[name]["hot"] = True
        save_boxes(data)
        console.print(f"[bold yellow]{name} marked as HOT")
    else:
        console.print("[red]Box not found")

# Show box details
def show_box(name):
    data = load_boxes()
    boxes = data.get("boxes", {})
    if name in boxes:
        info = boxes[name]
        table = Table(title=f"[bold cyan]{name} Box Info", box=box.SIMPLE)
        for k, v in info.items():
            table.add_row(k, str(v))
        console.print(table)
    else:
        console.print("[red]Box not found")

# Session Management
def create_session(session_name):
    data = load_boxes()
    sessions = data.setdefault("sessions", {})
    if session_name not in sessions:
        sessions[session_name] = {"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        save_boxes(data)
        console.print(f"[bold green]Session '{session_name}' created")
    else:
        console.print(f"[yellow]Session '{session_name}' already exists")

def show_status_bar(session):
    data = load_boxes()
    boxes = data.get("boxes", {})
    session_data = data.get("sessions", {}).get(session, {})
    time_created = session_data.get("created", "N/A")
    count = len([b for b in boxes.values() if b.get("session") == session])
    panel = Panel(f"[bold]{session.upper()}[/bold]             Boxes: {count}   Time: {time_created}   Online: yes", style="dim", box=box.ROUNDED)
    console.print(panel)

# Console mode
def launch_console():
    for _ in track(range(20), description="[green]Launching Console..."):
        time.sleep(0.02)

    console.print("[bold magenta]Welcome to AYO Console Mode")
    current_session = None

    while True:
        try:
            if current_session:
                show_status_bar(current_session)
            cmd = Prompt.ask(f"[bold green][ayo:{current_session or 'none'}] >").strip()

            if cmd == "exit":
                break
            elif cmd == "list boxes":
                print_all_boxes()
            elif cmd.startswith("ping"):
                parts = cmd.split()
                if len(parts) == 2:
                    name = parts[1]
                    data = load_boxes()
                    ip = data.get("boxes", {}).get(name, {}).get("rhost")
                    if ip:
                        ping(ip)
                    else:
                        console.print("[red]Box not found or IP not set")
                else:
                    console.print("[red]Usage: ping <box>")
            elif cmd.startswith("edit"):
                parts = cmd.split()
                if len(parts) == 4:
                    _, box, var, value = parts
                    edit_var(box, var, value)
                else:
                    console.print("[red]Usage: edit <box> <variable> <value>")
            elif cmd.startswith("create"):
                parts = cmd.split()
                if len(parts) == 5:
                    _, box, ip, platform, domain = parts
                    create_box(box, ip, platform, domain, session=current_session)
                else:
                    console.print("[red]Usage: create <box> <ip> <platform> <domain>")
            elif cmd.startswith("add hot"):
                parts = cmd.split()
                if len(parts) == 3:
                    add_hot(parts[2])
                else:
                    console.print("[red]Usage: add hot <box>")
            elif cmd.startswith("show"):
                parts = cmd.split()
                if len(parts) == 2:
                    show_box(parts[1])
                else:
                    console.print("[red]Usage: show <box>")
            elif cmd.startswith("session"):
                parts = cmd.split()
                if len(parts) == 2:
                    current_session = parts[1]
                    create_session(current_session)
                else:
                    console.print("[red]Usage: session <name>")
            elif cmd == "dashboard":
                print_all_boxes()
                print_hosts()
                print_hot()
            else:
                console.print("[bold red]Unknown command")
        except Exception as e:
            console.print(f"[red]Error: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("subargs", nargs="*", help="Subarguments for command")
    parser.add_argument("--box", help="Box name")
    parser.add_argument("--rhost", help="Remote host IP")
    parser.add_argument("--domain", help="Box domain")
    parser.add_argument("--platform", help="Platform")
    parser.add_argument("--active", help="Status")
    parser.add_argument("--var", help="Variable to set")
    parser.add_argument("--value", help="Value to set")
    parser.add_argument("--dashboard", action="store_true", help="Show dashboard")

    args = parser.parse_args()

    if args.dashboard:
        print_all_boxes()
        print_hosts()
        print_hot()

    elif args.command == "koth":
        launch_console()

    elif args.command == "new" and args.box and args.rhost and args.domain and args.platform:
        create_box(args.box, args.rhost, args.platform, args.domain)

    elif args.command == "set":
        if args.box and args.var and args.value:
            edit_var(args.box, args.var, args.value)
        elif len(args.subargs) == 3:
            box, var, value = args.subargs
            edit_var(box, var, value)
        else:
            console.print("[red]Usage: ayo set <box> <var> <value>")

    elif args.command == "get":
        if args.box and args.var:
            get_var(args.box, args.var)
        elif len(args.subargs) == 2:
            box, var = args.subargs
            get_var(box, var)
        else:
            console.print("[red]Usage: ayo get <box> <var>")

    else:
        console.print("[yellow]Use --dashboard to show dashboard or run a valid command")

if __name__ == "__main__":
    main()
