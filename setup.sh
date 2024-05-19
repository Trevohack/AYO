#!/bin/bash

# Author: Trevohack


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
    mkdir -p "/home/$name/Documents/ayo"
    cd "/home/$name/Documents/ayo" || exit
}

install() {
    echo -e "[${GREEN}+${RESET}] Downloading AYO..."
    wget https://raw.githubusercontent.com/Trevohack/AYO/main/src/main.py -O "/home/$name/Documents/ayo/main.py"
    wget https://raw.githubusercontent.com/Trevohack/AYO/main/src/machine_data.json -O "/home/$name/Documents/ayo/machine_data.json"

    sudo cp "/home/$name/Documents/ayo/main.py" "/usr/bin/ayo" 
    sudo chmod +x /usr/bin/ayo 
}

end() {
    echo -e "[${GREEN}+${RESET}] Happy Hacking!"
}

banner
init
install
end
