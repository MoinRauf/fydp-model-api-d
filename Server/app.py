from flask import Flask
from venti.venti_api import venti_api
from mri.mri_api import mri_api
from patient.patient_api import patient_api  # Import the Patient API Blueprint

# Initialize Flask app
app = Flask(__name__)

# Register the blueprints for each API
app.register_blueprint(venti_api)
app.register_blueprint(mri_api)
app.register_blueprint(patient_api)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
