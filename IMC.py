import os
import sys
import time
import random
import requests
import hashlib
import socket
import json
import shodan
import pyfiglet
import scapy.all as scapy
from bs4 import BeautifulSoup
from termcolor import colored
from tqdm import tqdm

# Banner & UI
def banner():
    os.system("clear" if os.name == "posix" else "cls")
    ascii_banner = pyfiglet.figlet_format("INFORMATION-CRACKER")
    print(colored(ascii_banner, 'red'))
    print(colored("By: GenzPX", 'yellow'))
    print(colored("Ultimate OSINT & Pentesting Tool", 'green'))
    print("-" * 60)

# Gunakan API resmi atau library khusus
def check_github(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        return response.status_code == 200
    except:
        return False

# Implementasi untuk platform lain dengan API



# Loading Animation
def loading(text):
    for _ in tqdm(range(50), desc=text, ascii=True, colour="blue"):
        time.sleep(0.02)

# IP & Geolocation Tracker
def ip_tracker():
    ip = input(colored("\nMasukkan IP Target: ", "cyan")).strip()
    if not ip:
        print(colored("❌ IP tidak boleh kosong!", "red"))
        return
    loading("Tracking IP...")
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['status'] == 'fail':
            print(colored("❌ IP tidak valid atau tidak ditemukan!", "red"))
        else:
            print(colored(f"\nLokasi: {data['city']}, {data['regionName']}, {data['country']}", "yellow"))
            print(colored(f"ISP: {data['isp']}, Org: {data['org']}", "yellow"))
            print(colored(f"Koordinat: {data['lat']}, {data['lon']}", "yellow"))
    except requests.exceptions.RequestException:
        print(colored("❌ Gagal menghubungi server!", "red"))

# Social Media Recon (lebih banyak situs)
def social_media_recon():
    username = input(colored("\nMasukkan Username: ", "cyan")).strip()
    if not username:
        print(colored("❌ Username tidak boleh kosong!", "red"))
        return
    loading("Mencari di 10+ platform...")
    social_sites = [
        "facebook.com", "twitter.com", "instagram.com", "github.com",
        "reddit.com", "tiktok.com", "pinterest.com", "linkedin.com",
        "medium.com", "tumblr.com"
    ]
    found = False
    for site in social_sites:
        url = f"https://{site}/{username}"
        response = requests.get(url)
        if response.status_code == 200:
            found = True
            print(colored(f"✔️ Ditemukan di {site}: {url}", "green"))
    if not found:
        print(colored("❌ Tidak ditemukan di platform manapun!", "red"))

# Web Exploit Scanner (lebih canggih)
def exploit_scanner():
    url = input(colored("\nMasukkan URL Target: ", "cyan")).strip()
    if not url:
        print(colored("❌ URL tidak boleh kosong!", "red"))
        return
    loading("Memeriksa eksploitasi...")
    payloads = [
        "' OR '1'='1'--", "' OR '1'='1'#", 
        "<script>alert('XSS')</script>", 
        "../../../../etc/passwd", "'; DROP TABLE users; --"
    ]
    for payload in payloads:
        try:
            response = requests.get(url + payload, timeout=5)
            if "root:" in response.text or "alert" in response.text:
                print(colored(f"⚠️ Vulnerable: {payload}", "red"))
            else:
                print(colored(f"✅ Aman dari: {payload}", "green"))
        except requests.exceptions.RequestException:
            print(colored("❌ Gagal menghubungi server!", "red"))
            return

# Network Scanner (dengan port scanning)
def network_scanner():
    target_ip = input(colored("\nMasukkan IP Range: ", "cyan")).strip()
    if not target_ip:
        print(colored("❌ IP tidak boleh kosong!", "red"))
        return
    loading("Memindai jaringan...")
    arp_request = scapy.ARP(pdst=target_ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    for element in answered:
        print(colored(f"IP: {element[1].psrc} - MAC: {element[1].hwsrc}", "yellow"))

    print(colored("\nScanning port umum (80, 443, 21, 22, 25, 3306)...", "blue"))
    common_ports = [80, 443, 21, 22, 25, 3306]
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(colored(f"✔️ Port {port} terbuka", "green"))
        else:
            print(colored(f"❌ Port {port} tertutup", "red"))
        sock.close()

# Hash Cracker (dengan wordlist lebih besar)
def hash_cracker():
    hash_value = input(colored("\nMasukkan Hash: ", "cyan")).strip()
    if not hash_value:
        print(colored("❌ Hash tidak boleh kosong!", "red"))
        return
    wordlist = ["password", "123456", "admin", "qwerty", "letmein", "123456789", "welcome", "monkey"]
    loading("Cracking hash...")
    for word in wordlist:
        hashed = hashlib.md5(word.encode()).hexdigest()
        if hashed == hash_value:
            print(colored(f"✔️ Hash ditemukan: {word}", "green"))
            return
    print(colored("❌ Hash tidak ditemukan", "red"))

# Gunakan wordlist eksternal
def load_wordlist(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(colored("❌ Wordlist tidak ditemukan!", "red"))
        return []

# Gunakan framework seperti OWASP ZAP API
def scan_sqli(url):
    try:
        test_payload = "' OR 1=1--"
        response = requests.get(f"{url}?id={test_payload}")
        return "error in your SQL syntax" in response.text
    except:
        return False

def show_warning():
    print(colored("PERINGATAN: ", "red") + "Tool ini hanya untuk tujuan edukasi dan testing authorized!")
    print(colored("JANGAN GUNAKAN UNTUK AKTIVITAS ILEGAL!", "red"))
    input("Tekan ENTER untuk setuju dan melanjutkan...")

import logging
logging.basicConfig(filename='audit.log', level=logging.INFO)

def log_action(user_ip, action):
    logging.info(f"[{time.ctime()}] {user_ip} - {action}")

# Integrasi Shodan
def shodan_scan(api_key, ip):
    api = shodan.Shodan(api_key)
    try:
        results = api.host(ip)
        return results
    except shodan.APIError as e:
        print(colored(f"❌ Error Shodan: {e}", "red"))
        return None



# Menu Utama
def main():
    while True:
        banner()
        print(colored("[1] IP & Geolocation Tracker", "cyan"))
        print(colored("[2] Social Media Recon", "cyan"))
        print(colored("[3] Web Exploit Scanner", "cyan"))
        print(colored("[4] Network Scanner", "cyan"))
        print(colored("[5] Hash Cracker", "cyan"))
        print(colored("[0] Keluar", "red"))
        choice = input(colored("\nPilih opsi: ", "yellow"))
        
        if choice == "1":
            ip_tracker()
        elif choice == "2":
            social_media_recon()
        elif choice == "3":
            exploit_scanner()
        elif choice == "4":
            network_scanner()
        elif choice == "5":
            hash_cracker()
        elif choice == "0":
            print(colored("\nTerima kasih telah menggunakan Information-Cracker!", "green"))
            sys.exit()
        else:
            print(colored("\nOpsi tidak valid!", "red"))
        input(colored("\nTekan ENTER untuk kembali ke menu...", "yellow"))

# Jalankan Script
if __name__ == "__main__":
    main()
