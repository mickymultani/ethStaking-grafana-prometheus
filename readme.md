# Monitoring Ethereum Validator Balances with Prometheus and Grafana
Set up a monitoring solution for tracking Ethereum validator balances using Prometheus for data storage, 
a custom Python exporter for fetching data from the beaconcha.in API, and Grafana for visualization.


## Virtual Environment Details:
```
conda create --name staking_dashboard python=3.10
conda activate staking_dashboard
```

Install necessary packages:
```
conda install requests pandas
conda install -c conda-forge influxdb-client
```

### 1. Write an adapter for Promethus (scraping end point)
See code for python_exporter.py in the repo

### 2. Start the adapter
```
python python_exporter.py
```

### 3. Download and start Prometheus
Download from https://prometheus.io/download/
Version: prometheus-2.51.0.linux-amd64.tar.gz

### 4. Configure the YAML file:
Open the prometheus.yml file  and update the scrape config:

```
scrape_configs:
  - job_name: 'python_exporter'
    honor_timestamps: false
    static_configs:
      - targets: ['localhost:8000']
```

### 5. Run Prometheus
Run Prometheus (for linux: ./prometheus --config.file=prometheus.yml)

Access Prometheus at http://localhost:9090


### Download and start Grafana
Download from https://grafana.com/grafana/download
Version: grafana-enterprise-10.4.1.linux-amd64.tar.gz
Run grafana (for linux: ./bin/grafana-server)

Access Grafana at http://localhost:3000 and log in(default is admin/admin)

Add Prometheus as a data source through Grafana's UI: Configuration > Data Sources > Add data source > Prometheus. 
Set the URL to http://localhost:9090.

Create a dashboard and panel for visualizing the validator balance. 
Use the query validator_balance{validator_id="237172"}.

*******************************************************************************************************************




### InfluxDB option not working (flux issues?!)------------------------------------
Install InfluxDB
Installed influxdb from the website https://github.com/influxdata/influxdb/releases/tag/v2.7.5
version installed: influxdb2_2.7.5-1_amd64.deb

- Check status if its running: sudo systemctl status influxdb
- If its not running, you can start with: sudo systemctl start influxdb
- Enable influxdb on startup: sudo systemctl enable influxdb

### InfluxDB Operator API token: 
org = StakeMax
bucket = stake-poc
----------------------------------------------------------------------------------------------
