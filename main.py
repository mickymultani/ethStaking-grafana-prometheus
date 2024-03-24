import requests
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# Replace these with your actual InfluxDB settings
influxdb_url = 'http://localhost:8086'
influxdb_token = 'pgyLUw-IaZrxhwtLOw9Lal__R9BGnTfnACV40d2xAmXTGwTu9tcWArQox-K9JnF7VHgbWGx5a5KLq9fIoabhug=='
influxdb_org = 'StakeMax'
influxdb_bucket = 'stake-poc'

# API configuration
base_url = "https://beaconcha.in/api/v1"
validator_id = "237172"  # Random Lido validator
headers = {'Content-Type': 'application/json'}  # Update if needed

# Initialize InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = client.write_api(write_options=SYNCHRONOUS)


def fetch_and_store_data(endpoint, measurement):
    """
    Fetch data from a given endpoint and write it to InfluxDB using the specified measurement.
    """
    response = requests.get(f"{base_url}/{endpoint}", headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        # Check if 'data' is a list or a single dictionary and adjust accordingly
        data_points = response_data.get('data', [])
        # If 'data' is a single dictionary, wrap it in a list to simplify processing
        if isinstance(data_points, dict):
            data_points = [data_points]

        for data_point in data_points:
            point = Point(measurement)
            for key, value in data_point.items():
                if isinstance(value, (int, float, str)):  # Assuming these are the acceptable types
                    point = point.field(key, value)
            point.time(datetime.utcnow())
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
    else:
        print(f"Error fetching data from {endpoint}: {response.status_code}")



def main():
    # Historical Data Endpoints
    historical_endpoints = {
        f"validator/{validator_id}/balancehistory": "balance_history",
        f"validator/stats/{validator_id}": "daily_stats",
        # Add other historical endpoints here
    }

    # Current Data Endpoints
    current_endpoints = {
        f"validator/{validator_id}": "current_validator_info",
        f"validator/{validator_id}/attestationefficiency": "attestation_efficiency",
        # Add other current endpoints here
    }

    # Fetch and store historical data
    for endpoint, measurement in historical_endpoints.items():
        fetch_and_store_data(endpoint, measurement)
        time.sleep(6)  # Respect the API rate limit

    # Fetch and store current data
    for endpoint, measurement in current_endpoints.items():
        fetch_and_store_data(endpoint, measurement)
        time.sleep(6)  # Respect the API rate limit

if __name__ == "__main__":
    main()
