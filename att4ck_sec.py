import os
import subprocess

def banner():
    print("""
    \033[1;35m
     _  _  _____  _____  _  _   ___  _  __   ___  ___  ___ 
    / _ \|_   _||_   _|| || | / __|| |/ /  / __|| __|/ __|
    / ___ \ | |    | |  | |_| || (__ | ' <   \__ \| _|| (__ 
    /_/   \_\|_|    |_|  \___/  \___||_|\_\  |___/|___|\___|
    
    >> VERSION 2.0 - STEALTH MODE <<
    [*] Features: User-Agent Spoofing | Rate Limiting | WAF Bypass
    \033[0m""")

def run_cmd(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"\033[1;31m[-] Error executing component: {e}\033[0m")

def main():
    os.system('clear')
    banner()
    
    target = input("\033[1;34m[*] Enter Target Domain (e.g. tesla.com): \033[0m").strip()
    if not target: return

    # Professional User-Agent to bypass basic WAF
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

    # Phase 1: Subdomain Discovery
    print(f"\n\033[1;32m[+] Phase 1: Subdomain Discovery...\033[0m")
    sub_file = f"subs_{target}.txt"
    run_cmd(f"subfinder -d {target} -silent -o {sub_file}")

    # Phase 2: HTTPX (Stealth Mode Monitoring)
    print(f"\n\033[1;32m[+] Phase 2: Probing Live Hosts (Monitoring)...\033[0m")
    live_file = f"live_{target}.txt"
    # -rl 5 limits requests per second to stay undetected
    run_cmd(f"httpx -l {sub_file} -H 'User-Agent: {ua}' -rl 5 -status-code -title -o {live_file}")

    # Phase 3: Nuclei (Safe Vulnerability Scanning)
    print(f"\n\033[1;32m[+] Phase 3: Deep Vulnerability Scan (Nuclei)...\033[0m")
    exploit_file = f"exploits_{target}.txt"
    # -rl 3 is very quiet and safe for large targets
    run_cmd(f"nuclei -l {live_file} -H 'User-Agent: {ua}' -rl 3 -severity critical,high,medium -o {exploit_file}")

    # Phase 4: Directory Fuzzing (Anti-Block FFuf)
    print(f"\n\033[1;32m[+] Phase 4: Directory Fuzzing (FFuf Stealth)...\033[0m")
    fuzz_file = f"fuzz_{target}.txt"
    # -p 0.7 and -t 5 are crucial to avoid IP blocking
    run_cmd(f"ffuf -u http://{target}/FUZZ -w /usr/share/wordlists/dirb/common.txt -H 'User-Agent: {ua}' -p 0.7 -t 5 -mc 200,301 -o {fuzz_file}")

    print(f"\n\033[1;33m[#] SUCCESS: Stealth V2 Scan Finished for {target}\033[0m")

if __name__ == "__main__":
    main()
