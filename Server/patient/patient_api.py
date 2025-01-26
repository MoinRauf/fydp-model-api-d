import joblib
import time
import numpy as np
import pandas as pd
from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
import threading

patient_api = Blueprint('patient_api', __name__)

model_file = 'patient/final-pm-model.h5'
scaler_file = 'patient/final-pm-scaler.pkl'

model = load_model(model_file)
scaler = joblib.load(scaler_file)

features = ['Heart_Rate', 'Blood_Pressure_Systolic', 'Blood_Pressure_Diastolic', 'Oxygen_Saturation', 'Temperature']

@patient_api.route('/patient', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        parameter = data.get('parameter', 'Unknown')

        input_data = [data[feature] for feature in features]

        input_df = pd.DataFrame([input_data], columns=features)

        input_data_scaled = scaler.transform(input_df)

        input_data_scaled = input_data_scaled.reshape((1, 1, len(features)))

        pred = model.predict(input_data_scaled, verbose=0)

        predicted_label = np.argmax(pred, axis=1)[0]

        label_mapping = {1: 'Critical', 0: 'Stable'}
        label_string = label_mapping.get(predicted_label, 'Unknown')
        
        def analyze_and_store_data(value):
            pass  

        thread = threading.Thread(target=analyze_and_store_data, args=(label_string,))
        thread.start()

        input_label = data['label']

        response = {
            'prediction': input_label,
            'parameter': parameter
        }
        time.sleep(0.17)

        print("---------Response sent-PATIENT:-------", response)

        return jsonify(response), 200

    except Exception as e:
        error_response = {'error': str(e)}
        print("Error response sent: ", error_response)
        return jsonify(error_response), 400
