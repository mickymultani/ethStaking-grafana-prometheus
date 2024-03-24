from flask import Flask, Response
import requests
import time

app = Flask(__name__)

BEACON_CHAIN_API_URL = "https://beaconcha.in/api/v1/validator/"
VALIDATOR_ID = "237172"

@app.route('/metrics')
def metrics():
    response = requests.get(f"{BEACON_CHAIN_API_URL}{VALIDATOR_ID}/balancehistory")
    if response.status_code == 200:
        data = response.json().get('data', [])
        metrics_response = ""
        for entry in data:
            timestamp = int(time.mktime(time.strptime(entry['week_end'], "%Y-%m-%dT%H:%M:%SZ"))) * 1000
            metrics_response += f'validator_balance{{validator_id="{VALIDATOR_ID}"}} {entry["balance"]} {timestamp}\n'
        return Response(metrics_response, mimetype='text/plain')
    else:
        return Response(f"Error fetching data from beaconcha.in API: {response.status_code}", status=500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
