import csv
import json
import os

file_paths = [
    {
        "csv": r"E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_ventilator_data.csv",
        "json": r"E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_ventilator_data.json",
    },
    {
        "csv": r"E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_mri_data.csv",
        "json": r"E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_mri_data.json",
    },
    {
        "csv": r"E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_patient_monitor_data.csv",
        "json": r"E:\fydp-last-sem\fydp-model-api-dd\Server\data\d-generated_patient_monitor_data.json",
    },
]

def convert_csv_to_json(csv_file_path, json_file_path):
    if os.path.exists(json_file_path):
        print(f"JSON file already exists, skipping conversion: {json_file_path}")
        return
    
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
    
    with open(json_file_path, mode='w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"CSV data successfully converted to JSON and saved to {json_file_path}")

def process_all_files(file_paths):
    for file_pair in file_paths:
        csv_file_path = file_pair["csv"]
        json_file_path = file_pair["json"]
        
        if not os.path.exists(csv_file_path):
            print(f"CSV file not found, skipping: {csv_file_path}")
            continue
        
        convert_csv_to_json(csv_file_path, json_file_path)

if __name__ == "__main__":
    process_all_files(file_paths)
