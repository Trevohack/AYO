

<h1 align="center">AYO</h1>

<div align="center">
  The Efficient CTF (Capture The Flag) Manager<br>
   <br>
  <img alt="GitHub License" src="https://img.shields.io/github/license/Trevohack/AYO?style=for-the-badge&labelColor=blue&color=violet">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Trevohack/AYO?style=for-the-badge&labelColor=blue&color=violet">
  <img alt="Static Badge" src="https://img.shields.io/badge/Tested--on-Linux-violet?style=for-the-badge&logo=linux&logoColor=black&labelColor=blue">
  <img alt="Static Badge" src="https://img.shields.io/badge/Bash-violet?style=for-the-badge&logo=gnubash&logoColor=black&labelColor=blue">
  <p></p>
    <a href="https://github.com/Trevohack/AYO?tab=readme-ov-file#installation">Install</a>
  <span> • </span>
       	<a href="https://github.com/Trevohack/AYO?tab=readme-ov-file#documentation">Documentation</a>
  <span> • </span>
	<a href="https://github.com/Trevohack/AYO?tab=readme-ov-file#usage">Usage</a>
  <p></p>
</div>


## Documentation


* Welcome to AYO, your simple CTF (Capture The Flag) environment manager! AYO focuses on providing an easy-to-use interface for setting up and managing variables crucial for CTFs, such as `rhost` (remote host), `domain`, `url`, and more. With AYO, you can quickly configure your CTF environment and retrieve information with just a few simple commands.

* AYO is an efficient CTF Manager that can do multiple tasks:
	 - Hold box info 
	 - Retrieve box info easily 
	 - Set or change box data easily 
	 - Add new boxes
	 - Configure hosts file 



## Usage

* A detailed explanation on how the commands work.
### Set Info 

* Set variables:
```bash
ayo set --var variable1 --value machine_1
```

* Set a new variable `url` with the value `http://myurl.com/`.
```bash
ayo set --var url --value http://myurl.com/
```


### Add New Boxes

* Create a new box named `example` with the specified `rhost`, `domain`, `platform`, and `active` status.

```bash
ayo new --box example --rhost 10.10.115.28 --domain example.htb --platform htb --active active 
```

* Real Time: 
```bash
ayo new --box Mailing --rhost 10.10.115.28 --domain mailing.htb --platform htb --active active 
```

### Retrieve Box Info 

* Retrieve the values of specific variables you have assigned:
```bash
ayo get rhost
ayo get url 
ayo get domain
```

* Real Time Examples: 
```bash
# Ex 1
rustscan -a $(ayo get rhost)

# Ex 2 
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://$(ayo get domain)/FUZZ.php -t 100

# Ex 3
curl $(ayo get domain)/rev-shell.php 
```



## Installation

1. **Oneliner:**
```bash
 curl -sL https://raw.githubusercontent.com/Trevohack/AYO/main/setup.sh | bash
``` 

2. **Clone The Repository:**  
```bash
git clone https://github.com/Trevohack/AYO
cd AYO 
sudo cp main.py /usr/bin/ayo 
sudo chmod +x /usr/bin/ayo
```

### Thank You! 
