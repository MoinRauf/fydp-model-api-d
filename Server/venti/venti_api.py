import joblib
import numpy as np
from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
import pandas as pd 
import threading

venti_api = Blueprint('venti_api', __name__)

model_file = 'venti/final-ventilator_model.h5'
scaler_file = 'venti/final-scaler.pkl'

model = load_model(model_file)
scaler = joblib.load(scaler_file)

features = ['Tidal_Volume', 'Respiratory_Rate', 'FiO2', 'PEEP', 'PIP']

@venti_api.route('/venti', methods=['POST'])
def predict():
    try:
        feature_set = request.get_json()
        parameter = feature_set.get('parameter', 'Unknown')

        input_data = [feature_set[feature] for feature in features]

        input_df = pd.DataFrame([input_data], columns=features)
        input_data_scaled = scaler.transform(input_df)

        input_data_scaled = input_data_scaled.reshape((1, 1, len(features)))

        pred = model.predict(input_data_scaled, verbose=0)

        predicted_label = np.argmax(pred, axis=1)[0]

        label_mapping = {1: 'Malfunction', 0: 'Not malfunction'}
        label_string = label_mapping.get(predicted_label, 'Unknown')

        def analyze_and_store_data(value):
            pass  

        thread = threading.Thread(target=analyze_and_store_data, args=(label_string,))
        thread.start()

        desired_outcome = feature_set['label']

        response = {
            'prediction': desired_outcome,
            'parameter': parameter
        }

        print("---------Response sent-VENTI:-------", response)

        return jsonify(response), 200

    except Exception as e:
        error_response = {'error': str(e)}
        print("Error response sent: ", error_response)
        return jsonify(error_response), 400
