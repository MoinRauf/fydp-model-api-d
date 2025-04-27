from flask import Flask
from flask_cors import CORS  # Import CORS
from venti.venti_api import venti_api  # Import the Venti API Blueprint
from mri.mri_api import mri_api
from patient.patient_api import patient_api  # Import the Patient API Blueprint

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register the Blueprints for each API
app.register_blueprint(venti_api, url_prefix='/venti')  # Add a prefix for clarity
app.register_blueprint(mri_api, url_prefix='/mri')
app.register_blueprint(patient_api, url_prefix='/patient')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
