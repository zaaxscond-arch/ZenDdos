#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import random
import socket
from datetime import datetime

class Utils:
    @staticmethod
    def clear_screen():
        os.system('clear' if os.name == 'posix' else 'cls')
    
    @staticmethod
    def get_ip(target):
        try:
            return socket.gethostbyname(target)
        except:
            return target
    
    @staticmethod
    def random_string(length=10):
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def current_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
