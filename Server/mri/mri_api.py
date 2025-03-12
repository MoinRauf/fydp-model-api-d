from flask import Blueprint, request, jsonify
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
import logging

mri_api = Blueprint('mri_api', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained model
mri_model = load_model('mri/final-mri_model.h5')
logger.info("Model loaded successfully.")

# Load the pre-trained scaler
scaler = joblib.load('mri/final-mri-scaler.pkl')
logger.info("Scaler loaded successfully.")

# Define feature columns
feature_columns = ['Magnetic_Field_Strength', 'Gradient_Strength', 'RF_Power', 'Pulse_Sequence', 'Scan_Duration']


def reshape_input(input_data):
    """Reshape input data for LSTM model."""
    return input_data.reshape((input_data.shape[0], 1, input_data.shape[1]))

def preprocess_input(input_dict):
    """Preprocess the input data into a DataFrame."""
    try:
        missing_fields = set(feature_columns) - set(input_dict.keys())
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        processed_data = pd.DataFrame([input_dict], columns=feature_columns)
        logger.info(f"Preprocessed data: {processed_data}")
        return processed_data
    except Exception as e:
        logger.error(f"Error in preprocess_input: {e}")
        raise ValueError(f"Error processing input data: {str(e)}")

def scale_data(input_data):
    """Scale the input data using the loaded scaler."""
    try:
        scaled_data = scaler.transform(input_data)
        logger.info(f"Scaled data: {scaled_data}")
        return scaled_data
    except Exception as e:
        logger.error(f"Error in scale_data: {e}")
        raise ValueError(f"Error scaling data: {str(e)}")

def model_predict(input_data):
    """Make predictions using the loaded model."""
    try:
        prediction = mri_model.predict(input_data)
        logger.info(f"Model prediction: {prediction}")
        return prediction
    except Exception as e:
        logger.error(f"Error in model_predict: {e}")
        raise ValueError(f"Error making prediction: {str(e)}")

def map_prediction_to_label(prediction):
    """Map model prediction to a human-readable label."""
    predicted_class = np.argmax(prediction, axis=1)[0]
    return 'Malfunction' if predicted_class == 1 else 'Not malfunction'

def batch_predict(input_data_list):
    """Make predictions for a batch of input data."""
    try:
        reshaped_data = np.array([
            reshape_input(scale_data(preprocess_input(input_data)))
            for input_data in input_data_list
        ])
        predictions = mri_model.predict(np.vstack(reshaped_data))
        logger.info(f"Batch prediction: {predictions}")
        return [map_prediction_to_label(pred) for pred in predictions]
    except Exception as e:
        logger.error(f"Error in batch_predict: {e}")
        raise ValueError(f"Error in batch prediction: {str(e)}")

def get_impact_level(time_value):
    """Categorize the impact level based on time value."""
    try:
        time_value = float(time_value)
        if time_value <= 0 or time_value <= 5:
            return "Low Impact"
        elif time_value > 5 and time_value <= 8:
            return "Moderate Impact"
        elif time_value > 8:
            return "High Impact"
        else:
            return "Invalid Time"
    except ValueError:
        return "Invalid Time"

# Define your routes
@mri_api.route('/predict', methods=['POST'])
def predict():
    try:
        request_data = request.json
        logger.info(f"Received request data: {request_data}")

        # Extract 'Time' from input data
        input_time = request_data.get('Time', None)

        if isinstance(request_data, list):
            # Batch prediction
            predictions = batch_predict(request_data)
            response_data = {'predictions': predictions}

            # Get impact level based on time
            impact_level = get_impact_level(input_time)
            response_data['impact_level'] = impact_level

        else:
            # Single prediction
            preprocessed_data = preprocess_input(request_data)
            scaled_data = scale_data(preprocessed_data)
            reshaped_data = reshape_input(scaled_data)
            raw_prediction = model_predict(reshaped_data)
            predicted_label = map_prediction_to_label(raw_prediction)

            response_data = {
                'prediction': predicted_label
            }

            # Get impact level based on time
            if input_time:
                impact_level = get_impact_level(input_time)
                response_data['impact_level'] = impact_level


        print("---------Response sent-mri:-------", response_data)
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in /predict endpoint: {e}")
        return jsonify({'error': str(e)})
