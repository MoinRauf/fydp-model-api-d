import time
import json
import requests
import threading
import signal
import sys

venti_json_path = r'E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_ventilator_data.json'
mri_json_path = r'E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_mri_data.json'
patient_json_path = r'E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_patient_monitor_data.json'

venti_api_url = 'http://127.0.0.1:5000/venti'
mri_api_url = 'http://127.0.0.1:5000/mri'
patient_api_url = 'http://127.0.0.1:5000/patient'

stop_threads = False

def read_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def send_data_to_api(api_url, data, api_type):
    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            print(f"[{api_type}] Data sent successfully to {api_url}: {data}")
        else:
            print(f"[{api_type}] Failed to send data to {api_url}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[{api_type}] Error sending data to {api_url}: {e}")

def trigger_api(api_type, json_path, api_url):
    global stop_threads
    data = read_json_data(json_path)
    
    while not stop_threads:
        for item in data:
            if stop_threads:
                break
            send_data_to_api(api_url, item, api_type)
            time.sleep(5)
        if not stop_threads:
            print(f"[{api_type}] End of data reached. Restarting from the beginning.")
            time.sleep(5)

def signal_handler(sig, frame):
    global stop_threads
    print("\n[INFO] Termination signal received. Stopping all threads...")
    stop_threads = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    venti_thread = threading.Thread(target=trigger_api, args=('venti', venti_json_path, venti_api_url))
    mri_thread = threading.Thread(target=trigger_api, args=('mri', mri_json_path, mri_api_url))
    patient_thread = threading.Thread(target=trigger_api, args=('patient', patient_json_path, patient_api_url))

    venti_thread.start()
    mri_thread.start()
    patient_thread.start()

    while True:
        time.sleep(1)
