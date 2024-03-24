### testing to see if the end point works and what does the reponse data look like

import requests

# API configuration
base_url = "https://beaconcha.in/api/v1"
validator_id = "237172"  # Example validator ID, replace with your actual ID
headers = {'Content-Type': 'application/json'}  # Update if needed

def fetch_balance_history(validator_id):
    """
    Fetch historical balance data for a given validator.
    """
    endpoint = f"{base_url}/validator/{validator_id}/balancehistory"
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()
        return balance_data
    else:
        print(f"Error fetching balance history: {response.status_code}")
        return None

def main():
    balance_history = fetch_balance_history(validator_id)
    if balance_history:
        print("Fetched balance history data:")
        print(balance_history)
    else:
        print("Failed to fetch data or no data available.")

if __name__ == "__main__":
    main()
