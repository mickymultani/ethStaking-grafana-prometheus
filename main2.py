import requests
from influxdb_client import InfluxDBClient, Point
from datetime import datetime

# InfluxDB Settings
influxdb_url = 'http://localhost:8086'
influxdb_token = 'pgyLUw-IaZrxhwtLOw9Lal__R9BGnTfnACV40d2xAmXTGwTu9tcWArQox-K9JnF7VHgbWGx5a5KLq9fIoabhug=='
influxdb_org = 'StakeMax'
influxdb_bucket = 'new-test'

# API Configuration
base_url = "https://beaconcha.in/api/v1"
validator_id = "237172"  # Example validator ID

# Initialize InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = client.write_api()

def fetch_balance_history():
    """
    Fetches balance history from the beaconcha.in API and writes it to InfluxDB.
    """
    endpoint = f"{base_url}/validator/{validator_id}/balancehistory"
    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json().get('data', [])
        for entry in data:
            point = Point("balance_history")\
                .tag("validator_index", str(entry['validatorindex']))\
                .field("balance", float(entry['balance']))\
                .field("effective_balance", float(entry['effectivebalance']))\
                .time(datetime.strptime(entry['week_end'], "%Y-%m-%dT%H:%M:%SZ"))

            write_api.write(bucket=influxdb_bucket, record=point)

        print(f"Successfully wrote {len(data)} balance history records to InfluxDB.")
    else:
        print(f"Failed to fetch balance history. Status code: {response.status_code}")

def main():
    try:
        fetch_balance_history()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensures all pending writes are flushed and connections are closed properly
        write_api.close()
        client.close()

if __name__ == "__main__":
    main()
