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
                                                              
{Fore.YELLOW}             >> ATT4CK_SEC FRAMEWORK V1.1 <<
{Fore.RED}             [!] STATUS: ULTIMATE PREDATOR MODE
{Fore.CYAN}             Modules: Recon | Nuclei | Fuzzing | Params
{Style.RESET_ALL}
    """
    print(banner)

def get_all_subs(domain):
    print(f"{Fore.BLUE}[*] Phase 1: Nuclear Harvesting for: {Fore.WHITE}{domain}")
    subs = set()
    
    # 1. Subfinder
    print(f"{Fore.YELLOW}[>] Executing Subfinder (Passive Discovery)...")
    os.system(f"subfinder -d {domain} -all -silent > .tmp_subs.txt")
    
    # 2. Assetfinder
    print(f"{Fore.YELLOW}[>] Executing Assetfinder...")
    os.system(f"assetfinder --subs-only {domain} >> .tmp_subs.txt")

    # 3. Passive APIs
    try:
        r1 = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
        [subs.add(l.split(',')[0].lower().strip()) for l in r1.text.split('\n') if ',' in l]
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
    # 1. HTTPX Probing
    httpx_out = f"live_{domain}.txt"
    print(f"\n{Fore.MAGENTA}[*] Phase 2: Predator Probing (Identifying Live Hosts)...")
    os.system(f"httpx -l {input_file} -silent -sc -title -td -o {httpx_out}")
    
    if os.path.exists(httpx_out) and os.path.getsize(httpx_out) > 0:
        # 2. Nuclei Scanning
        nuclei_out = f"exploits_{domain}.txt"
        print(f"\n{Fore.RED}[*] Phase 3: Hunting for Critical Vulnerabilities (Nuclei)...")
        os.system(f"nuclei -l {httpx_out} -severity critical,high,medium -as -rl 150 -silent -o {nuclei_out}")
        
        # 3. FFuf Path Fuzzing (New Module)
        fuzz_out = f"fuzzing_{domain}.txt"
        print(f"\n{Fore.YELLOW}[*] Phase 4: Fuzzing Hidden Directories (FFuf)...")
        # Note: Make sure the wordlist path is correct on your Kali
        wordlist = "/usr/share/wordlists/dirb/common.txt"
        os.system(f"ffuf -w {wordlist} -u https://{domain}/FUZZ -mc 200,301 -t 80 -o {fuzz_out} -of csv -silent")
        print(f"{Fore.GREEN}[+] Fuzzing complete. Saved to: {fuzz_out}")

        # 4. Arjun Parameter Discovery (New Module)
        param_out = f"params_{domain}.txt"
        print(f"\n{Fore.CYAN}[*] Phase 5: Mining Hidden Parameters (Arjun)...")
        os.system(f"arjun -u https://{domain} -oT {param_out}")
        print(f"{Fore.GREEN}[+] Parameter mining complete. Saved to: {param_out}")

    else:
        print(f"{Fore.RED}[!] No responsive targets found. Attack halted.")

def main():
    print_banner()
    target = input(f"{Fore.YELLOW}Enter Target Domain (e.g. google.com): {Fore.WHITE}").strip()
    if not target: return

    unique_targets = get_all_subs(target)
    print(f"{Fore.CYAN}[+] Unique Targets Found: {Fore.WHITE}{len(unique_targets)}")

    raw_file = f"all_subs_{target}.txt"
    with open(raw_file, "w") as f:
        for s in sorted(unique_targets): f.write(s + "\n")

    run_predator_recon(raw_file, target)
    print(f"\n{Fore.GREEN}[#] V1.1 FINAL PREDATOR RECON FINISHED!")
    print(f"{Fore.YELLOW}[*] Check the directory for output files.")

if __name__ == "__main__":
    main()
