#!/bin/bash

# Author: Trevohack
# AYO 2.0 Installer

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

banner() {
    echo -e "${RED}
 ▄▄▄     ▓██   ██▓ ▒█████  
▒████▄    ▒██  ██▒▒██▒  ██▒
▒██  ▀█▄   ▒██ ██░▒██░  ██▒
░██▄▄▄▄██  ░ ▐██▓░▒██   ██░
 ▓█   ▓██▒ ░ ██▒▓░░ ████▓▒░
 ▒▒   ▓▒█░  ██▒▒▒ ░ ▒░▒░▒░ 
  ▒   ▒▒ ░▓██ ░▒░   ░ ▒ ▒░ 
  ░   ▒   ▒ ▒ ░░  ░ ░ ░ ▒  
      ░  ░░ ░         ░ ░  
          ░ ░              
${RESET}"
    read -p "Enter your username: " name
}

init() {
    echo -e "[${GREEN}+${RESET}] Configuring Environment..."
    
    ayo_dir="/home/$name/Documents/ayo"
    mkdir -p "$ayo_dir" || { echo -e "${RED}[-] Failed to create directory $ayo_dir${RESET}"; exit 1; }
    cd "$ayo_dir" || { echo -e "${RED}[-] Failed to cd into $ayo_dir${RESET}"; exit 1; }

    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}[-] pip3 is not installed. Please install it first.${RESET}"
        exit 1
    fi

    pip3 install --user rich python-hosts || {
        echo -e "${RED}[-] Python packages failed to install.${RESET}"
        exit 1
    }
}

install() {
    echo -e "[${GREEN}+${RESET}] Downloading AYO..."
    ayo_dir="/home/$name/Documents/ayo"

    wget -q https://raw.githubusercontent.com/Trevohack/AYO/main/src/main.py -O "$ayo_dir/main.py" || {
        echo -e "${RED}[-] Failed to download main.py${RESET}"
        exit 1
    }

    wget -q https://raw.githubusercontent.com/Trevohack/AYO/main/src/machine_data.json -O "$ayo_dir/machine_data.json" || {
        echo -e "${RED}[-] Failed to download machine_data.json${RESET}"
        exit 1
    }

    echo -e "[${GREEN}+${RESET}] Installing AYO to /usr/bin/ayo"

    sudo cp "$ayo_dir/main.py" /usr/bin/ayo || {
        echo -e "${RED}[-] Failed to copy script to /usr/bin${RESET}"
        exit 1
    }

    sudo chmod +x /usr/bin/ayo || {
        echo -e "${RED}[-] Failed to make /usr/bin/ayo executable${RESET}"
        exit 1
    }
}

end() {
    echo -e "[${GREEN}+${RESET}] Done. Run 'ayo' from anywhere to start!"
    echo -e "[${YELLOW}!${RESET}] You might need to restart your terminal."
    echo -e "[${GREEN}+${RESET}] Happy Hacking!"
}

# Main
banner
init
install
end







