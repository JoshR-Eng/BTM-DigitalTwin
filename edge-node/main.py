# Imports
import csv, requests, time, os
from collections import deque
from dotenv import load_dotenv
from datetime import datetime, timezone

# Initilise 
load_dotenv()
URL = os.getenv('URL')
FILE_PATH = os.getenv('FILE_PATH')
LOG_FILE = os.getenv('LOG_FILE')
recent_data = deque(maxlen=10)

# ¦--- Handle static data - only really applicable to this test script
try:
    with open(FILE_PATH, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        temperature_data = [float(row['Temperature']) for row in csv_reader]
except (FileNotFoundError, KeyError) as e:
    print(f"Error: {e}")
    exit()
# ---¦

# Prepare Log File
with open(LOG_FILE, mode='w', newline='') as log:
    writer = csv.writer(log)
    writer.writerow(['cooling_power','client_send_time', 
                    'server_recieve_time', 'client_recieve_time'])
                     

# Add something to deal with intial edge case where deque 
# will be empty so no way to calc dt
#  ¦
# \¦/
init_temp = temperature_data[0]
client_send_time = datetime.now(timezone.utc)
recent_data.append({
    "temperature": init_temp, 
    "timestamp": client_send_time })
time.sleep(0.5)
# ----

# Most of this will probabaly stay...
for temperature in temperature_data[1:]:

    current_time = datetime.now(timezone.utc)
    previous_data_point = recent_data[-1]
    dt = (current_time - previous_data_point["timestamp"]).total_seconds()

    payload = {
        "temperature": temperature,
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
        server_recieve_time = response_data.get('server_recieve_time')

        with open(LOG_FILE, mode='a', newline='') as log:
            writer = csv.writer(log)
            writer.writerow([cooling_power, 
                             client_send_time, 
                             server_recieve_time, 
                             client_recieve_time.isoformat()])
            
        print(f"-> Received: Cooling Power={cooling_power:.2f} W")

    else:
        print("Error")
        exit()


    recent_data.append({
        "temperature": temperature,
        "timestamp": current_time
    })
    time.sleep(0.01)