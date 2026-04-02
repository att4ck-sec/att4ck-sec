import requests
import sys
import os
import subprocess
import re
from colorama import Fore, Style, init

# Initialize Colors
init(autoreset=True)

def print_banner():
    os.system('clear')
    banner = f"""
{Fore.RED}     ___  _____ _____  _   _   ____ _  __   ____  _____ ____ 
{Fore.RED}    / _ \|_   _|_   _|| | | | / ___| |/ /  / ___|| ____/ ___|
{Fore.RED}   / /_\ \ | |   | |  | |_| || |   | ' /   \___ \|  _|| |    
{Fore.RED}  / /   \ \| |   | |  |  _  || |___| . \    ___) | |__| |___ 
{Fore.RED} /_/     \_|_|   |_|  |_| |_| \____|_|\_\  |____/|_____\____|
                                                              
{Fore.YELLOW}             >> ATT4CK_SEC FRAMEWORK V1 <<
{Fore.RED}             [!!!] STATUS: ULTIMATE PREDATOR MODE
{Fore.CYAN}             Modules: Multi-Engine | Deep-Probe | Cloud-Bypass | Nuclei
{Style.RESET_ALL}
    """
    print(banner)

def get_all_subs(domain):
    print(f"{Fore.BLUE}[*] Phase 1: Nuclear Harvesting for: {Fore.WHITE}{domain}")
    subs = set()
    
    # 1. Subfinder - Deep Passive Discovery
    print(f"{Fore.YELLOW}[>] Executing Subfinder (All Sources)...")
    os.system(f"subfinder -d {domain} -all -silent > .tmp_subs.txt")
    
    # 2. Assetfinder - Domain Discovery
    print(f"{Fore.YELLOW}[>] Executing Assetfinder...")
    os.system(f"assetfinder --subs-only {domain} >> .tmp_subs.txt")

    # 3. Passive APIs (HackerTarget/Anubis/AlienVault)
    try:
        r1 = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
        [subs.add(l.split(',')[0].lower().strip()) for l in r1.text.split('\n') if ',' in l]
        
        r2 = requests.get(f"https://jldc.me/anubis/subdomains/{domain}", timeout=10)
        if r2.status_code == 200: [subs.add(s.lower().strip()) for s in r2.json()]
    except: pass

    # Clean and filter
    if os.path.exists(".tmp_subs.txt"):
        with open(".tmp_subs.txt", "r") as f:
            for line in f:
                s = line.strip().lower()
                if s and s.endswith(domain): subs.add(s)
        os.remove(".tmp_subs.txt")

    return subs

def run_predator_recon(input_file, domain):
    # 1. Advanced HTTPX Probing (Deep Intelligence)
    httpx_out = f"live_{domain}.txt"
    print(f"\n{Fore.MAGENTA}[*] Phase 2: Predator Probing (Common Bug Bounty Ports)...")
    # -p: 80,443,8080,8443,9000,8000,8888,2082,2083,2087,2096 (Control Panels)
    # -td: Tech, -cdn: CDN detection, -asn: Network info, -cname: CNAME discovery
    os.system(f"httpx -l {input_file} -p 80,443,8080,8443,9000,8000,8888,2082,2083,2087,2096 -sc -title -td -ip -cdn -asn -cname -o {httpx_out}")
    
    if os.path.exists(httpx_out) and os.path.getsize(httpx_out) > 0:
        # 2. Nuclei - The Predator Scan (Aggressive)
        nuclei_out = f"exploits_{domain}.txt"
        print(f"\n{Fore.RED}[*] Phase 3: Hunting for Zero-Days & Criticals (Nuclei -as)...")
        # -as: Automatic Scan based on tech, -rl 150: High speed rate limit, -stats: Progress
        # -nm: No Mismatch (Focus on valid tech stacks)
        os.system(f"nuclei -ut && nuclei -l {httpx_out} -severity critical,high,medium -as -rl 150 -stats -o {nuclei_out}")
        
        if os.path.exists(nuclei_out) and os.path.getsize(nuclei_out) > 0:
            print(f"\n{Fore.GREEN}[!!!] TARGET BREACHED! Findings saved in: {Fore.WHITE}{nuclei_out}")
    else:
        print(f"{Fore.RED}[!] No responsive targets found. Security is extremely tight.")

def main():
    print_banner()
    target = input(f"{Fore.YELLOW}Enter Target Domain: {Fore.WHITE}").strip()
    if not target: return

    unique_targets = get_all_subs(target)
    print(f"{Fore.CYAN}[+] Unique Targets Found: {Fore.WHITE}{len(unique_targets)}")

    raw_file = f"all_subs_{target}.txt"
    with open(raw_file, "w") as f:
        for s in sorted(unique_targets): f.write(s + "\n")

    run_predator_recon(raw_file, target)
    print(f"\n{Fore.GREEN}[#] V1 FINAL PREDATOR RECON FINISHED!")

if __name__ == "__main__":
    main()
