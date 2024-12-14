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
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from concurrent.futures import ThreadPoolExecutor, as_completed
from F5 import F5
from Forti import Forti


def iterate(RUN_MULTITHREADING=False):
    mainDir = sys.argv[1]
    print(f"[*] {mainDir}")
    mainCrypto = Crypto()
    port = 443

    f5Token = mainCrypto.encrypt_random_key(getpass("Enter f5 token"))
    fortiToken = mainCrypto.encrypt_random_key(getpass("Enter forti token"))
    
    now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    outputDir = f"output/output-{now}"
    if not os.path.exists(f"{mainDir}/{outputDir}"):
        os.mkdir(f"{mainDir}/{outputDir}")
    
    logFile = open(f"{mainDir}/{outputDir}/log.txt", "w")
    logFile.write(f"[*] {mainDir}" + "\n")

    for dir in os.listdir(f"{mainDir}/api"):
        print(f"[*] {dir}")
        logFile.write(f"[*] {dir}" + "\n")
        
        commandsFile = open(f"{mainDir}/api/{dir}/commands.txt", 'r')
        devicesFile = open(f"{mainDir}/api/{dir}/devices.txt", 'r')
        commands = commandsFile.read().splitlines()
        devices = devicesFile.read().splitlines()
        commandsFile.close()
        devicesFile.close()

        print(f"[*] Devices: {devices}")
        print(f"[*] Commands to run: {commands}")
        logFile.write(f"[*] Devices: {devices}" + "\n")
        logFile.write(f"[*] Commands to run: {commands}" + "\n")


        if dir == 'f5' or dir == 'f501' or dir == 'f502':  
            token = f5Token

        if dir == 'forti' or dir == 'forti01' or dir == 'forti02': 
            token = fortiToken
            

        for device in devices:
            outFilePerDevice = open(f"{mainDir}/{outputDir}/{device}.txt", "w")
            print (f"[*] {device}")
            logFile.write(f"[*] {device}" + "\n")
            
            if dir == 'f5' or dir == 'f501' or dir == 'f502':
                api = F5(device, port, mainCrypto.decrypt_random_key(token))

            if dir == 'forti' or dir == 'forti01' or dir == 'forti02': 
                api = Forti(device, port, mainCrypto.decrypt_random_key(token))
            
            if RUN_MULTITHREADING:
                #parallel threads per device for all commands
                with ThreadPoolExecutor(max_workers=10) as executor:
                    future_list = []
                    for command in commands:
                        time.sleep(api.sleepTimeCommand)
                        future = executor.submit(api.runCommand, command)
                        future_list.append(future)
                    for f in as_completed(future_list):
                        out = f.result()
                        print(json.dumps(out))
                        outFilePerDevice.write(json.dumps(out) + "\n")
            else:
                for command in commands:
                    time.sleep(api.sleepTimeCommand)
                    out = api.runCommand(command)
                    print(json.dumps(out))
                    outFilePerDevice.write(json.dumps(out) + "\n")

            outFilePerDevice.close()  
            
    print("\n[*] DONE!\n")
    logFile.write("\n[*] DONE!\n")
    logFile.close()

def main():
    if len(sys.argv) == 2:
        iterate()
    else:
        print("Run api_multi.py <folder name>")

if __name__ == "__main__":
    main()