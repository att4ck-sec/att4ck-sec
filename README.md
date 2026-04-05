# ATT4CK_SEC V2.0 (Stealth Edition) 🛡️

An automated reconnaissance and vulnerability scanning framework designed for Ethical Hackers and Bug Bounty researchers. This version is optimized for stealth and bypassing basic WAF protections.

## 🚀 Features
- **Passive Subdomain Discovery**: Fast and stealthy enumeration.
- **Stealth Probing**: Uses `httpx` with custom User-Agents and rate limiting.
- **Safe Vulnerability Scanning**: Integrated with `nuclei` at a safe request rate.
- **Anti-Block Fuzzing**: Advanced `ffuf` configuration to prevent IP blocking.
- **WAF Bypass**: Randomized headers and delayed requests.

## 🛠️ Installation & Usage
Ensure you have `subfinder`, `httpx`, `nuclei`, and `ffuf` installed on your Kali Linux.

```bash
git clone [https://github.com/att4ck-sec/att4ck-sec.git](https://github.com/att4ck-sec/att4ck-sec.git)
cd att4ck-sec
python3 att4ck_sec.py
