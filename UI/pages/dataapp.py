from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

# Load the Excel data categorized using LLMs
# df = pd.read_excel(r"C:\Users\Sneha\Desktop\Predixion AI\prm-sys2\UI\classified_transactions4.xlsx")
df=pd.read_csv(r"UI\xns_extra_data.csv")

@app.route('/get_data', methods=['GET'])
def get_data():
    # Convert the DataFrame to a dictionary
    data = df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
