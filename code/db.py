from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# 1. Connect to InfluxDB server
url = "http://localhost:8086"
token = "YOUR_API_TOKEN"
org = "YOUR_ORG"
bucket = "YOUR_BUCKET"

client = InfluxDBClient(url=url, token=token, org=org)

# 2. Write Data
write_api = client.write_api(write_options=SYNCHRONOUS)

point = Point("cpu_usage") \
    .tag("host", "server01") \
    .field("usage", 45.2)

write_api.write(bucket=bucket, org=org, record=point)
print("Data point successfully written!")

# 3. Query Data (Flux Query)
query_api = client.query_api()

query = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu_usage")'
result = query_api.query(org=org, query=query)

for table in result:
    for record in table.records:
        print(f"Host: {record.values.get('host')} -> Usage: {record.get_value()}")

client.close()