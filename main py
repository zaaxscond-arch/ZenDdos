#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import threading
from datetime import datetime
from colorama import init, Fore, Style

from core.attack import AttackEngine
from core.utils import Utils

init(autoreset=True)

VERSION = "2.0"
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

class ZenDdos:
    def __init__(self):
        self.config = self.load_config()
        self.attack = AttackEngine(self.config)
        self.running = True
        self.stats = {
            'total_requests': 0,
            'start_time': None,
            'target': None
        }
    
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except:
            default = {
                "threads": 500,
                "timeout": 5,
                "max_requests": 100000,
                "delay": 0.001,
                "user_agents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                ]
            }
            with open('config.json', 'w') as f:
                json.dump(default, f, indent=4)
            return default
    
    def show_banner(self):
        os.system('clear' if os.name == 'posix' else 'cls')
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
{Fore.GREEN}│  {Fore.WHITE}[6] {Fore.YELLOW}CONFIGURATION{Fore.CYAN}                           │
{Fore.GREEN}│  {Fore.WHITE}[7] {Fore.YELLOW}STATISTICS{Fore.CYAN}                              │
{Fore.GREEN}│  {Fore.WHITE}[8] {Fore.YELLOW}ABOUT{Fore.CYAN}                                  │
{Fore.GREEN}│  {Fore.WHITE}[0] {Fore.RED}EXIT{Fore.CYAN}                                      │
{Fore.CYAN}└─────────────────────────────────────────────────────┘
        """)
        
        choice = input(f"{Fore.YELLOW}[>] Pilih angka: {Fore.WHITE}")
        return choice.strip()
    
    def get_target(self):
        target = input(f"{Fore.WHITE}[>] Target URL/IP: {Fore.YELLOW}")
        port = input(f"{Fore.WHITE}[>] Port (default 80): {Fore.YELLOW}") or "80"
        duration = input(f"{Fore.WHITE}[>] Duration (detik): {Fore.YELLOW}") or "60"
        
        return {
            'target': target.strip(),
            'port': int(port),
            'duration': int(duration)
        }
    
    def run_attack(self, method):
        target_data = self.get_target()
        if not target_data['target']:
            print(f"{Fore.RED}[!] Target kosong!")
            return
        
        self.stats['target'] = target_data['target']
        self.stats['start_time'] = datetime.now()
        
        print(f"\n{Fore.CYAN}[*] Memulai serangan...")
        print(f"{Fore.WHITE}Target: {Fore.YELLOW}{target_data['target']}")
        print(f"{Fore.WHITE}Port: {Fore.YELLOW}{target_data['port']}")
        print(f"{Fore.WHITE}Duration: {Fore.YELLOW}{target_data['duration']}s")
        print(f"{Fore.WHITE}Method: {Fore.YELLOW}{method}")
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
    
    def show_config(self):
        self.show_banner()
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│  {Fore.YELLOW}KONFIGURASI{Fore.CYAN}                                   │")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘\n")
        
        print(f"{Fore.WHITE}Threads    : {Fore.GREEN}{self.config.get('threads', 500)}")
        print(f"{Fore.WHITE}Timeout    : {Fore.GREEN}{self.config.get('timeout', 5)}s")
        print(f"{Fore.WHITE}Max Request: {Fore.GREEN}{self.config.get('max_requests', 100000)}")
        print(f"{Fore.WHITE}Delay      : {Fore.GREEN}{self.config.get('delay', 0.001)}s")
        
        print(f"\n{Fore.YELLOW}[1] Ubah Threads")
        print(f"{Fore.YELLOW}[2] Ubah Timeout")
        print(f"{Fore.YELLOW}[3] Ubah Max Request")
        print(f"{Fore.YELLOW}[0] Kembali")
        
        choice = input(f"\n{Fore.YELLOW}[>] Pilih: {Fore.WHITE}")
        
        if choice == '1':
            val = int(input(f"{Fore.WHITE}Threads: {Fore.YELLOW}") or "500")
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
        
        if self.stats['start_time']:
            duration = datetime.now() - self.stats['start_time']
            print(f"{Fore.WHITE}Target      : {Fore.YELLOW}{self.stats['target']}")
            print(f"{Fore.WHITE}Duration    : {Fore.YELLOW}{str(duration).split('.')[0]}")
            print(f"{Fore.WHITE}Total Req   : {Fore.GREEN}{self.attack.total_requests}")
            print(f"{Fore.WHITE}Success     : {Fore.GREEN}{self.attack.success}")
            print(f"{Fore.WHITE}Failed      : {Fore.RED}{self.attack.failed}")
        else:
            print(f"{Fore.YELLOW}[!] Belum ada serangan")
        
        input(f"\n{Fore.YELLOW}[>] Enter untuk kembali...")
    
    def about(self):
        self.show_banner()
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────┐")
        print(f"{Fore.CYAN}│  {Fore.YELLOW}TENTANG ZENDDOS{Fore.CYAN}                              │")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────┘\n")
        
        print(f"{Fore.WHITE}Nama    : {Fore.CYAN}{TOOL_NAME}")
        print(f"{Fore.WHITE}Versi   : {Fore.CYAN}{VERSION}")
        print(f"{Fore.WHITE}Dev     : {Fore.CYAN}{DEVELOPER}")
        print(f"{Fore.WHITE}Metode  : {Fore.CYAN}HTTP Flood, SYN Flood, UDP Flood, Slowloris, Mixed")
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
                self.show_config()
            elif choice == '7':
                self.show_stats()
            elif choice == '8':
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
