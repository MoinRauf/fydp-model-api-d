import time
import json
import requests
import threading
import signal
import sys

# File paths for JSON data
venti_json_path = r'E:\Ai-work-fydp\fydp-model-api\Server\data\generated_ventilator_data.json'
mri_json_path = r'E:\Ai-work-fydp\fydp-model-api\Server\data\generated_mri_data.json'
patient_json_path = r'E:\Ai-work-fydp\fydp-model-api\Server\data\generated_patient_monitor_data.json'

# API endpoints
venti_api_url = 'http://127.0.0.1:5000/venti/predict'
mri_api_url = 'http://127.0.0.1:5000/mri/predict'
patient_api_url = 'http://127.0.0.1:5000/patient/predict'

# Global flag to stop threads
stop_threads = False

# Function to read the JSON data
def read_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to send data to the Flask API
def send_data_to_api(api_url, data, api_type):
    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            print(f"[{api_type}] Data sent successfully to {api_url}: {data}")
        else:
            print(f"[{api_type}] Failed to send data to {api_url}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[{api_type}] Error sending data to {api_url}: {e}")

# Function to trigger the API calls
def trigger_api(api_type, json_path, api_url):
    global stop_threads
    # Read the JSON data
    data = read_json_data(json_path)
    
    while not stop_threads:
        for item in data:
            if stop_threads:
                break
            # Send each item as a POST request
            send_data_to_api(api_url, item, api_type)
            # Wait for 5 seconds before sending the next data
            time.sleep(5)
        if not stop_threads:
            print(f"[{api_type}] End of data reached. Restarting from the beginning.")
            time.sleep(5)  # Optional: Delay before restarting

# Signal handler to stop the script gracefully
def signal_handler(sig, frame):
    global stop_threads
    print("\n[INFO] Termination signal received. Stopping all threads...")
    stop_threads = True
    sys.exit(0)

# Register the signal handler for Ctrl + C
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    # Create threads for each API
    venti_thread = threading.Thread(target=trigger_api, args=('venti', venti_json_path, venti_api_url))
    mri_thread = threading.Thread(target=trigger_api, args=('mri', mri_json_path, mri_api_url))
    patient_thread = threading.Thread(target=trigger_api, args=('patient', patient_json_path, patient_api_url))

    # Start all threads simultaneously
    venti_thread.start()
    mri_thread.start()
    patient_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)
