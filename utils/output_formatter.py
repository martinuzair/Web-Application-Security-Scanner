import json
import os
from colorama import Fore, Style, init

init(autoreset=True)


def info(message):
    print(Fore.CYAN + "[*] " + message + Style.RESET_ALL)


def success(message):
    print(Fore.GREEN + "[+] " + message + Style.RESET_ALL)


def warning(message):
    print(Fore.YELLOW + "[!] " + message + Style.RESET_ALL)


def error(message):
    print(Fore.RED + "[-] " + message + Style.RESET_ALL)


def save_report(report_data, filename="reports/report.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    success(f"Report saved to {filename}")