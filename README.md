# API MULTI

## Execute multiple API commands on multiple devices

## Running the commands
python gettoken_f5.py  
python gettoken_forti.py  
python api_multi.py FOLDER_NAME  

## Features
1. Run multiple commands on multiple devices
2. Seperation by set of commands per main directory - Each main folder can hold multiple devices and their respective commands
3. Flexible and supports multiple devices and commands based on the required set
4. Log all commands and output to the file per device
5. General log to track the process
6. Support for multithreading for all commands per device
7. Playing with in memory ecryption of username, password and token
8. API for F5 and Fortimanager
9. Can be easily extended to use with other APIs

