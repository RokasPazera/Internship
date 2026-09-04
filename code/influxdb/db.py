import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient


load_dotenv()
url = os.getenv("INFLUXDB_URL")
token = os.getenv("INFLUXDB_TOKEN")
org = os.getenv("INFLUXDB_ORG")
bucket = os.getenv("INFLUXDB_BUCKET")

if not token:
    raise ValueError("Missing required token credentials in .env file.")
if not org:
    raise ValueError("Missing required org credentials in .env file.")
if not bucket:
    raise ValueError("Missing required bucket credentials in .env file.")

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

query = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "meters")'
result = query_api.query(org=org, query=query)

for table in result:
    for record in table.records:
        if record.get_value() < 70 or record.get_value() > 80:
            print(f"Sensor: {record.values.get('sensor')} -> Distance: {record.get_value()} [ALERT]")
        else:
            print(f"Sensor: {record.values.get('sensor')} -> Distance: {record.get_value()} [OK]")

client.close()
