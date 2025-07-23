# Imports
import csv
import requests
import time
import json
import serial
import os
from collections import deque
from datetime import datetime, timezone


# ----------------------------------    Initilise    -------------------------------------- 

URL = 'https://pi-control-804893961704.europe-west1.run.app'
LOG_FILE = 'BTM-DigitalTwin/logs/results.csv' # remember to create this directory on Pi first
recent_data = deque(maxlen=10)
baudrate = 115200

try:
    dataPath = serial.Serial('/dev/ttyACM0', baudrate, timeout=1)
    dataPath.flush()
    print("CONNECTED: to Arduino on /dev/ttyACM0")
except serial.SerialException as e:
    print(f"Error: Serial. {e}\n\tCould not connect to Arduino")
    exit()


# Prepare Log File
try:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, mode='w', newline='') as log:
        writer = csv.writer(log)
        writer.writerow(['cooling_power','client_send_time', 'client_recieve_time'])
        print(f"Log file created at {LOG_FILE}")
except IOError as e:
    print(f"Error: Log File. \n{e}\n\tLog File could not be created")
    exit()
               
print("\tConnection Initialised \n\tEnabling hardware communication")

# ----------------------------------    Main Loop    --------------------------------------

while True:
    try:
        if dataPath.in_waiting > 0:
            line = dataPath.readline().decode('utf-8').strip()

            try:
                arduino_data = json.loads(line)

                if arduino_data.get('type') == 'temperature':
                    recieved_temp = arduino_data.get('value')

                    current_temp = (recieved_temp * 0.1)           # Applys scaling and offset of CAN config (in .dbc)

                    current_time = datetime.now(timezone.utc)
                    dt = 1.0 # default for first run
                    if recent_data:
                        dt = (current_time - recent_data[-1]['timestamp']).total_seconds()

                    payload = {
                        "temperature": current_temp,
                        "dt": dt,
                        "client_send_time": current_time.isoformat()
                    }

                    response = requests.post(URL, json=payload)
                    client_recieve_time = datetime.now(timezone.utc)

                    # Data response
                    if response.status_code == 200:
                        response_data = response.json()
                        cooling_power = response_data.get('cooling_power')
                        client_send_time = response_data.get('client_send_time')

                        # Send response to dSPACE
                        command_to_dSPACE = {'type': 'cooling_power', 'value': cooling_power}
                        dataPath.write((json.dumps(command_to_dSPACE) + '\n').encode('utf-8'))

                        print(f"{current_temp:.2f}K = {cooling_power}W Cooling")

                        # Logging
                        with open(LOG_FILE, mode='a', newline='') as log:
                            writer = csv.writer(log)
                            writer.writerow([cooling_power, 
                                            client_send_time, 
                                            client_recieve_time.isoformat()])
                            
                    else:
                        print(f"\nERROR: Server \n{response.status_code} - {response.text}")
                            
                    recent_data.append({
                        "temperature": current_temp,
                        "timestamp": current_time
                    })
            except (json.JSONDecodeError, KeyError):
                pass # ignore invalid json data
        
    except serial.SerialException as e:
        print(f"\nERROR: Serial \n{e}.\n\t---Reconnecting---")
        time.sleep(5)
    except requests.exceptions.RequestException as e:
        print(f"\nERROR: Network \n{e}.\n\t---Retrying---")
        time.sleep(5)
    except KeyboardInterrupt:
        print("\nProgram Cancelled")
        dataPath.close()
        break
    time.sleep(0.01)