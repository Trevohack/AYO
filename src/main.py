#!/usr/bin/python3 

"""
> 'AYO' is a simple application to store box information when playing ctfs
> Store box data and receive them instantly 
"""


import time 
import os
import sys
import argparse 
import json
import getpass 
from python_hosts import Hosts, HostsEntry
from rich.console import Console 
from rich.table import Table 


 
hosts = Hosts(path='/etc/hosts')
console = Console()
data_file = "/home/treveen/Documents/ayo/machine_data.json"
htb_path = "/home/treveen/htb"
thm_path = "/home/treveen/thm"


def banner():
    console.print("""
[cyan]
 ▄▄▄·  ▄· ▄▌      
▐█ ▀█ ▐█▪██▌ ▄█▀▄ 
▄█▀▀█ ▐█▌▐█▪▐█▌.▐▌
▐█▪ ▐▌ ▐█▀·.▐█▌.▐▌
 ▀  ▀   ▀ •  ▀█▄▀▪

[/]                                              
""")

def get_box_data():
    global data_file 

    with open(data_file, 'r') as file:
        data = json.load(file)
    return data


def print_box_info():
    global data_file 

    with open(data_file, 'r') as file:
        data = json.load(file)
        current_box = data['current_box']
        status = data['status']
        rhost = data['rhost']
        domain = data['domain']
        platform = data['platform']

    table = Table(title="AYO - CTF Manager") 
    table.add_column("BOX", style="blue")
    table.add_column("RHOST", style="blue")
    table.add_column("DOMAIN", style="green")
    table.add_column("PLATFORM", style="blue") 
    table.add_column("STATUS", style="blue") 

    banner()
    table.add_row(current_box, rhost, domain, platform, status)
    console.print(table) 


def main():
    global data_file 
    global args

    parser = argparse.ArgumentParser(description='AYO - CTF Manager [Help Menu]')
    subparsers = parser.add_subparsers(dest='command', help='Update or get data')

    parser_new = subparsers.add_parser('new', help='Add new CTF box')
    parser_new.add_argument('--box', '-b', type=str, dest='ctf_name', help='Name of the CTF Box')
    parser_new.add_argument('--rhost', '-r', type=str, help='$rhost IP address')
    parser_new.add_argument('--domain', '-d', type=str, help='Domain Name')
    parser_new.add_argument('--platform', '-p', type=str, help='Platform Name')
    parser_new.add_argument('--active', '-a', choices=['active', 'dead'], help='Status of the CTF (active/dead)')

    parser_get = subparsers.add_parser('get', help='Get CTF box info')
    parser_get.add_argument('info', help='Information to retrieve')

    parser_set = subparsers.add_parser('set', help='Set CTF box info')
    parser_set.add_argument('--var', type=str, help='Variable to set')
    parser_set.add_argument('--value', type=str, help='Value to set')

    args = parser.parse_args()

    if args.command == 'new':
        new_box(args)
    if args.command == 'get':
        get_info(args)
    if args.command == 'set':
        set_info(args)


def new_box(args):
    global data_file 
    global htb_path
    global thm_path

    htb_list = ["htb", "HackTheBox", "HTB", "HACKTHEBOX"]
    thm_list = ["thm", "TryHackMe", "THM", "TRYHACKME"]
    data = get_box_data()

    data['current_box'] = args.ctf_name
    data['rhost'] = args.rhost
    data['domain'] = args.domain
    data['platform'] = args.platform
    data['status'] = args.active

    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

    new_box = HostsEntry(entry_type='ipv4', address=args.rhost, names=[args.domain])
    hosts.add([new_box])
    hosts.write()

    print_box_info()
    
    create_dir = console.input(f"[green]Create a directory for {args.ctf_name}? (y/n): [/]")
    if create_dir == "y" or create_dir == "yes":
        if args.platform in htb_list:
            ctf_path = os.path.join(htb_path, args.ctf_name) 
        elif args.platform in thm_list:
            ctf_path = os.path.join(thm_path, args.ctf_name) 

        try:
            os.makedirs(ctf_path)
            console.print(f"[green][+] Directory '{ctf_path}' created successfully.[/]")
        except FileExistsError:
            print(f"Directory '{ctf_path}' already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        console.print(f"[green][+] No directory was created for {args.ctf_name}!")

    console.print(f"[green][+] {args.ctf_name} box added! [/]") 


def get_info(args):
    global data_file 

    data = get_box_data()

    if args.info in data:
        print(data[args.info])
    else:
        console.print(f"[red][-] Unsupported info: {args.info} [/]")

def set_info(args):
    global data_file 

    data = get_box_data() 
    if args.var and args.value:
        data[args.var] = args.value

        with open(data_file, 'w') as file:
            json.dump(data, file, indent=4)

        console.print(f"[green][+] Set {args.var} to {args.value} [/]")
    else:
        console.print("[red][-] Please provide both [bold]--var[/] and [bold]--value arguments[/][red] for setting a variable [/]")
        sys.exit()

if __name__ == "__main__":
    main()
