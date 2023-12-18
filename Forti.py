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

class Forti():
    def __init__(self, ip, port, token):
        self.session = requests.Session()
        self.crypto = Crypto()
        self.ip = ip
        self.port = port
        self.sleepTimeCommand = 0.1
        self.headers = {
                    'Content-Type':"application/json",
                    'cache-control':"no-cache"
        }
        self.payload = {
            "method": "",
            "params": [],
            "session": token,
            "id": 0
        }

    def runCommand(self, command):
        method = command.split('---')[0]
        url = f"https://{self.ip}:{str(self.port)}/jsonrpc"
        api_method = command.split('---')[1]
        params = command.split('---')[2]
        self.payload["method"] = api_method
        self.payload["params"] = []
        self.payload["params"].append(json.loads(params)),

        response = self.session.request(method, url, data=json.dumps(self.payload), headers=self.headers, verify = False)
        return response.json()


    

