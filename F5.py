import os
import sys
import paramiko
import time
from getpass import getpass
from datetime import datetime
import requests
import json
from Crypto import Crypto
import time
import gc
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class F5():
    def __init__(self, ip, port, token):
        self.session = requests.Session()
        self.crypto = Crypto()
        self.ip = ip
        self.port = port
        self.sleepTimeCommand = 0.2
        #self.token = self.crypto.encrypt_random_key(token)
        self.headers = self.crypto.encrypt_random_key(json.dumps({
                    'Content-Type':"application/json",
                    'X-F5-Auth-Token':token,
                    'cache-control':"no-cache"
                }))

    def runCommand(self, command):
        method = command.split('---')[0]
        #url = "https://" + self.ip + ":" + str(self.port) + command.split('---')[1]
        url = f"https://{self.ip}:{str(self.port)}{command.split('---')[1]}"
        payload = command.split('---')[2]  
        response = self.session.request(method, url, data=payload, headers=json.loads(self.crypto.decrypt_random_key(self.headers)), verify = False)
        return response.json()


    

