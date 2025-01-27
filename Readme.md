# Project Setup and Execution

## Important Commands

1. **Install dependencies:**
   - Move into the **server** folder and run the following command:
     ```bash
     pip install -r requirements.txt
     ```

2. **Run the app:**
   - After installing dependencies, run this command to start the application:
     ```bash
     python server/app.py
     ```

3. **Run the API Trigger:**
   - Move into the **server** folder, then navigate to the **trigger** folder, and run the following command:
     ```bash
     python server/trigger/api_trigger.py
     ```

## File Path Configuration

1. **Converter File:**
   - In the **data** folder, there is a file named **converter.py**, which contains paths for CSV and JSON files.
   - Change the paths according to your laptop's file structure.
   - To do this, right-click on the CSV or JSON file in VS Code, click on **"Copy Path"**, and replace the existing paths in the `converter.py` file with the new ones.

2. **API Trigger File:**
   - In the **trigger** folder, there is a file named **api_trigger.py**, which also uses the file path of the JSON file from the **data** folder.
   - Similarly, right-click on the JSON file in the **data** folder, click on **"Copy Path"**, and replace the old path with the new one in `api_trigger.py`.

## Conclusion

Once you've set up the project and configured the file paths, you should be able to run the application and trigger the necessary processes. If you encounter any issues, check the paths again or refer to the project documentation for further troubleshooting.

Thank you for using this project! If you have any questions or need further assistance, feel free to email me at **moinraufc04@gmail.com**.
